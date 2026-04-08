"""ALM & Treasury Module"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_alm_data


def render():
    st.title("🏦 ALM & Treasury")
    st.caption("Duration gap · NIM sensitivity · Liquidity ratios (LCR/NSFR) · Rate shock scenarios")

    if "alm_data" not in st.session_state:
        st.session_state.alm_data = generate_alm_data()
    d = st.session_state.alm_data

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Assets",       f"KES {d['total_assets_M']:.0f}M")
    c2.metric("Total Liabilities",  f"KES {d['total_liabilities_M']:.0f}M")
    c3.metric("Equity",             f"KES {d['equity_M']:.0f}M")
    c4.metric("Duration Gap",       f"{d['duration_gap']:.2f} yrs",
              delta_color="inverse")
    c5.metric("LCR / NSFR",        f"{d['lcr_pct']:.0f}% / {d['nsfr_pct']:.0f}%")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["⚖️ Balance Sheet", "📉 NIM Sensitivity", "🔥 Stress Test"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Asset allocation")
            fig = go.Figure(go.Bar(
                x=d["assets"]["Value_M"],
                y=d["assets"]["Asset"],
                orientation="h",
                marker_color="#6ab0ff",
                text=[f"KES {v}M | {dur}yr | {y}%" for v, dur, y in zip(
                    d["assets"]["Value_M"],
                    d["assets"]["Duration_Years"],
                    d["assets"]["Yield_Pct"]
                )],
                textposition="inside"
            ))
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0),
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#d0d6e8"))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.subheader("Liability structure")
            fig2 = go.Figure(go.Bar(
                x=d["liabilities"]["Value_M"],
                y=d["liabilities"]["Liability"],
                orientation="h",
                marker_color="#f87171",
                text=[f"KES {v}M | {dur}yr | {c}%" for v, dur, c in zip(
                    d["liabilities"]["Value_M"],
                    d["liabilities"]["Duration_Years"],
                    d["liabilities"]["Cost_Pct"]
                )],
                textposition="inside"
            ))
            fig2.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0.5rem'>
          <div style='background:#222840;border:1px solid #2d3347;border-radius:8px;padding:1rem'>
            <div style='font-size:11px;color:#9aa5c0'>Asset duration</div>
            <div style='font-size:1.4rem;font-weight:600;color:#6ab0ff'>{d['asset_duration']} yrs</div>
          </div>
          <div style='background:#222840;border:1px solid #2d3347;border-radius:8px;padding:1rem'>
            <div style='font-size:11px;color:#9aa5c0'>Liability duration</div>
            <div style='font-size:1.4rem;font-weight:600;color:#f87171'>{d['liability_duration']} yrs</div>
          </div>
          <div style='background:#222840;border:1px solid #2d3347;border-radius:8px;padding:1rem'>
            <div style='font-size:11px;color:#9aa5c0'>Duration gap</div>
            <div style='font-size:1.4rem;font-weight:600;color:#fbbf24'>{d['duration_gap']} yrs</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("NIM sensitivity to rate shocks")
        nim_df = d["nim_sensitivity"]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=nim_df["Rate_Shock_Pct"],
            y=nim_df["NIM_Pct"],
            marker_color=[("#f87171" if v < 0 else "#4ade80")
                          if r != 0 else "#6ab0ff"
                          for v, r in zip(nim_df["NIM_Pct"],
                                         nim_df["Rate_Shock_Pct"])],
            text=[f"{v:.2f}%" for v in nim_df["NIM_Pct"]],
            textposition="outside"
        ))
        fig3.update_layout(
            height=320, xaxis_title="Rate shock (bps × 100)",
            yaxis_title="Net Interest Margin (%)",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d0d6e8")
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info(f"⚠️  A +200bps shock reduces NIM from "
                f"{nim_df[nim_df['Rate_Shock_Pct']==0]['NIM_Pct'].values[0]:.2f}% to "
                f"{nim_df[nim_df['Rate_Shock_Pct']==2]['NIM_Pct'].values[0]:.2f}%, "
                f"reflecting the liability-sensitive balance sheet (duration gap = {d['duration_gap']:.2f} yrs).")

    with tab3:
        st.subheader("Portfolio VaR & CVaR")
        c1, c2 = st.columns(2)
        c1.metric("95% VaR (1-day)", f"KES {d['var_95_M']:.2f}M",
                  "Maximum loss at 95% confidence")
        c2.metric("95% CVaR (Expected Shortfall)", f"KES {d['cvar_95_M']:.2f}M",
                  "Average loss beyond VaR")

        confidence = st.slider("Confidence level", 90, 99, 95)
        portfolio_val = d["total_assets_M"]
        sim_rets = np.random.normal(0.0008, 0.012, 2000)
        var_custom = abs(np.percentile(sim_rets, 100 - confidence)) * portfolio_val
        cvar_custom = abs(sim_rets[sim_rets <= np.percentile(sim_rets, 100 - confidence)].mean()) * portfolio_val

        c3, c4 = st.columns(2)
        c3.metric(f"{confidence}% VaR",  f"KES {var_custom:.2f}M")
        c4.metric(f"{confidence}% CVaR", f"KES {cvar_custom:.2f}M")

        fig4 = go.Figure()
        fig4.add_trace(go.Histogram(
            x=sim_rets * portfolio_val * 10, nbinsx=60,
            marker_color="#6ab0ff", opacity=0.7, name="P&L"
        ))
        var_line = -var_custom
        fig4.add_vline(x=var_line, line_color="#fbbf24", line_dash="dash",
                       annotation_text=f"VaR ({confidence}%)")
        fig4.add_vline(x=-cvar_custom, line_color="#f87171", line_dash="dash",
                       annotation_text=f"CVaR")
        fig4.update_layout(
            height=300, xaxis_title="Daily P&L (KES M)",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d0d6e8"), showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)
