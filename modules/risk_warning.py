"""Risk & Early Warning Module"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_macro_signals, generate_regulatory_events


def render():
    st.title("⚠️ Risk & Early Warning")
    st.caption("EA macro risk index · Regulatory event tracker · FX & inflation signals")

    if "macro_df" not in st.session_state:
        st.session_state.macro_df = generate_macro_signals(24)
    if "reg_df" not in st.session_state:
        st.session_state.reg_df = generate_regulatory_events()

    macro_df = st.session_state.macro_df
    reg_df   = st.session_state.reg_df

    latest = macro_df.iloc[-1]
    prev   = macro_df.iloc[-2]

    risk = latest["risk_index"]
    risk_color = "#f87171" if risk > 75 else "#fbbf24" if risk > 60 else "#4ade80"
    risk_label = "CRITICAL" if risk > 75 else "ELEVATED" if risk > 60 else "NORMAL"

    st.markdown(f"""
    <div style='background:#222840;border:2px solid {risk_color};border-radius:10px;
                padding:1rem 1.5rem;margin-bottom:1.2rem;display:flex;
                align-items:center;gap:1.5rem'>
      <div style='font-size:2rem;font-weight:700;color:{risk_color}'>{risk:.1f}</div>
      <div>
        <div style='font-size:0.75rem;color:#9aa5c0'>EA FINTECH RISK INDEX</div>
        <div style='font-weight:600;color:{risk_color}'>{risk_label}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("KES/USD",      f"{latest['kes_usd']:.1f}",
              f"{latest['kes_usd'] - prev['kes_usd']:+.1f}", delta_color="inverse")
    c2.metric("Inflation",    f"{latest['inflation_pct']:.1f}%",
              delta_color="inverse")
    c3.metric("CBK Rate",     f"{latest['cbk_rate_pct']:.2f}%",
              delta_color="inverse")
    c4.metric("GDP Growth",   f"{latest['gdp_growth_pct']:.1f}%")
    c5.metric("MM Vol (Bn)",  f"KES {latest['mobile_money_vol_bn']:.0f}B",
              f"{latest['mobile_money_vol_bn'] - prev['mobile_money_vol_bn']:+.0f}")

    st.divider()

    tab1, tab2 = st.tabs(["📈 Macro Dashboard", "📋 Regulatory Events"])

    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("Risk index — 24 months")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=macro_df["month"], y=macro_df["risk_index"],
                fill="tozeroy", fillcolor="rgba(248,81,73,0.1)",
                line=dict(color="#f87171", width=2), name="Risk Index"
            ))
            fig.add_hline(y=60, line_dash="dash", line_color="#fbbf24",
                          annotation_text="Alert (60)")
            fig.add_hline(y=75, line_dash="dash", line_color="#f87171",
                          annotation_text="Critical (75)")
            fig.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=0),
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#d0d6e8"),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.subheader("KES/USD — 24 months")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=macro_df["month"], y=macro_df["kes_usd"],
                line=dict(color="#fbbf24", width=2), name="KES/USD"
            ))
            fig2.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=0),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Inflation vs CBK Rate")
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=macro_df["month"],
                                      y=macro_df["inflation_pct"],
                                      name="Inflation",
                                      line=dict(color="#f87171", width=1.5)))
            fig3.add_trace(go.Scatter(x=macro_df["month"],
                                      y=macro_df["cbk_rate_pct"],
                                      name="CBK Rate",
                                      line=dict(color="#6ab0ff", width=1.5)))
            fig3.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.subheader("GDP Growth trend")
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=macro_df["month"],
                                      y=macro_df["gdp_growth_pct"],
                                      fill="tozeroy",
                                      fillcolor="rgba(63,185,80,0.1)",
                                      line=dict(color="#4ade80", width=1.5)))
            fig4.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        st.subheader("Regulatory & macro event tracker")
        sev_colors = {"High": "#f87171", "Medium": "#fbbf24",
                      "Low": "#4ade80", "Opportunity": "#6ab0ff"}

        for _, row in reg_df.iterrows():
            col = sev_colors.get(row["severity"], "#9aa5c0")
            cat_map = {
                "Monetary": "🏦", "FX": "💱", "Regulation": "📜",
                "Tax": "💰", "Opportunity": "🌱", "Credit": "💳"
            }
            icon = cat_map.get(row["category"], "⚠️")
            st.markdown(f"""
            <div style='border-left:3px solid {col};padding:0.6rem 0.8rem;
                        margin-bottom:0.6rem;background:#222840;border-radius:0 6px 6px 0'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span style='font-size:12px;color:{col};font-weight:600'>{icon} {row["category"]} · {row["severity"]}</span>
                <span style='font-size:11px;color:#9aa5c0'>{row["date"].strftime("%b %Y")}</span>
              </div>
              <div style='font-size:13px;color:#e8edf8;margin-top:3px'>{row["event"]}</div>
              <div style='font-size:12px;color:#9aa5c0;margin-top:2px'>→ {row["impact"]}</div>
            </div>
            """, unsafe_allow_html=True)
