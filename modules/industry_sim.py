"""Industry Simulator Module"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np


INDUSTRY_CONFIGS = {
    "🏦 Banking & Fintech": {
        "modules": ["Credit Intelligence", "Fraud & Verification", "ALM & Treasury",
                    "Portfolio & ESG", "Risk & Early Warning", "Market Intelligence"],
        "primary_metric": "Non-Performing Loan Ratio",
        "kpi_label": "NPL Target",
        "kpi_target": "< 5%",
        "key_risk": "Credit Risk & Liquidity",
        "data_sources": ["CRB scores", "Mobile money data", "Bank statements", "CRB alternative data"],
        "model_stack": ["XGBoost PD model", "LGD regression", "Nelson-Siegel yield curve",
                        "CVXPY portfolio optimiser", "VaR/CVaR engine"],
        "color": "#6ab0ff",
        "description": (
            "Full Basel II/III credit risk stack. PD-LGD-EAD pipeline feeds "
            "expected loss computation and RAROC pricing. ALM engine monitors "
            "duration gap and NIM sensitivity across rate shock scenarios."
        ),
    },
    "📱 Mobility & PAYG": {
        "modules": ["Credit Intelligence", "Customer Analytics", "Fraud & Verification",
                    "Risk & Early Warning"],
        "primary_metric": "PAYG Repayment Rate",
        "kpi_label": "Repayment Target",
        "kpi_target": "> 95%",
        "key_risk": "Collections & Churn",
        "data_sources": ["Mobile money repayment history", "Device telemetry",
                         "SIM age & behaviour", "Agent network data"],
        "model_stack": ["Conversion model (XGBoost)", "Repayment model (XGBoost + SMOTE)",
                        "Churn scorer (GBM)", "LTV survival model"],
        "color": "#4ade80",
        "description": (
            "Dual-model PAYG scoring: conversion probability → repayment risk. "
            "Alternative data (mobile money, SIM age, chama membership) replaces "
            "traditional bureau data. Churn and LTV engines drive segment retention."
        ),
    },
    "⚡ Energy & EV": {
        "modules": ["Customer Analytics", "Risk & Early Warning", "Portfolio & ESG"],
        "primary_metric": "Station Utilisation",
        "kpi_label": "Utilisation Target",
        "kpi_target": "> 70%",
        "key_risk": "Demand & Macro Volatility",
        "data_sources": ["Swap event logs", "Station telemetry", "FX rates", "Import duty data"],
        "model_stack": ["Holt-Winters demand forecaster", "Monte Carlo NPV",
                        "ESG-constrained portfolio", "Scenario analyser (Bull/Bear/Base)"],
        "color": "#fbbf24",
        "description": (
            "Financial model covers unit economics, DCF valuation, Monte Carlo simulation "
            "across 1000 scenarios, and ESG portfolio optimisation for impact investors. "
            "Demand forecasting drives station deployment decisions."
        ),
    },
    "🏢 Insurance": {
        "modules": ["Fraud & Verification", "Customer Analytics", "Risk & Early Warning",
                    "ALM & Treasury"],
        "primary_metric": "Combined Ratio",
        "kpi_label": "Combined Ratio Target",
        "kpi_target": "< 100%",
        "key_risk": "Underwriting & Liquidity",
        "data_sources": ["Claims history", "Actuarial tables", "Investment portfolio", "Premium data"],
        "model_stack": ["Fraud detection tier-1/2/3", "Churn prediction",
                        "ALM duration matching", "VaR on investment portfolio"],
        "color": "#c084fc",
        "description": (
            "Fraud detection pipeline filters fraudulent claims before expensive investigation. "
            "ALM engine matches asset-liability duration for P&C and life lines. "
            "Customer analytics optimises policyholder retention."
        ),
    },
    "🛒 Retail Credit": {
        "modules": ["Credit Intelligence", "Fraud & Verification", "Customer Analytics"],
        "primary_metric": "Approval Rate",
        "kpi_label": "Target Approval Rate",
        "kpi_target": "60–75%",
        "key_risk": "Default Rate & Fraud",
        "data_sources": ["POS transaction data", "Purchase history", "Device fingerprint",
                         "Telco data"],
        "model_stack": ["XGBoost credit scorer", "3-tier verification pipeline",
                        "Customer LTV model", "Segment churn predictor"],
        "color": "#ec6547",
        "description": (
            "Buy-now-pay-later and retail credit pipeline. Tiered verification "
            "starts with free fraud signals (SIM age, velocity, device), escalating "
            "to CRB only for borderline cases — cutting verification cost by 60–70%."
        ),
    },
    "🌾 Agri-Finance": {
        "modules": ["Credit Intelligence", "Risk & Early Warning", "Customer Analytics"],
        "primary_metric": "Seasonal Default Rate",
        "kpi_label": "Default Target",
        "kpi_target": "< 8%",
        "key_risk": "Seasonal & Weather Risk",
        "data_sources": ["Chama/SACCO data", "Mobile money", "Crop yield proxies",
                         "Weather signals", "Market prices"],
        "model_stack": ["Alternative data credit model", "Macro early warning",
                        "Social capital score", "Seasonal stress test"],
        "color": "#4ade80",
        "description": (
            "Agricultural credit uses alternative data (chama membership, mobile money "
            "regularity, SIM age) to score smallholder farmers with no CRB history. "
            "Macro early warning tracks rainfall, inflation, and commodity price signals."
        ),
    },
}


def render():
    st.title("🌍 Industry Simulator")
    st.caption("Reconfigure the full NEXUS platform for any industry with one selector")

    industry = st.session_state.get("active_industry", "🏦 Banking & Fintech")
    cfg = INDUSTRY_CONFIGS.get(industry, INDUSTRY_CONFIGS["🏦 Banking & Fintech"])

    color = cfg["color"]
    st.markdown(f"""
    <div style='background:#222840;border:1px solid {color};border-left:4px solid {color};
                border-radius:0 10px 10px 0;padding:1.2rem 1.5rem;margin-bottom:1.5rem'>
      <div style='font-size:1.2rem;font-weight:700;color:{color};margin-bottom:0.4rem'>
        {industry} — Platform Configuration
      </div>
      <div style='font-size:13px;color:#d0d6e8;line-height:1.6'>{cfg["description"]}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric(cfg["kpi_label"], cfg["kpi_target"])
    c2.metric("Primary Risk", cfg["key_risk"])
    c3.metric("Active Modules", str(len(cfg["modules"])))

    st.divider()
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Active modules")
        for mod in cfg["modules"]:
            st.markdown(f"""
            <div style='padding:6px 10px;background:#1c2128;border-radius:6px;
                        border-left:3px solid {color};margin-bottom:6px;
                        font-size:13px;color:#d0d6e8'>
              {mod}
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Data sources ingested")
        for ds in cfg["data_sources"]:
            st.markdown(f"<div style='font-size:12px;color:#9aa5c0;padding:3px 0'>• {ds}</div>",
                        unsafe_allow_html=True)

    with col_r:
        st.subheader("Model stack")
        for i, model in enumerate(cfg["model_stack"], 1):
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;padding:6px 0;
                        border-bottom:1px solid #2a3050'>
              <span style='font-size:11px;color:{color};font-weight:700;
                           background:{color}22;padding:2px 7px;border-radius:10px'>{i}</span>
              <span style='font-size:13px;color:#d0d6e8'>{model}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Industry comparison — module coverage")
    industries = list(INDUSTRY_CONFIGS.keys())
    all_modules = [
        "Credit Intelligence", "Fraud & Verification", "Portfolio & ESG",
        "ALM & Treasury", "Risk & Early Warning", "Market Intelligence",
        "Customer Analytics"
    ]

    z = []
    for ind in industries:
        row = [1 if m in INDUSTRY_CONFIGS[ind]["modules"] else 0
               for m in all_modules]
        z.append(row)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=all_modules,
        y=[ind.split(" ", 1)[1] for ind in industries],
        colorscale=[[0, "#222840"], [1, "#6ab0ff"]],
        showscale=False,
        text=[[("✓" if v else "") for v in row] for row in z],
        texttemplate="%{text}",
        textfont=dict(size=16, color="#4ade80"),
    ))
    fig.update_layout(
        height=320,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#d0d6e8"),
        xaxis=dict(tickangle=-30),
        margin=dict(l=0, r=0, t=10, b=80)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Run a simulation")
    col1, col2 = st.columns(2)
    with col1:
        port_size  = st.number_input("Portfolio size (KES M)", 10, 50000, 500, step=50)
        avg_pd     = st.slider("Average PD (%)", 1.0, 30.0, 8.0)
        avg_lgd    = st.slider("Average LGD (%)", 20.0, 80.0, 55.0)
    with col2:
        growth_rate = st.slider("Portfolio growth rate (%/yr)", 0.0, 50.0, 15.0)
        stress_pd   = st.slider("Stress scenario PD multiplier", 1.0, 4.0, 1.5)

    if st.button("Run scenario →", type="primary"):
        el = port_size * (avg_pd / 100) * (avg_lgd / 100)
        el_stress = port_size * (avg_pd / 100 * stress_pd) * (avg_lgd / 100)
        port_next = port_size * (1 + growth_rate / 100)
        raroc = ((port_size * 0.12) - el) / (el * 8)

        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Expected Loss", f"KES {el:.1f}M")
        col_b.metric("Stress EL",     f"KES {el_stress:.1f}M",
                     f"+{el_stress - el:.1f}M under stress",
                     delta_color="inverse")
        col_c.metric("Portfolio Y+1", f"KES {port_next:.0f}M")
        col_d.metric("RAROC",         f"{raroc:.1%}")

        years = np.arange(1, 6)
        proj_el = [port_size * (1 + growth_rate / 100) ** (y - 1)
                   * (avg_pd / 100) * (avg_lgd / 100) for y in years]
        proj_el_s = [e * stress_pd for e in proj_el]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=[f"Y{y}" for y in years], y=proj_el,
                              name="Base EL", marker_color="#6ab0ff"))
        fig2.add_trace(go.Bar(x=[f"Y{y}" for y in years], y=proj_el_s,
                              name="Stress EL", marker_color="#f87171",
                              opacity=0.6))
        fig2.update_layout(
            height=280, barmode="overlay",
            xaxis_title="Year", yaxis_title="Expected Loss (KES M)",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d0d6e8"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig2, use_container_width=True)
