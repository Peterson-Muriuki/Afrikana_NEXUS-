"""NEXUS Home Page"""
import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import (
    generate_loan_applications, generate_customers,
    generate_macro_signals, generate_portfolio_assets
)

def render():
    industry = st.session_state.get("active_industry", "🏦 Banking & Fintech")

    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem'>
      <div class='hero-title'>NEXUS — Universal Intelligence Platform</div>
      <div class='hero-sub'>Integrated credit · risk · portfolio · customer intelligence — across any industry</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Platform KPIs ──────────────────────────────────────────────────────
    if "home_data" not in st.session_state:
        with st.spinner("Initialising platform data..."):
            st.session_state.loan_df    = generate_loan_applications(500)
            st.session_state.cust_df    = generate_customers(800)
            st.session_state.macro_df   = generate_macro_signals(24)
            assets_df, returns_df       = generate_portfolio_assets(12)
            st.session_state.assets_df  = assets_df
            st.session_state.returns_df = returns_df
            st.session_state.home_data  = True

    loan_df  = st.session_state.loan_df
    cust_df  = st.session_state.cust_df
    macro_df = st.session_state.macro_df

    latest_risk = macro_df.iloc[-1]["risk_index"]
    avg_pd       = loan_df["default_probability"].mean()
    avg_score    = loan_df["credit_score"].mean()
    ltv_cac      = cust_df["ltv_cac_ratio"].mean()
    churn        = cust_df["churn_probability"].mean()
    high_risk_pct = (cust_df["risk_band"] == "High").mean() * 100

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("EA Risk Index",     f"{latest_risk:.1f}/100",
              f"{latest_risk - 60:+.1f} vs threshold",
              delta_color="inverse")
    c2.metric("Portfolio Avg PD",  f"{avg_pd*100:.1f}%",
              "Probability of Default")
    c3.metric("Avg Credit Score",  f"{avg_score:.0f}",
              "300–850 scale")
    c4.metric("LTV / CAC",         f"{ltv_cac:.2f}x",
              f"+{ltv_cac-3:.2f} vs 3x target")
    c5.metric("Portfolio Churn",   f"{churn*100:.1f}%",
              delta_color="inverse")
    c6.metric("High-Risk Clients", f"{high_risk_pct:.1f}%",
              delta_color="inverse")

    st.divider()

    # ── Module cards ───────────────────────────────────────────────────────
    st.subheader("Platform modules")
    col_a, col_b, col_c = st.columns(3)

    modules = [
        ("💳", "Credit Intelligence",   "pill-blue",
         "Dual-model scoring (XGBoost) · PD/LGD/EAD · Expected loss · Decision engine",
         ["Banking", "Fintech", "Telco", "Agriculture"]),
        ("🛡️", "Fraud & Verification",  "pill-red",
         "3-tier pipeline · Free signals first · Cost-optimised CRB routing · Fraud flags",
         ["Lending", "Insurance", "E-commerce", "SACCOS"]),
        ("📊", "Portfolio & ESG",        "pill-green",
         "Markowitz optimisation · ESG constraints · Efficient frontier · Risk attribution",
         ["Asset Managers", "Pension Funds", "DFIs", "Wealth"]),
        ("🏦", "ALM & Treasury",         "pill-purple",
         "Duration gap · NIM sensitivity · Liquidity ratios · Rate shock analysis",
         ["Commercial Banks", "Development Banks", "MFIs"]),
        ("⚠️", "Risk & Early Warning",   "pill-amber",
         "EA macro risk index · Regulatory event tracker · Inflation & FX signals",
         ["Any regulated entity"]),
        ("📈", "Market Intelligence",    "pill-blue",
         "Nelson-Siegel yield curve · VaR/CVaR · NLP sentiment · Technical indicators",
         ["Treasury", "Investment", "Research"]),
        ("👥", "Customer Analytics",     "pill-green",
         "Churn scoring · LTV/CAC · Segment profiling · Retention strategy engine",
         ["PAYG", "Subscriptions", "Retail", "Mobility"]),
        ("🌍", "Industry Simulator",     "pill-purple",
         "Reconfigure all models for your sector with one selector",
         ["All industries"]),
    ]

    cols = [col_a, col_b, col_c]
    for i, (icon, title, pill_cls, desc, industries) in enumerate(modules):
        with cols[i % 3]:
            industry_pills = " ".join(
                f"<span class='pill {pill_cls}'>{ind}</span>"
                for ind in industries[:3]
            )
            st.markdown(f"""
            <div class='nexus-card'>
              <h4>{icon} {title}</h4>
              <p style='margin-bottom:0.5rem'>{desc}</p>
              {industry_pills}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── Risk index chart ────────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("EA Macro Risk Index — 24 months")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=macro_df["month"], y=macro_df["risk_index"],
            mode="lines", name="Risk Index",
            line=dict(color="#6ab0ff", width=2),
            fill="tozeroy", fillcolor="rgba(88,166,255,0.08)"
        ))
        fig.add_hline(y=60, line_dash="dash", line_color="#fbbf24",
                      annotation_text="Alert (60)")
        fig.add_hline(y=75, line_dash="dash", line_color="#f87171",
                      annotation_text="Critical (75)")
        fig.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,
            gridcolor="#2a3050"), font=dict(color="#d0d6e8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Credit score distribution")
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(
            x=loan_df["credit_score"], nbinsx=20,
            marker_color="#4ade80", opacity=0.8,
            name="Score"
        ))
        fig2.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,
            gridcolor="#2a3050"), font=dict(color="#d0d6e8"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Source projects ────────────────────────────────────────────────────
    st.subheader("Built from")
    repos = [
        ("kenya-credit-scoring",     "Alternative data credit engine for Kenyan digital lenders"),
        ("KenyaCreditAI",            "RF + social sentiment scoring with alt data"),
        ("smart-credit-verifier",    "3-tier cost-optimised verification pipeline"),
        ("quant_risk_engine",        "Nelson-Siegel yield curve · VaR · NLP sentiment"),
        ("esg-portfolio-optimizer",  "Markowitz + ESG constraints + ML return prediction"),
        ("ALM-Optimization-Engine",  "CVXPY asset optimisation · duration gap · NIM analysis"),
        ("K-SIP",                    "EA macro early warning · competitive intelligence"),
        ("afrikana-analytics",       "Churn · LTV · demand forecasting toolkit"),
    ]
    r1, r2 = st.columns(2)
    for i, (repo, desc) in enumerate(repos):
        col = r1 if i % 2 == 0 else r2
        with col:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:8px;padding:6px 0;
                        border-bottom:1px solid #2a3050'>
              <span style='font-family:monospace;font-size:12px;color:#6ab0ff'>{repo}</span>
              <span style='font-size:12px;color:#9aa5c0'>— {desc}</span>
            </div>
            """, unsafe_allow_html=True)
