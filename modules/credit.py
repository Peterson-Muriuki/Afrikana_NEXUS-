"""Credit Intelligence Module"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_loan_applications, score_single_applicant


def render():
    st.title("💳 Credit Intelligence")
    st.caption("Dual-model PD scoring · Expected loss · Portfolio segmentation · Decision engine")

    if "loan_df" not in st.session_state:
        st.session_state.loan_df = generate_loan_applications(500)
    df = st.session_state.loan_df

    tab1, tab2, tab3 = st.tabs(["📋 Portfolio Overview", "🔍 Individual Scorer", "📉 EL & Risk Bands"])

    # ── Tab 1: Portfolio Overview ─────────────────────────────────────────
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Applications",   f"{len(df):,}")
        c2.metric("Avg Credit Score",      f"{df['credit_score'].mean():.0f}")
        c3.metric("Portfolio Avg PD",      f"{df['default_probability'].mean()*100:.2f}%")
        c4.metric("Actual Default Rate",   f"{df['defaulted'].mean()*100:.2f}%")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("PD distribution by employment type")
            pd_emp = df.groupby("employment_type")["default_probability"].mean().sort_values()
            fig = go.Figure(go.Bar(
                x=pd_emp.values * 100, y=pd_emp.index,
                orientation="h", marker_color="#6ab0ff",
                text=[f"{v:.1f}%" for v in pd_emp.values * 100],
                textposition="outside"
            ))
            fig.update_layout(height=280, margin=dict(l=0, r=40, t=10, b=0),
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#d0d6e8"),
                              xaxis_title="Avg PD (%)")
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("Credit score by county")
            score_county = df.groupby("county")["credit_score"].mean().sort_values(ascending=False)
            fig2 = go.Figure(go.Bar(
                x=score_county.index, y=score_county.values,
                marker_color="#4ade80",
                text=[f"{v:.0f}" for v in score_county.values],
                textposition="outside"
            ))
            fig2.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               yaxis_title="Avg Score")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Score vs PD scatter")
        fig3 = px.scatter(
            df.sample(200, random_state=1),
            x="credit_score", y="default_probability",
            color="employment_type", size="loan_amount",
            opacity=0.6, height=320,
            labels={"credit_score": "Credit Score",
                    "default_probability": "PD",
                    "employment_type": "Employment"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2: Individual Scorer ───────────────────────────────────────────
    with tab2:
        st.subheader("Score an applicant")
        st.markdown("Enter applicant details to get an instant AI credit decision.")

        col1, col2, col3 = st.columns(3)
        with col1:
            age            = st.number_input("Age", 18, 75, 32)
            monthly_income = st.number_input("Monthly income (KES)", 5000, 500000, 45000, step=5000)
            loan_amount    = st.number_input("Loan amount (KES)", 1000, 2000000, 80000, step=5000)
        with col2:
            mm_tenure   = st.slider("Mobile money tenure (months)", 0, 60, 24)
            mm_freq     = st.slider("Monthly MM transactions", 0, 80, 22)
            sim_age     = st.slider("SIM age (months)", 0, 72, 30)
        with col3:
            in_chama  = st.selectbox("In a chama/SACCO?", [1, 0],
                                     format_func=lambda x: "Yes" if x else "No")
            crb_score = st.number_input("CRB score (0 = none)", 0, 700, 520)

        if st.button("Score applicant →", type="primary"):
            result = score_single_applicant({
                "age": age, "monthly_income": monthly_income,
                "loan_amount": loan_amount, "mm_tenure_months": mm_tenure,
                "mm_txn_frequency": mm_freq, "sim_age_months": sim_age,
                "in_chama": in_chama, "crb_score": crb_score,
            })
            color = {"APPROVE": "#4ade80", "REFER": "#fbbf24", "DECLINE": "#f87171"}
            st.markdown(f"""
            <div style='background:#222840;border:1px solid #2d3347;border-radius:10px;padding:1.5rem;margin-top:1rem'>
              <div style='font-size:1.4rem;font-weight:700;color:{color[result["decision"]]};margin-bottom:0.8rem'>
                {result["decision"]}
              </div>
              <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem'>
                <div><div style='font-size:11px;color:#9aa5c0'>Credit Score</div>
                     <div style='font-size:1.3rem;font-weight:600;color:#e8edf8'>{result["credit_score"]} ({result["grade"]})</div></div>
                <div><div style='font-size:11px;color:#9aa5c0'>PD</div>
                     <div style='font-size:1.3rem;font-weight:600;color:#e8edf8'>{result["pd"]*100:.2f}%</div></div>
                <div><div style='font-size:11px;color:#9aa5c0'>LGD</div>
                     <div style='font-size:1.3rem;font-weight:600;color:#e8edf8'>{result["lgd"]*100:.0f}%</div></div>
                <div><div style='font-size:11px;color:#9aa5c0'>Expected Loss</div>
                     <div style='font-size:1.3rem;font-weight:600;color:#e8edf8'>KES {result["expected_loss"]:,.0f}</div></div>
              </div>
              <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem'>
                <div><div style='font-size:11px;color:#9aa5c0'>Mobile Money Score</div>
                     <div style='font-size:1rem;color:#e8edf8'>{result["mm_score"]:.3f}</div></div>
                <div><div style='font-size:11px;color:#9aa5c0'>Social Capital Score</div>
                     <div style='font-size:1rem;color:#e8edf8'>{result["social_score"]:.3f}</div></div>
                <div><div style='font-size:11px;color:#9aa5c0'>DTI Ratio</div>
                     <div style='font-size:1rem;color:#e8edf8'>{result["dti_ratio"]:.3f}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: EL & Risk Bands ─────────────────────────────────────────────
    with tab3:
        df["el"] = df["default_probability"] * 0.55 * df["loan_amount"]
        df["risk_grade"] = pd.cut(
            df["credit_score"],
            bins=[0, 560, 620, 680, 750, 1000],
            labels=["E (High Risk)", "D", "C", "B", "A (Low Risk)"]
        )

        st.subheader("Expected loss by loan purpose")
        el_purpose = df.groupby("loan_purpose")["el"].sum() / 1e6
        fig = go.Figure(go.Bar(
            x=el_purpose.index,
            y=el_purpose.values,
            marker_color=["#6ab0ff", "#4ade80", "#fbbf24", "#f87171", "#c084fc", "#ec6547"],
            text=[f"KES {v:.1f}M" for v in el_purpose.values],
            textposition="outside"
        ))
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#d0d6e8"),
                          yaxis_title="Expected Loss (KES M)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Risk grade distribution")
        grade_ct = df["risk_grade"].value_counts().sort_index()
        fig2 = go.Figure(go.Pie(
            labels=grade_ct.index.astype(str),
            values=grade_ct.values,
            hole=0.5,
            marker_colors=["#f87171", "#fbbf24", "#6ab0ff", "#4ade80", "#c084fc"]
        ))
        fig2.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"))
        st.plotly_chart(fig2, use_container_width=True)
