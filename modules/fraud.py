"""Fraud & Verification Module"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_fraud_applications


def render():
    st.title("🛡️ Fraud Detection & Smart Verification")
    st.caption("3-tier cost-optimised pipeline · Free signals first · CRB only when necessary")

    if "fraud_df" not in st.session_state:
        st.session_state.fraud_df = generate_fraud_applications(300)
    df = st.session_state.fraud_df

    total = len(df)
    baseline_cost = total * 70
    actual_cost   = df["verification_cost_ksh"].sum()
    savings       = baseline_cost - actual_cost
    savings_pct   = savings / baseline_cost * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Applications processed", f"{total:,}")
    c2.metric("Cost savings vs CRB-all", f"KES {savings:,.0f}",
              f"{savings_pct:.1f}% saved")
    c3.metric("Fraud flag rate",
              f"{(df['fraud_score'] > 60).mean()*100:.1f}%")
    c4.metric("Approval rate",
              f"{(df['decision']=='APPROVE').mean()*100:.1f}%")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Decision pipeline funnel")
        paths = df["verification_path"].value_counts()
        labels = list(paths.index)
        values = list(paths.values)
        colors = {
            "TIER1_APPROVE":      "#4ade80",
            "TIER1_REJECT":       "#f87171",
            "TIER1_FRAUD_REJECT": "#da3633",
            "TIER2_APPROVE":      "#6ab0ff",
            "TIER3_CRB":          "#fbbf24",
        }
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            marker_color=[colors.get(l, "#9aa5c0") for l in labels],
            text=[f"{v} ({v/total*100:.0f}%)" for v in values],
            textposition="outside"
        ))
        fig.update_layout(height=280, margin=dict(l=0, r=80, t=10, b=0),
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#d0d6e8"))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Cost breakdown vs baseline")
        cost_data = {
            "All CRB (old method)": baseline_cost,
            "NEXUS 3-tier":          actual_cost,
        }
        fig2 = go.Figure(go.Bar(
            x=list(cost_data.keys()),
            y=list(cost_data.values()),
            marker_color=["#f87171", "#4ade80"],
            text=[f"KES {v:,.0f}" for v in cost_data.values()],
            textposition="outside"
        ))
        fig2.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                           plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"),
                           yaxis_title="Total Cost (KES)")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Fraud score vs Tier-1 risk score")
    fig3 = px.scatter(
        df, x="tier1_risk_score", y="fraud_score",
        color="verification_path", size="loan_amount",
        opacity=0.7, height=340,
        labels={"tier1_risk_score": "Tier-1 Risk Score",
                "fraud_score": "Fraud Score",
                "verification_path": "Decision Path"},
        color_discrete_sequence=px.colors.qualitative.G10
    )
    fig3.add_hline(y=60, line_dash="dash", line_color="#f87171",
                   annotation_text="Fraud threshold")
    fig3.add_vline(x=75, line_dash="dash", line_color="#4ade80",
                   annotation_text="Auto-approve")
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="#d0d6e8"))
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Sample applications")
    st.dataframe(
        df[["app_id", "loan_amount", "sim_age_months", "fraud_score",
            "tier1_risk_score", "verification_path", "verification_cost_ksh",
            "decision"]].head(20).reset_index(drop=True),
        use_container_width=True, height=300
    )
