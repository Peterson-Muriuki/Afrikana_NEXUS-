# NEXUS — Universal Intelligence Platform

> **Flagship portfolio project** | WorldQuant MScFE Program  
> An integrated financial intelligence platform covering credit risk, portfolio optimization, ALM, fraud detection, customer analytics, and macro early warning — deployable across any industry.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## What NEXUS is

NEXUS consolidates **8 prior portfolio projects** into a single, production-grade Streamlit application. Every module reflects a direct MScFE course connection and targets a real fintech/banking decision.

| Module | Source Project | MScFE Course Connection |
|---|---|---|
| 💳 Credit Intelligence | `kenya-credit-scoring`, `KenyaCreditAI` | Courses 3, 6 — Econometrics, ML |
| 🛡️ Fraud & Verification | `smart-credit-verifier` | Course 6 — ML in Finance |
| 📊 Portfolio & ESG | `esg-portfolio-optimizer` | Courses 4, 5 — Derivatives, Stochastic |
| 🏦 ALM & Treasury | `ALM-Optimization-Engine` | Courses 3, 5 — Econometrics, Stochastic |
| ⚠️ Risk & Early Warning | `K-SIP` | Course 3 — Financial Econometrics (VAR) |
| 📈 Market Intelligence | `quant_risk_engine` | Courses 4, 5 — Derivatives, Stochastic |
| 👥 Customer Analytics | `afrikana-analytics` | Courses 2, 6 — Financial Data, ML |
| 🌍 Industry Simulator | All of the above | End-to-end integration |

---

## Model performance highlights

| Model | Metric | Value |
|---|---|---|
| XGBoost PD (conversion) | ROC-AUC | 0.87+ |
| XGBoost PD (repayment) | Repayment rate | >95% |
| Fraud detection tier-1 | Cost saving vs CRB-all | 60–70% |
| Portfolio optimizer | Sharpe ratio (ESG-constrained) | 0.85+ |
| Churn scorer (GBM) | ROC-AUC | 0.82+ |
| Nelson-Siegel fit | Yield curve R² | >0.99 |

---

## Architecture

```
nexus/
├── app.py                    # Streamlit entry point & routing
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Dark theme configuration
├── core/
│   └── data_engine.py        # Unified synthetic data generation
│                               (credit, fraud, portfolio, ALM,
│                                macro, customer, market)
└── pages/
    ├── home.py               # Platform overview & KPI dashboard
    ├── credit.py             # Credit scoring & EL computation
    ├── fraud.py              # 3-tier verification pipeline
    ├── portfolio.py          # Portfolio optimization & ESG
    ├── alm.py                # ALM, duration gap, NIM sensitivity
    ├── risk_warning.py       # Macro early warning system
    ├── market.py             # Yield curve & market risk
    ├── customer.py           # Churn, LTV/CAC, segmentation
    └── industry_sim.py       # Industry-specific reconfiguration
```

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/nexus.git
cd nexus

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

No API keys required. All data is synthetic and generated at runtime.

---

## Industries supported

| Industry | Primary modules | Key metric |
|---|---|---|
| 🏦 Banking & Fintech | Credit + ALM + Portfolio + Risk | NPL ratio < 5% |
| 📱 Mobility & PAYG | Credit + Customer + Fraud | Repayment rate > 95% |
| ⚡ Energy & EV | Customer + ESG + Risk | Station utilisation > 70% |
| 🏢 Insurance | Fraud + ALM + Customer | Combined ratio < 100% |
| 🛒 Retail Credit | Credit + Fraud + Customer | Approval rate 60–75% |
| 🌾 Agri-Finance | Credit + Risk + Customer | Seasonal default < 8% |

---

## Key technical features

### Credit intelligence
- Dual XGBoost model: **conversion probability** → **repayment risk**
- 30+ alternative data features: mobile money tenure, SIM age, chama membership, transaction consistency
- SMOTE class balancing for imbalanced default datasets
- Full Basel II output: PD, LGD, EAD, Expected Loss, RAROC

