"""Customer Analytics Module"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_customers


def render():
    st.title("👥 Customer Analytics")
    st.caption("Churn scoring · LTV/CAC · Segment profiling · Retention strategy · Geographic distribution")

    if "cust_df" not in st.session_state:
        st.session_state.cust_df = generate_customers(800)
    df = st.session_state.cust_df

    avg_ltv  = df["ltv_ksh"].mean()
    avg_cac  = df["cac_ksh"].mean()
    ltv_cac  = df["ltv_cac_ratio"].mean()
    churn    = df["churn_probability"].mean()
    high_pct = (df["risk_band"] == "High").mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg LTV",         f"KES {avg_ltv:,.0f}")
    c2.metric("Avg CAC",         f"KES {avg_cac:,.0f}")
    c3.metric("LTV/CAC Ratio",   f"{ltv_cac:.2f}x")
    c4.metric("Portfolio Churn", f"{churn*100:.1f}%", delta_color="inverse")
    c5.metric("High-Risk %",     f"{high_pct:.1f}%",  delta_color="inverse")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["🎯 Segment Analysis", "⚠️ Churn Risk", "🗺️ Geography"])

    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("LTV/CAC by segment")
            seg_stats = df.groupby("segment")["ltv_cac_ratio"].mean().sort_values(ascending=False)
            fig = go.Figure(go.Bar(
                x=seg_stats.index, y=seg_stats.values,
                marker_color=["#4ade80" if v >= 3 else "#fbbf24" if v >= 2 else "#f87171"
                              for v in seg_stats.values],
                text=[f"{v:.2f}x" for v in seg_stats.values],
                textposition="outside"
            ))
            fig.add_hline(y=3, line_dash="dash", line_color="#9aa5c0",
                          annotation_text="Target 3.0x")
            fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#d0d6e8"),
                              yaxis_title="LTV/CAC Ratio")
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.subheader("Revenue by segment")
            seg_rev = df.groupby("segment")["monthly_revenue_ksh"].agg(["mean", "sum"])
            fig2 = go.Figure(go.Bar(
                x=seg_rev.index, y=seg_rev["sum"] / 1e6,
                marker_color="#6ab0ff",
                text=[f"KES {v:.1f}M" for v in seg_rev["sum"] / 1e6],
                textposition="outside"
            ))
            fig2.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               yaxis_title="Total Monthly Revenue (KES M)")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("LTV vs CAC — segment scatter")
        fig3 = px.scatter(
            df, x="cac_ksh", y="ltv_ksh",
            color="segment", size="monthly_revenue_ksh",
            opacity=0.6, height=320,
            labels={"cac_ksh": "CAC (KES)", "ltv_ksh": "LTV (KES)",
                    "segment": "Segment"},
            color_discrete_sequence=px.colors.qualitative.G10
        )
        # Add 3x line
        max_cac = df["cac_ksh"].max()
        fig3.add_trace(go.Scatter(
            x=[0, max_cac], y=[0, max_cac * 3],
            mode="lines", name="3x LTV/CAC",
            line=dict(color="#9aa5c0", dash="dash", width=1)
        ))
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Churn risk distribution")
        col_l, col_r = st.columns(2)

        with col_l:
            churn_band = df["risk_band"].value_counts()
            fig4 = go.Figure(go.Pie(
                labels=churn_band.index,
                values=churn_band.values,
                hole=0.5,
                marker_colors=["#4ade80", "#fbbf24", "#f87171"]
            ))
            fig4.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"))
            st.plotly_chart(fig4, use_container_width=True)

        with col_r:
            st.subheader("At-risk customers (churn > 40%)")
            at_risk = df[df["churn_probability"] > 0.40].sort_values(
                "churn_probability", ascending=False
            ).head(10)[["customer_id", "segment", "country",
                         "tenure_months", "monthly_revenue_ksh",
                         "ltv_ksh", "churn_probability"]]
            at_risk["churn_probability"] = (at_risk["churn_probability"] * 100).round(1).astype(str) + "%"
            st.dataframe(at_risk.reset_index(drop=True),
                         use_container_width=True, height=280)

        st.subheader("Churn probability by tenure band")
        df["tenure_band"] = pd.cut(df["tenure_months"], [0, 6, 12, 24, 48],
                                   labels=["0-6m", "6-12m", "12-24m", "24-48m"])
        churn_tenure = df.groupby("tenure_band")["churn_probability"].mean()
        fig5 = go.Figure(go.Bar(
            x=churn_tenure.index.astype(str),
            y=churn_tenure.values * 100,
            marker_color=["#f87171", "#fbbf24", "#6ab0ff", "#4ade80"],
            text=[f"{v:.1f}%" for v in churn_tenure.values * 100],
            textposition="outside"
        ))
        fig5.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=30),
                           plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"),
                           yaxis_title="Avg Churn Probability (%)")
        st.plotly_chart(fig5, use_container_width=True)

    with tab3:
        st.subheader("Customer distribution by country")
        country_stats = df.groupby("country").agg(
            Customers=("customer_id", "count"),
            Avg_LTV=("ltv_ksh", "mean"),
            Avg_Churn=("churn_probability", "mean"),
        ).reset_index()
        country_stats["Avg_LTV"] = country_stats["Avg_LTV"].astype(int)
        country_stats["Avg_Churn_Pct"] = (country_stats["Avg_Churn"] * 100).round(1)

        fig6 = go.Figure(go.Bar(
            x=country_stats["country"],
            y=country_stats["Customers"],
            marker_color="#6ab0ff",
            text=country_stats["Customers"],
            textposition="outside"
        ))
        fig6.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=30),
                           plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"))
        st.plotly_chart(fig6, use_container_width=True)
        st.dataframe(country_stats.drop(columns=["Avg_Churn"]), use_container_width=True)
