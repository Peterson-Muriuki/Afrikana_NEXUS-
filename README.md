# Afrikana-NEXUS - Universal Intelligence Platform

> **Flagship portfolio project** | MScFE   
> An integrated financial intelligence platform covering credit risk, portfolio optimization, ALM, fraud detection, customer analytics, and macro early warning - deployable across any industry.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## What NEXUS is

Afrikana-NEXUS consolidates **8 prior portfolio projects** into a single, production-grade Streamlit application. Every module reflects a direct MScFE connection and targets a real fintech/banking decision.

| Module | Source Project | MScFE |
|---|---|---|
| Credit Intelligence | `kenya-credit-scoring`, `KenyaCreditAI` | Econometrics, ML |
| Fraud & Verification | `smart-credit-verifier` | ML in Finance |
| Portfolio & ESG | `esg-portfolio-optimizer` | Derivatives, Stochastic |
| ALM & Treasury | `ALM-Optimization-Engine` | Econometrics, Stochastic |
| Risk & Early Warning | `K-SIP` | Financial Econometrics (VAR) |
| Market Intelligence | `quant_risk_engine` | Derivatives, Stochastic |
| Customer Analytics | `afrikana-analytics` | Financial Data, ML |
| Industry Simulator | All of the above | End-to-end integration |

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
├── app.py                    
├── requirements.txt
├── .streamlit/
│   └── config.toml          
├── core/
│   └── data_engine.py        
│                               
│                                
└── pages/
    ├── home.py               
    ├── credit.py             
    ├── fraud.py             
    ├── portfolio.py         
    ├── alm.py                
    ├── risk_warning.py       
    ├── market.py             
    ├── customer.py          
    └── industry_sim.py       
```

## Quickstart

```bash

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

No API keys required. All data is synthetic and generated at runtime.

---

## Industries supported

| Industry | Primary modules | Key metric |
|---|---|---|
| Banking & Fintech | Credit + ALM + Portfolio + Risk | NPL ratio < 5% |
| Mobility & PAYG | Credit + Customer + Fraud | Repayment rate > 95% |
| Energy & EV | Customer + ESG + Risk | Station utilisation > 70% |
| Insurance | Fraud + ALM + Customer | Combined ratio < 100% |
| Retail Credit | Credit + Fraud + Customer | Approval rate 60–75% |
| Agri-Finance | Credit + Risk + Customer | Seasonal default < 8% |

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
  - **Tier 3 (KES 70):** CRB check - only for borderline cases
- Saves 60-70% on verification costs vs checking everyone with CRB

### Portfolio & ESG
- Markowitz mean-variance optimisation with **ESG score constraint**
- Efficient frontier simulation (1,500 random portfolios)
- Random Forest return predictor using technical features (RSI, MA ratio, volatility)
- ESG decomposition: E / S / G sub-scores per asset

### ALM & treasury
- **Duration gap analysis** - asset vs liability duration
- **NIM sensitivity** across ±300bps rate shock scenarios
- CVXPY-based asset weight optimisation (maximise return - 0.5 × risk)
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

- [`kenya-credit-scoring`](https://github.com/Peterson-Muriuki/kenya-credit-scoring) - Alternative data credit engine for Kenyan digital lenders
- [`KenyaCreditAI`](https://github.com/Peterson-Muriuki/KenyaCreditAI) - Alternative data credit scoring for financial inclusion
- [`smart-credit-verifier`](https://github.com/Peterson-Muriuki/smart-credit-verifier) - 3-tier cost-optimised verification pipeline
- [`quant_risk_engine`](https://github.com/Peterson-Muriuki/quant_risk_engine) - Nelson-Siegel yield curve · VaR · NLP sentiment
- [`esg-portfolio-optimizer`](https://github.com/Peterson-Muriuki/esg-portfolio-optimizer) - Markowitz + ESG constraints + ML return predictor
- [`ALM-Optimization-Engine`](https://github.com/Peterson-Muriuki/ALM-Optimization-Engine) - Duration gap · NIM sensitivity · CVXPY optimisation
- [`K-SIP`](https://github.com/Peterson-Muriuki/K-SIP) - Kenya Strategic Intelligence Platform · EA early warning
- [`afrikana-analytics`](https://github.com/Peterson-Muriuki/afrikana-analytics) - Churn · LTV · demand forecasting for African platforms

---

## Author

**Peterson Muriuki**  
WorldQuant MScFE Program  
[GitHub](https://github.com/Peterson-Muriuki) · [LinkedIn](https://www.linkedin.com/in/peterson-muriuki-5857aaa9/))
