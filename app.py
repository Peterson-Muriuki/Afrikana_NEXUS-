"""
NEXUS — Universal Intelligence Platform
========================================
Flagship integration of all prior portfolio projects.
Covers: Credit Risk · Portfolio Optimization · ALM · ESG · Fraud Detection
        Customer Intelligence · Market Risk · Early Warning · Forecasting

Industries: Fintech · Banking · Insurance · Mobility · Energy · Real Estate
"""

import streamlit as st

st.set_page_config(
    page_title="NEXUS — Universal Intelligence Platform",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling — lighter charcoal theme ──────────────────────────────────────
st.markdown("""
<style>
/* Main background — soft dark charcoal, not pitch black */
.stApp {
    background-color: #1a1f2e;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #141824;
    border-right: 1px solid #2d3347;
}
[data-testid="stSidebar"] * { color: #d0d6e8 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 13px !important; }

/* Main content area */
section[data-testid="stMainBlockContainer"] {
    background-color: #1a1f2e;
}

/* Cards */
.nexus-card {
    background: #222840;
    border: 1px solid #2d3347;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.nexus-card h4 { color: #6ab0ff; margin: 0 0 0.3rem; }
.nexus-card p  { color: #9aa5c0; font-size: 13px; margin: 0; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #222840;
    border: 1px solid #2d3347;
    border-radius: 8px;
    padding: 0.8rem 1rem;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    background: #222840;
}

/* Pills */
.pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
}
.pill-blue   { background: #1f4f8a44; color: #6ab0ff; border: 1px solid #2563ab; }
.pill-green  { background: #1a4d2e44; color: #4ade80; border: 1px solid #22863a; }
.pill-amber  { background: #5c3a0044; color: #fbbf24; border: 1px solid #8a5c00; }
.pill-red    { background: #5c1a1a44; color: #f87171; border: 1px solid #8a2020; }
.pill-purple { background: #3d1a6e44; color: #c084fc; border: 1px solid #6e3aab; }

/* Hero */
.hero-title { font-size: 2.2rem; font-weight: 700; color: #e8edf8; line-height: 1.2; }
.hero-sub   { font-size: 1.1rem; color: #9aa5c0; margin-top: 0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── Page map — label → (module_key, import_name) ──────────────────────────
PAGE_OPTIONS = [
    ("🏠 Home",                 "home"),
    ("💳 Credit Intelligence",  "credit"),
    ("🛡️ Fraud & Verification", "fraud"),
    ("📊 Portfolio & ESG",      "portfolio"),
    ("🏦 ALM & Treasury",       "alm"),
    ("⚠️ Risk & Early Warning",  "risk_warning"),
    ("📈 Market Intelligence",   "market"),
    ("👥 Customer Analytics",    "customer"),
    ("🌍 Industry Simulator",    "industry_sim"),
]
LABELS     = [label for label, _ in PAGE_OPTIONS]
MODULE_MAP = {label: mod for label, mod in PAGE_OPTIONS}

# ── Sidebar navigation ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔷 NEXUS")
    st.markdown("<small style='color:#9aa5c0'>Universal Intelligence Platform</small>",
                unsafe_allow_html=True)
    st.divider()

    selected_label = st.radio(
        "Navigate",
        options=LABELS,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("<small style='color:#9aa5c0'>Industry context</small>",
                unsafe_allow_html=True)
    industry = st.selectbox(
        "Active industry",
        ["🏦 Banking & Fintech", "📱 Mobility & PAYG", "⚡ Energy & EV",
         "🏢 Insurance", "🛒 Retail Credit", "🌾 Agri-Finance"],
        label_visibility="collapsed",
    )
    st.session_state["active_industry"] = industry
    st.markdown(
        f"<div style='font-size:11px;color:#4ade80;margin-top:4px'>Active: {industry}</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("<small style='color:#9aa5c0'>v1.0 · WorldQuant MScFE Portfolio</small>",
                unsafe_allow_html=True)

# ── Page routing — clean dict lookup, no string splitting ─────────────────
module_name = MODULE_MAP[selected_label]

if module_name == "home":
    from modules import home;         home.render()
elif module_name == "credit":
    from modules import credit;       credit.render()
elif module_name == "fraud":
    from modules import fraud;        fraud.render()
elif module_name == "portfolio":
    from modules import portfolio;    portfolio.render()
elif module_name == "alm":
    from modules import alm;          alm.render()
elif module_name == "risk_warning":
    from modules import risk_warning; risk_warning.render()
elif module_name == "market":
    from modules import market;       market.render()
elif module_name == "customer":
    from modules import customer;     customer.render()
elif module_name == "industry_sim":
    from modules import industry_sim; industry_sim.render()
