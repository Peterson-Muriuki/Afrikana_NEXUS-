"""Portfolio & ESG Optimization Module"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_portfolio_assets, optimize_portfolio


def render():
    st.title("📊 Portfolio Optimization & ESG")
    st.caption("Markowitz mean-variance · ESG integration · Efficient frontier · Risk attribution")

    if "assets_df" not in st.session_state:
        assets_df, returns_df = generate_portfolio_assets(12)
        st.session_state.assets_df  = assets_df
        st.session_state.returns_df = returns_df
    assets_df  = st.session_state.assets_df
    returns_df = st.session_state.returns_df

    st.sidebar.markdown("---")
    esg_min    = st.sidebar.slider("Min ESG score constraint", 30, 80, 50)
    max_weight = st.sidebar.slider("Max single asset weight", 0.10, 0.50, 0.30)
    rf_rate    = st.sidebar.slider("Risk-free rate (%)", 5.0, 15.0, 9.0) / 100

    result = optimize_portfolio(assets_df, returns_df, esg_min, max_weight)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Portfolio Return",  f"{result['expected_return']*100:.2f}%")
    c2.metric("Portfolio Vol",     f"{result['volatility']*100:.2f}%")
    c3.metric("Sharpe Ratio",      f"{result['sharpe_ratio']:.3f}")
    c4.metric("Weighted ESG",      f"{result['esg_score']:.1f}/100")

    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Optimal portfolio weights")
        w = result["weights"]
        w_filtered = {k: v for k, v in w.items() if v > 0.01}
        fig = go.Figure(go.Pie(
            labels=list(w_filtered.keys()),
            values=[round(v * 100, 2) for v in w_filtered.values()],
            hole=0.5,
            marker_colors=px.colors.qualitative.G10
        ))
        fig.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#d0d6e8"))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("ESG scores by asset")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Environmental", x=assets_df["ticker"], y=assets_df["e_score"],
            marker_color="#4ade80"
        ))
        fig2.add_trace(go.Bar(
            name="Social", x=assets_df["ticker"], y=assets_df["s_score"],
            marker_color="#6ab0ff"
        ))
        fig2.add_trace(go.Bar(
            name="Governance", x=assets_df["ticker"], y=assets_df["g_score"],
            marker_color="#c084fc"
        ))
        fig2.update_layout(barmode="group", height=320,
                           margin=dict(l=0, r=0, t=10, b=30),
                           plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"),
                           legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True)

    # Efficient frontier simulation
    st.subheader("Efficient frontier")
    n = len(assets_df)
    mu_vec  = assets_df["expected_return"].values
    cov_mat = returns_df.cov().values * 252

    frontier_rets, frontier_vols, frontier_sharpes = [], [], []
    for _ in range(1500):
        w_rand = np.random.dirichlet(np.ones(n))
        r = w_rand @ mu_vec
        v = np.sqrt(w_rand @ cov_mat @ w_rand)
        s = (r - rf_rate) / (v + 1e-9)
        frontier_rets.append(r)
        frontier_vols.append(v)
        frontier_sharpes.append(s)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=[v * 100 for v in frontier_vols],
        y=[r * 100 for r in frontier_rets],
        mode="markers",
        marker=dict(color=frontier_sharpes, colorscale="Viridis",
                    size=4, opacity=0.6,
                    colorbar=dict(title="Sharpe")),
        name="Random portfolios"
    ))
    opt_vol = result["volatility"]
    opt_ret = result["expected_return"]
    fig3.add_trace(go.Scatter(
        x=[opt_vol * 100], y=[opt_ret * 100],
        mode="markers+text",
        marker=dict(color="#f87171", size=14, symbol="star"),
        text=["Optimal"], textposition="top center",
        textfont=dict(color="#e8edf8"),
        name="Optimal (ESG-constrained)"
    ))
    fig3.update_layout(
        height=360, xaxis_title="Volatility (%)", yaxis_title="Expected Return (%)",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#d0d6e8"),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Asset universe")
    display = assets_df.copy()
    display["weight_%"] = [f"{result['weights'].get(t,0)*100:.1f}%" for t in display["ticker"]]
    display["expected_return"] = (display["expected_return"] * 100).round(2).astype(str) + "%"
    display["volatility"] = (display["volatility"] * 100).round(2).astype(str) + "%"
    st.dataframe(display[["ticker", "sector", "expected_return", "volatility",
                           "esg_score", "e_score", "s_score", "g_score",
                           "market_cap_bn", "weight_%"]],
                 use_container_width=True)
