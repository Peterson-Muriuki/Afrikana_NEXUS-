"""
NEXUS Core Data Engine
=======================
Generates realistic synthetic data for all platform modules.
No external API keys required — fully self-contained demo.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

RNG = np.random.default_rng(42)
random.seed(42)

# ── Credit Intelligence ────────────────────────────────────────────────────

def generate_loan_applications(n=500):
    """Generate realistic loan application dataset."""
    ages = RNG.integers(22, 65, n)
    incomes = RNG.lognormal(10.5, 0.6, n).astype(int)
    loan_amounts = RNG.lognormal(10.2, 0.8, n).astype(int)
    loan_amounts = np.clip(loan_amounts, 5_000, 2_000_000)

    mm_tenure = RNG.integers(0, 60, n)
    mm_txn_freq = RNG.integers(1, 80, n)
    sim_age = RNG.integers(1, 72, n)
    chama = RNG.choice([0, 1], n, p=[0.55, 0.45])
    crb_score = np.where(RNG.random(n) > 0.35,
                         RNG.integers(300, 700, n), 0)
    has_crb = (crb_score > 0).astype(int)

    dti = loan_amounts / (incomes * 12)
    mm_score = (mm_tenure / 60) * 0.4 + (mm_txn_freq / 80) * 0.3 + (sim_age / 72) * 0.3
    social = chama * 0.5 + RNG.random(n) * 0.5

    default_prob = (
        0.05
        + 0.15 * (dti > 0.5).astype(float)
        - 0.10 * mm_score
        - 0.08 * social
        + 0.12 * (has_crb == 0).astype(float)
        + 0.07 * (ages < 25).astype(float)
        + RNG.normal(0, 0.05, n)
    )
    default_prob = np.clip(default_prob, 0.01, 0.95)
    defaulted = RNG.random(n) < default_prob

    employment_types = RNG.choice(
        ["Employed", "Self-employed", "Informal", "Student", "Unemployed"],
        n, p=[0.30, 0.35, 0.25, 0.06, 0.04]
    )
    loan_purposes = RNG.choice(
        ["Business", "Education", "Medical", "Agricultural", "Consumer", "Housing"],
        n, p=[0.30, 0.15, 0.10, 0.20, 0.15, 0.10]
    )
    genders = RNG.choice(["Male", "Female"], n, p=[0.52, 0.48])
    counties = RNG.choice(
        ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Machakos", "Kitale"],
        n, p=[0.30, 0.12, 0.10, 0.10, 0.08, 0.10, 0.10, 0.10]
    )

    credit_score = (
        600
        - 80 * default_prob
        + 0.5 * mm_score * 100
        + RNG.normal(0, 15, n)
    ).astype(int)
    credit_score = np.clip(credit_score, 300, 850)

    df = pd.DataFrame({
        "app_id": [f"APP{str(i).zfill(5)}" for i in range(n)],
        "age": ages,
        "gender": genders,
        "county": counties,
        "employment_type": employment_types,
        "loan_purpose": loan_purposes,
        "monthly_income": incomes,
        "loan_amount": loan_amounts,
        "loan_term_months": RNG.choice([3, 6, 12, 18, 24], n),
        "dti_ratio": dti.round(3),
        "mm_tenure_months": mm_tenure,
        "mm_txn_frequency": mm_txn_freq,
        "sim_age_months": sim_age,
        "in_chama": chama,
        "has_crb": has_crb,
        "crb_score": crb_score,
        "mm_score": mm_score.round(3),
        "social_score": social.round(3),
        "credit_score": credit_score,
        "default_probability": default_prob.round(4),
        "defaulted": defaulted.astype(int),
    })
    return df


def score_single_applicant(app: dict) -> dict:
    """Score a single applicant and return detailed breakdown."""
    income = app.get("monthly_income", 30000)
    loan = app.get("loan_amount", 50000)
    mm_tenure = app.get("mm_tenure_months", 12)
    mm_freq = app.get("mm_txn_frequency", 20)
    sim_age = app.get("sim_age_months", 18)
    chama = app.get("in_chama", 0)
    crb = app.get("crb_score", 0)
    age = app.get("age", 30)

    dti = loan / (income * 12 + 1)
    mm = (mm_tenure / 60) * 0.4 + (mm_freq / 80) * 0.3 + (sim_age / 72) * 0.3
    social = chama * 0.5 + 0.3

    pd_score = max(0.02, min(0.95,
        0.05 + 0.15 * (dti > 0.5) - 0.10 * mm - 0.08 * social
        + 0.12 * (crb == 0) + 0.07 * (age < 25)
    ))

    lgd = 0.45 if dti < 0.3 else (0.60 if dti < 0.5 else 0.75)
    ead = loan
    el = pd_score * lgd * ead

    score = int(850 - pd_score * 350 + mm * 50 + social * 30)
    score = max(300, min(850, score))

    grade = ("A" if score >= 750 else "B" if score >= 680 else
             "C" if score >= 620 else "D" if score >= 560 else "E")

    decision = ("APPROVE" if pd_score < 0.08 else
                 "REFER" if pd_score < 0.20 else "DECLINE")

    return {
        "credit_score": score, "grade": grade, "decision": decision,
        "pd": round(pd_score, 4), "lgd": round(lgd, 4),
        "ead": ead, "expected_loss": round(el, 2),
        "mm_score": round(mm, 3), "social_score": round(social, 3),
        "dti_ratio": round(dti, 3),
    }


# ── Fraud Detection ────────────────────────────────────────────────────────

def generate_fraud_applications(n=300):
    """Tiered verification pipeline data."""
    sim_age = RNG.integers(0, 72, n)
    apps_24h = RNG.integers(0, 8, n)
    completion_sec = RNG.integers(30, 600, n)
    app_hour = RNG.integers(0, 24, n)
    device_value = RNG.integers(3000, 80000, n)
    has_mm = (RNG.random(n) > 0.2).astype(int)
    line_type = RNG.choice(["prepaid", "postpaid"], n, p=[0.75, 0.25])
    loan_amounts = RNG.integers(500, 100000, n)

    fraud_score = (
        0.30 * (sim_age < 1).astype(float)
        + 0.40 * (apps_24h > 2).astype(float)
        + 0.15 * (completion_sec < 120).astype(float)
        + 0.10 * ((app_hour < 6) | (app_hour > 22)).astype(float)
        + 0.15 * (device_value < 5000).astype(float)
    ) * 100

    tier1_score = (
        50
        + 15 * (sim_age >= 24).astype(float)
        + 10 * (device_value >= 40000).astype(float)
        + 12 * (line_type == "postpaid").astype(float)
        + 10 * has_mm
        + RNG.normal(0, 5, n)
    )

    paths = []
    costs = []
    decisions = []
    for i in range(n):
        if fraud_score[i] > 60:
            paths.append("TIER1_FRAUD_REJECT")
            costs.append(0)
            decisions.append("REJECT")
        elif tier1_score[i] >= 75:
            paths.append("TIER1_APPROVE")
            costs.append(0)
            decisions.append("APPROVE")
        elif tier1_score[i] < 30:
            paths.append("TIER1_REJECT")
            costs.append(0)
            decisions.append("REJECT")
        elif tier1_score[i] >= 55:
            paths.append("TIER2_APPROVE")
            costs.append(20)
            decisions.append("APPROVE")
        else:
            paths.append("TIER3_CRB")
            costs.append(70)
            decisions.append(RNG.choice(["APPROVE", "REJECT"]))

    return pd.DataFrame({
        "app_id": [f"FR{str(i).zfill(4)}" for i in range(n)],
        "loan_amount": loan_amounts,
        "sim_age_months": sim_age,
        "apps_last_24h": apps_24h,
        "completion_seconds": completion_sec,
        "app_hour": app_hour,
        "device_value_ksh": device_value,
        "has_mobile_money": has_mm,
        "line_type": line_type,
        "fraud_score": fraud_score.round(1),
        "tier1_risk_score": tier1_score.round(1),
        "verification_path": paths,
        "verification_cost_ksh": costs,
        "decision": decisions,
    })


# ── Portfolio & ESG ────────────────────────────────────────────────────────

def generate_portfolio_assets(n_assets=12):
    """Multi-asset portfolio with ESG scores."""
    tickers = [
        "KCB", "Equity", "Safaricom", "EABL", "BAT-K",
        "ABSA-K", "NCBA", "DTB", "Coop", "Stanbic",
        "ARM", "Bamburi"
    ][:n_assets]

    sectors = [
        "Banking", "Banking", "Telecom", "Consumer", "Consumer",
        "Banking", "Banking", "Banking", "Banking", "Banking",
        "Materials", "Materials"
    ][:n_assets]

    expected_returns = RNG.uniform(0.06, 0.18, n_assets)
    volatilities     = RNG.uniform(0.12, 0.35, n_assets)
    esg_scores       = RNG.integers(38, 88, n_assets)
    e_scores         = (esg_scores + RNG.integers(-10, 10, n_assets)).clip(20, 95)
    s_scores         = (esg_scores + RNG.integers(-8, 12, n_assets)).clip(25, 95)
    g_scores         = (esg_scores + RNG.integers(-6, 14, n_assets)).clip(30, 95)
    market_caps_bn   = RNG.uniform(2, 120, n_assets)

    # Correlation matrix
    corr = np.eye(n_assets)
    for i in range(n_assets):
        for j in range(i + 1, n_assets):
            c = 0.45 if sectors[i] == sectors[j] else 0.20
            c += RNG.uniform(-0.10, 0.10)
            corr[i, j] = corr[j, i] = np.clip(c, -0.1, 0.9)

    cov = np.outer(volatilities, volatilities) * corr

    # Simulate 252 days of returns
    returns_sim = RNG.multivariate_normal(
        expected_returns / 252, cov / 252, 252
    )
    returns_df = pd.DataFrame(returns_sim, columns=tickers)
    dates = pd.bdate_range(end=datetime.today(), periods=252)
    returns_df.index = dates

    assets_df = pd.DataFrame({
        "ticker": tickers,
        "sector": sectors,
        "expected_return": expected_returns.round(4),
        "volatility": volatilities.round(4),
        "esg_score": esg_scores,
        "e_score": e_scores,
        "s_score": s_scores,
        "g_score": g_scores,
        "market_cap_bn": market_caps_bn.round(1),
    })

    return assets_df, returns_df


def optimize_portfolio(assets_df, returns_df, esg_min=50, max_weight=0.30):
    """Simple mean-variance optimization with ESG constraint."""
    tickers = assets_df["ticker"].tolist()
    n = len(tickers)
    mu = assets_df["expected_return"].values
    cov = returns_df.cov().values * 252
    esg = assets_df["esg_score"].values

    from scipy.optimize import minimize

    def neg_sharpe(w):
        ret = w @ mu
        vol = np.sqrt(w @ cov @ w)
        return -ret / (vol + 1e-9)

    constraints = [
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        {"type": "ineq", "fun": lambda w: w @ esg - esg_min},
    ]
    bounds = [(0, max_weight)] * n
    w0 = np.ones(n) / n

    result = minimize(neg_sharpe, w0, method="SLSQP",
                      bounds=bounds, constraints=constraints,
                      options={"maxiter": 500})

    w = result.x if result.success else w0
    w = np.maximum(w, 0)
    w /= w.sum()

    port_ret = w @ mu
    port_vol = np.sqrt(w @ cov @ w)
    port_esg = w @ esg
    sharpe = port_ret / (port_vol + 1e-9)

    return {
        "weights": dict(zip(tickers, w.round(4))),
        "expected_return": round(port_ret, 4),
        "volatility": round(port_vol, 4),
        "sharpe_ratio": round(sharpe, 3),
        "esg_score": round(port_esg, 1),
    }


# ── ALM ───────────────────────────────────────────────────────────────────

def generate_alm_data():
    """Balance sheet items for ALM analysis."""
    assets = pd.DataFrame({
        "Asset": ["Government Bonds", "Corporate Bonds", "Mortgages",
                  "Personal Loans", "Cash & Equivalents", "Equities"],
        "Value_M": [450, 280, 320, 190, 85, 75],
        "Duration_Years": [4.2, 3.1, 7.8, 2.5, 0.1, 6.0],
        "Yield_Pct": [10.5, 12.8, 14.2, 18.5, 9.0, 11.2],
        "Rating": ["AAA", "A", "AA", "BBB", "AAA", "B"],
        "Liquidity": ["High", "Medium", "Low", "Medium", "High", "Medium"],
    })

    liabilities = pd.DataFrame({
        "Liability": ["Demand Deposits", "Fixed Deposits", "Savings Accounts",
                      "Borrowed Funds", "Subordinated Debt"],
        "Value_M": [380, 420, 210, 150, 80],
        "Duration_Years": [0.3, 1.8, 0.8, 3.5, 6.2],
        "Cost_Pct": [3.5, 9.8, 6.2, 11.5, 13.0],
        "Repricing": ["Overnight", "Fixed", "Variable", "Fixed", "Fixed"],
    })

    total_assets = assets["Value_M"].sum()
    total_liab   = liabilities["Value_M"].sum()
    equity       = total_assets - total_liab

    asset_dur = (assets["Value_M"] * assets["Duration_Years"]).sum() / total_assets
    liab_dur  = (liabilities["Value_M"] * liabilities["Duration_Years"]).sum() / total_liab
    dur_gap   = asset_dur - liab_dur

    nim_data = []
    for drate in np.arange(-3, 4, 1):
        asset_yield = assets["Yield_Pct"].mean() + drate * 0.4
        liab_cost   = liabilities["Cost_Pct"].mean() + drate * 0.6
        nim         = asset_yield - liab_cost
        nim_data.append({"Rate_Shock_Pct": drate, "NIM_Pct": round(nim, 2)})

    nim_sensitivity = pd.DataFrame(nim_data)

    var_returns = RNG.normal(0.0008, 0.012, 500)
    var_95 = float(np.percentile(var_returns, 5)) * total_assets
    cvar_95 = float(var_returns[var_returns <= np.percentile(var_returns, 5)].mean()) * total_assets

    return {
        "assets": assets,
        "liabilities": liabilities,
        "total_assets_M": round(total_assets, 1),
        "total_liabilities_M": round(total_liab, 1),
        "equity_M": round(equity, 1),
        "asset_duration": round(asset_dur, 2),
        "liability_duration": round(liab_dur, 2),
        "duration_gap": round(dur_gap, 2),
        "nim_sensitivity": nim_sensitivity,
        "var_95_M": round(abs(var_95), 2),
        "cvar_95_M": round(abs(cvar_95), 2),
        "lcr_pct": round(RNG.uniform(118, 145), 1),
        "nsfr_pct": round(RNG.uniform(108, 128), 1),
    }


# ── Macro Risk & Early Warning ─────────────────────────────────────────────

def generate_macro_signals(months=24):
    """EA macro risk time series."""
    dates = pd.date_range(end=datetime.today(), periods=months + 1, freq="MS")[:months]

    base_risk = 55.0
    kes_usd   = 128.0
    inflation  = 6.8
    cbk_rate   = 13.0
    gdp_growth = 5.2

    risk_index, kes_series, inf_series = [], [], []
    cbk_series, gdp_series, mm_vol_series = [], [], []

    for i in range(months):
        base_risk  = float(np.clip(base_risk  + float(RNG.normal(0, 3)),    30, 90))
        kes_usd    = float(np.clip(kes_usd    + float(RNG.normal(0.8, 1.5)),110, 160))
        inflation  = float(np.clip(inflation  + float(RNG.normal(-0.1, 0.4)),3, 12))
        cbk_rate   = float(np.clip(cbk_rate   + float(RNG.normal(-0.05, 0.15)),9, 16))
        gdp_growth = float(np.clip(gdp_growth + float(RNG.normal(0, 0.3)),  2, 8))
        mm_vol     = 650 + i * 8 + float(RNG.normal(0, 20))

        risk_index.append(round(base_risk, 1))
        kes_series.append(round(kes_usd, 1))
        inf_series.append(round(inflation, 1))
        cbk_series.append(round(cbk_rate, 2))
        gdp_series.append(round(gdp_growth, 1))
        mm_vol_series.append(round(mm_vol, 0))

    df = pd.DataFrame({
        "month":               list(dates),
        "risk_index":          risk_index,
        "kes_usd":             kes_series,
        "inflation_pct":       inf_series,
        "cbk_rate_pct":        cbk_series,
        "gdp_growth_pct":      gdp_series,
        "mobile_money_vol_bn": mm_vol_series,
    })
    return df


def generate_regulatory_events():
    events = [
        {"date": "2025-03", "category": "Monetary", "severity": "High",
         "event": "CBK raises benchmark rate by 75bps to 13.0%",
         "impact": "Increased cost of credit; PAYG collections pressure"},
        {"date": "2025-01", "category": "FX", "severity": "High",
         "event": "KES depreciates to 138/USD — 8% decline in 60 days",
         "impact": "Import cost inflation; dollar-denominated debt burden"},
        {"date": "2024-11", "category": "Regulation", "severity": "Medium",
         "event": "CBK Digital Credit Provider framework — Phase 2 rollout",
         "impact": "Licensing cost increase; compliance reporting requirements"},
        {"date": "2024-09", "category": "Tax", "severity": "Medium",
         "event": "Finance Act 2024: Excise duty on mobile money transactions +5%",
         "impact": "Transaction cost pass-through risk; volume sensitivity"},
        {"date": "2024-07", "category": "Opportunity", "severity": "Low",
         "event": "Solar import duty removed for off-grid equipment",
         "impact": "~10% hardware cost reduction for PAYG solar players"},
        {"date": "2024-05", "category": "Credit", "severity": "Medium",
         "event": "CRB alternative data pilot — PAYG repayment data accepted",
         "impact": "New credit signal source; competitive advantage window"},
    ]
    df = pd.DataFrame(events)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False).reset_index(drop=True)


# ── Customer Analytics ─────────────────────────────────────────────────────

def generate_customers(n=800):
    """PAYG/fintech customer base with churn and LTV."""
    segments = RNG.choice(
        ["Premium", "Mass Market", "Emerging", "Agricultural", "Youth"],
        n, p=[0.15, 0.35, 0.25, 0.15, 0.10]
    )
    tenure = RNG.integers(1, 48, n)
    rev_map = {"Premium": 4500, "Mass Market": 1800, "Emerging": 900,
               "Agricultural": 1200, "Youth": 600}
    base_rev = np.array([rev_map[s] for s in segments])
    monthly_rev = (base_rev * RNG.lognormal(0, 0.3, n)).astype(int)

    churn_base = {"Premium": 0.05, "Mass Market": 0.18,
                  "Emerging": 0.28, "Agricultural": 0.22, "Youth": 0.35}
    churn_prob = np.array([churn_base[s] for s in segments])
    churn_prob += 0.01 * (48 - tenure) / 48
    churn_prob = np.clip(churn_prob + RNG.normal(0, 0.03, n), 0.01, 0.95)
    churned = (RNG.random(n) < churn_prob).astype(int)

    expected_months = np.minimum(36, 1 / (churn_prob + 0.01))
    ltv = (monthly_rev * 0.62 * expected_months * 0.95).astype(int)
    cac = np.where(segments == "Premium", 2800,
          np.where(segments == "Mass Market", 1400,
          np.where(segments == "Emerging", 900, 1100)))
    cac = (cac + RNG.normal(0, 150, n)).clip(400, 5000).astype(int)

    countries = RNG.choice(
        ["Kenya", "Uganda", "Tanzania", "Rwanda", "Ethiopia"],
        n, p=[0.40, 0.20, 0.20, 0.10, 0.10]
    )

    return pd.DataFrame({
        "customer_id": [f"C{str(i).zfill(5)}" for i in range(n)],
        "segment": segments,
        "country": countries,
        "tenure_months": tenure,
        "monthly_revenue_ksh": monthly_rev,
        "churn_probability": churn_prob.round(3),
        "churned": churned,
        "ltv_ksh": ltv,
        "cac_ksh": cac,
        "ltv_cac_ratio": (ltv / cac).round(2),
        "risk_band": pd.cut(churn_prob, [0, 0.2, 0.4, 1.0],
                            labels=["Low", "Medium", "High"]).astype(str),
    })


# ── Market & Yield Curve ──────────────────────────────────────────────────

def nelson_siegel_yield(tau, b0, b1, b2, lam):
    lam = max(lam, 1e-6)
    f1 = (1 - np.exp(-lam * tau)) / (lam * tau)
    f2 = f1 - np.exp(-lam * tau)
    return b0 + b1 * f1 + b2 * f2


def generate_yield_curve(scenario="baseline"):
    maturities = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 15, 20])
    params = {
        "baseline":    (12.5, -3.2, 1.8, 0.5),
        "rate_hike":   (14.0, -2.5, 1.5, 0.4),
        "rate_cut":    (10.5, -3.8, 2.2, 0.6),
        "flat":        (12.0, -0.5, 0.3, 0.5),
        "inverted":    (11.0,  2.5, -1.0, 0.5),
    }
    b0, b1, b2, lam = params.get(scenario, params["baseline"])
    yields = np.array([nelson_siegel_yield(t, b0, b1, b2, lam)
                       for t in maturities])
    return pd.DataFrame({"maturity": maturities, "yield_pct": yields.round(3)})


def generate_market_returns(n_days=504):
    tickers = ["NSE20", "SAFCOM", "KCB", "EQUITY", "EABL"]
    mus   = [0.0003, 0.0005, 0.0004, 0.0006, 0.0002]
    vols  = [0.010,  0.015,  0.018,  0.016,  0.012 ]
    corr  = np.array([
        [1.00, 0.65, 0.70, 0.68, 0.50],
        [0.65, 1.00, 0.55, 0.58, 0.40],
        [0.70, 0.55, 1.00, 0.75, 0.45],
        [0.68, 0.58, 0.75, 1.00, 0.48],
        [0.50, 0.40, 0.45, 0.48, 1.00],
    ])
    cov = np.outer(vols, vols) * corr
    rets = RNG.multivariate_normal(mus, cov, n_days)
    dates = pd.bdate_range(end=datetime.today(), periods=n_days)
    return pd.DataFrame(rets, columns=tickers, index=dates)
