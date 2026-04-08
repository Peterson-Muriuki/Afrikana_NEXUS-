"""Market Intelligence Module"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.data_engine import generate_yield_curve, generate_market_returns


def render():
    st.title("📈 Market Intelligence")
    st.caption("Nelson-Siegel yield curve · VaR/CVaR · Volatility · Correlation · Sentiment")

    if "market_rets" not in st.session_state:
        st.session_state.market_rets = generate_market_returns(504)
    rets = st.session_state.market_rets

    tab1, tab2, tab3 = st.tabs(["📉 Yield Curve", "📊 Market Risk", "🔗 Correlations"])

    with tab1:
        st.subheader("Nelson-Siegel yield curve scenarios")
        scenarios = ["baseline", "rate_hike", "rate_cut", "flat", "inverted"]
        colors    = ["#6ab0ff", "#f87171", "#4ade80", "#fbbf24", "#c084fc"]

        fig = go.Figure()
        for scen, col in zip(scenarios, colors):
            yc = generate_yield_curve(scen)
            fig.add_trace(go.Scatter(
                x=yc["maturity"], y=yc["yield_pct"],
                name=scen.replace("_", " ").title(),
                line=dict(color=col, width=2),
                mode="lines+markers"
            ))
        fig.update_layout(
            height=360, xaxis_title="Maturity (years)",
            yaxis_title="Yield (%)",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d0d6e8"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig, use_container_width=True)

        active_scen = st.selectbox("Select scenario", scenarios,
                                   format_func=lambda s: s.replace("_", " ").title())
        yc = generate_yield_curve(active_scen)
        st.dataframe(yc.rename(columns={"maturity": "Maturity (yrs)",
                                        "yield_pct": "Yield (%)"}),
                     use_container_width=True)

    with tab2:
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("Rolling volatility (21-day)")
            vol_df = rets.rolling(21).std() * np.sqrt(252) * 100
            fig2 = go.Figure()
            for ticker, col in zip(rets.columns, ["#6ab0ff", "#4ade80", "#f87171",
                                                   "#fbbf24", "#c084fc"]):
                fig2.add_trace(go.Scatter(
                    x=vol_df.index, y=vol_df[ticker],
                    name=ticker, line=dict(color=col, width=1.2)
                ))
            fig2.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0),
                               plot_bgcolor="rgba(0,0,0,0)",
                               paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#d0d6e8"),
                               legend=dict(bgcolor="rgba(0,0,0,0)"),
                               yaxis_title="Annualised Vol (%)")
            st.plotly_chart(fig2, use_container_width=True)

        with col_r:
            st.subheader("VaR / CVaR summary")
            summary = []
            for ticker in rets.columns:
                r = rets[ticker]
                vol = r.std() * np.sqrt(252) * 100
                var95 = np.percentile(r, 5) * 100
                cvar95 = r[r <= np.percentile(r, 5)].mean() * 100
                summary.append({
                    "Ticker": ticker,
                    "Ann. Vol (%)": round(vol, 2),
                    "1d VaR 95% (%)": round(var95, 3),
                    "1d CVaR 95% (%)": round(cvar95, 3),
                })
            st.dataframe(pd.DataFrame(summary), use_container_width=True, height=320)

        # Return distribution
        st.subheader("Return distribution — NSE20")
        nse_rets = rets["NSE20"]
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(
            x=nse_rets * 100, nbinsx=50,
            marker_color="#6ab0ff", opacity=0.75, name="Daily returns"
        ))
        var95_nse = np.percentile(nse_rets, 5) * 100
        fig3.add_vline(x=var95_nse, line_color="#f87171", line_dash="dash",
                       annotation_text="95% VaR")
        fig3.update_layout(height=280, xaxis_title="Daily Return (%)",
                           plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("Return correlation matrix")
        corr = rets.corr()
        fig4 = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale="RdBu", zmid=0,
            text=corr.round(2).values,
            texttemplate="%{text}",
            colorbar=dict(title="Corr")
        ))
        fig4.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#d0d6e8"))
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("Market sentiment (TextBlob NLP proxy)")
        tickers = list(rets.columns)
        sentiments = {
            "NSE20":  ("Bullish", 0.22,  "#4ade80"),
            "SAFCOM": ("Bullish", 0.31,  "#4ade80"),
            "KCB":    ("Neutral", 0.05,  "#fbbf24"),
            "EQUITY": ("Bullish", 0.18,  "#4ade80"),
            "EABL":   ("Bearish", -0.12, "#f87171"),
        }
        cols = st.columns(5)
        for i, (ticker, (label, score, color)) in enumerate(sentiments.items()):
            with cols[i]:
                st.markdown(f"""
                <div style='text-align:center;background:#222840;border:1px solid #2d3347;
                            border-radius:8px;padding:0.7rem'>
                  <div style='font-size:12px;color:#9aa5c0'>{ticker}</div>
                  <div style='font-size:1rem;font-weight:600;color:{color}'>{label}</div>
                  <div style='font-size:11px;color:#9aa5c0'>{score:+.2f}</div>
                </div>
                """, unsafe_allow_html=True)