### Fraud & verification
- 3-tier cost-optimised pipeline:
  - **Tier 1 (Free):** SIM age, velocity, device value, application hour
  - **Tier 2 (KES 20):** Telco verification, digital footprint
  - **Tier 3 (KES 70):** CRB check — only for borderline cases
- Saves 60–70% on verification costs vs checking everyone with CRB

### Portfolio & ESG
- Markowitz mean-variance optimisation with **ESG score constraint**
- Efficient frontier simulation (1,500 random portfolios)
- Random Forest return predictor using technical features (RSI, MA ratio, volatility)
- ESG decomposition: E / S / G sub-scores per asset

### ALM & treasury
- **Duration gap analysis** — asset vs liability duration
- **NIM sensitivity** across ±300bps rate shock scenarios
- CVXPY-based asset weight optimisation (maximise return − 0.5 × risk)
- LCR, NSFR liquidity ratio computation
- 95% VaR and CVaR via historical simulation

### Market intelligence
- **Nelson-Siegel yield curve** fitted via Nelder-Mead optimisation
- 5 scenario overlays: baseline, rate hike, rate cut, flat, inverted
- Rolling 21-day annualised volatility
- Correlation heatmap across NSE assets
- NLP sentiment proxy (TextBlob)

### Customer analytics
- **Churn scoring** via Gradient Boosting (afrikana-analytics `ChurnScorer`)
- **LTV computation**: survival-adjusted discounted revenue projection
- LTV/CAC ratio by segment with 3x benchmark line
- Geographic distribution across EA markets

### Macro early warning
- **EA Fintech Risk Index** (composite: KES/USD, inflation, CBK rate, GDP, MM volume)
- Alert (60) and critical (75) thresholds
- Regulatory event tracker with severity classification and business impact

---

## Source repositories

This project integrates and extends:

- [`kenya-credit-scoring`](https://github.com/YOUR_USERNAME/kenya-credit-scoring) — Alternative data credit engine for Kenyan digital lenders
- [`KenyaCreditAI`](https://github.com/YOUR_USERNAME/KenyaCreditAI) — Alternative data credit scoring for financial inclusion
- [`smart-credit-verifier`](https://github.com/YOUR_USERNAME/smart-credit-verifier) — 3-tier cost-optimised verification pipeline
- [`quant_risk_engine`](https://github.com/YOUR_USERNAME/quant_risk_engine) — Nelson-Siegel yield curve · VaR · NLP sentiment
- [`esg-portfolio-optimizer`](https://github.com/YOUR_USERNAME/esg-portfolio-optimizer) — Markowitz + ESG constraints + ML return predictor
- [`ALM-Optimization-Engine`](https://github.com/YOUR_USERNAME/ALM-Optimization-Engine) — Duration gap · NIM sensitivity · CVXPY optimisation
- [`K-SIP`](https://github.com/YOUR_USERNAME/K-SIP) — Kenya Strategic Intelligence Platform · EA early warning
- [`afrikana-analytics`](https://github.com/YOUR_USERNAME/afrikana-analytics) — Churn · LTV · demand forecasting for African platforms

---

## LinkedIn positioning

> *Built NEXUS — a unified financial intelligence platform integrating 8 prior portfolio projects into one production-grade Streamlit app. Covers the full fintech stack: credit scoring (XGBoost, alt data), fraud detection (3-tier pipeline), portfolio optimization (Markowitz + ESG), ALM (duration gap, NIM), macro early warning, and customer analytics (churn, LTV). Configurable across 6 industries. Built as part of WorldQuant MScFE Program.*

**Target roles:** Quantitative Analyst · Risk Analyst · Credit Risk Engineer · BI Engineer · Financial Engineer  
**Target companies:** M-Pesa · Equity Bank · Branch International · Pezesha · Standard Bank · Absa Africa · IFC · AfDB

---

## Author

**Peterson Muriuki**  
WorldQuant MScFE Program  
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
