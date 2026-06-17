
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Financial Freedom", page_icon="💼", layout="wide")

DATA_DIR = Path("data")
SETTINGS_PATH = DATA_DIR / "settings.json"
SNAPSHOT_PATH = DATA_DIR / "monthly_snapshots.csv"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_SETTINGS = {
    "current_age": 50, "target_retirement_age": 55, "super_access_age": 60,
    "target_income": 120000, "inflation_rate_pct": 3.0,
    "current_portfolio": 900000, "monthly_investment": 3000,
    "dividend_yield_pct": 5.0, "portfolio_growth_rate_pct": 6.0,
    "super_balance_1": 400000, "super_balance_2": 250000,
    "super_growth_rate_pct": 6.0, "super_drawdown_pct": 4.0,
    "home_loan_balance": 155000, "home_loan_interest_pct": 6.25, "home_loan_monthly_repayment": 6000,
    "car_loan_balance": 0, "car_loan_interest_pct": 8.0, "car_loan_monthly_repayment": 0,
    "credit_card_balance": 0, "credit_card_interest_pct": 20.0, "credit_card_monthly_repayment": 0,
    "personal_loan_balance": 0, "personal_loan_interest_pct": 10.0, "personal_loan_monthly_repayment": 0,
    "extra_bad_debt_repayment": 0,
    "investment_loan_balance": 500000, "investment_loan_interest_pct": 0.0, "investment_loan_monthly_repayment": 2800,
    "cash_balance": 25000,
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #f6f8fb; }
.main .block-container { padding-top: 1.35rem; padding-left: 2.7rem; padding-right: 2.7rem; max-width: 1500px; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #06111f 0%, #102033 100%); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] summary { color: #f8fafc !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    color: #0f172a !important; background-color: #ffffff !important; caret-color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-baseweb="input"], [data-testid="stSidebar"] div[data-baseweb="input"] * {
    background-color: #ffffff !important; color: #0f172a !important;
}
[data-testid="stSidebar"] summary { background-color: rgba(255,255,255,0.065); border-radius: 10px; }

[data-testid="stSidebar"] .stButton > button {
    background: #38bdf8 !important;
    color: #06111f !important;
    border: 1px solid #38bdf8 !important;
    font-weight: 900 !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] .stButton > button * { color: #06111f !important; font-weight: 900 !important; }
[data-testid="stSidebar"] .stButton > button:hover {
    background: #7dd3fc !important;
    color: #06111f !important;
    border-color: #7dd3fc !important;
}

.app-header {
    display:flex;
    align-items:flex-end;
    justify-content:space-between;
    gap: 1rem;
    margin-bottom: 1rem;
}
.title-block h1 {
    font-size: 2.25rem;
    line-height: 1;
    margin: 0;
    font-weight: 900;
    letter-spacing: -0.055em;
    color: #0f172a;
}
.title-block .subtitle {
    color:#64748b;
    margin-top: 0.35rem;
    font-size: 1rem;
    font-weight: 600;
}
.asof {
    color:#64748b;
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:999px;
    padding:0.55rem 0.9rem;
    font-size:0.82rem;
    font-weight:700;
}

.hero {
    background: radial-gradient(circle at top left, #1d4ed8 0%, #0f172a 42%, #020617 100%);
    color: white;
    border-radius: 28px;
    padding: 2rem 2.2rem;
    margin: 0.8rem 0 1.1rem 0;
    box-shadow: 0 24px 55px rgba(15, 23, 42, 0.28);
    display: grid;
    grid-template-columns: 1.05fr 1fr;
    gap: 2rem;
    align-items: center;
}
.hero-kicker {
    color:#93c5fd;
    font-size:0.78rem;
    font-weight:900;
    letter-spacing:0.12em;
    text-transform:uppercase;
}
.hero-number {
    font-size: 5.5rem;
    line-height: 0.95;
    font-weight: 900;
    letter-spacing: -0.08em;
    margin-top:0.35rem;
}
.hero-label {
    font-size:1.15rem;
    color:#dbeafe;
    font-weight:700;
    margin-top:0.55rem;
}
.hero-status {
    display:inline-block;
    margin-top:1rem;
    padding:0.45rem 0.75rem;
    border-radius:999px;
    font-weight:900;
    font-size:0.8rem;
    color:#06111f;
}
.hero-status.good { background:#86efac; }
.hero-status.watch { background:#fcd34d; }
.hero-status.bad { background:#fca5a5; }

.hero-right {
    background: rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.14);
    border-radius:22px;
    padding:1.2rem;
}
.progress-label {
    display:flex;
    justify-content:space-between;
    color:#dbeafe;
    font-weight:800;
    font-size:0.9rem;
    margin-bottom:0.55rem;
}
.progress-track {
    height: 16px;
    background: rgba(255,255,255,0.18);
    border-radius:999px;
    overflow:hidden;
}
.progress-fill {
    height:100%;
    border-radius:999px;
    background: linear-gradient(90deg, #38bdf8, #22c55e);
}
.hero-right .small-note {
    color:#bfdbfe;
    font-size:0.86rem;
    line-height:1.5;
    margin-top:0.9rem;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 18px 18px 16px 18px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.065);
    min-height: 128px;
}
.metric-card .eyebrow {
    font-size: 0.70rem;
    color: #64748b;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-card .value {
    font-size: 1.85rem;
    color: #0f172a;
    font-weight: 900;
    letter-spacing: -0.045em;
    margin-top: 7px;
}
.metric-card .note {
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 6px;
    font-weight:600;
}
.status-good { color: #16a34a !important; }
.status-watch { color: #d97706 !important; }
.status-bad { color: #dc2626 !important; }

.panel {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055);
    margin-bottom: 18px;
}
.panel-title { font-weight: 900; font-size: 1.15rem; color: #0f172a; margin-bottom: 4px; letter-spacing:-0.03em; }
.panel-subtitle { color: #64748b; font-size: 0.86rem; margin-bottom: 12px; font-weight:600; }
.insight-box {
    background:#f8fafc;
    border:1px solid #e2e8f0;
    border-radius:16px;
    padding:14px 16px;
    color:#334155;
    font-size:0.92rem;
    line-height:1.55;
    font-weight:600;
}
.insight-box b { color:#0f172a; }

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 14px 16px;
    border-radius: 17px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
}
div[data-testid="stMetricLabel"] { color: #64748b; font-weight: 800; }
div[data-testid="stMetricValue"] { color: #0f172a; font-weight: 900; letter-spacing:-0.03em; }

h2, h3 { color:#0f172a; letter-spacing:-0.04em; font-weight:900; }
.block-spacer { height:0.5rem; }
</style>
""", unsafe_allow_html=True)

def load_settings():
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r") as f:
        data = json.load(f)
    for k, v in DEFAULT_SETTINGS.items():
        data.setdefault(k, v)
    return data

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)

def pct_to_rate(v): return float(v) / 100
def money(v):
    v = float(v)
    if abs(v) >= 1_000_000: return f"${v/1_000_000:.2f}M"
    return f"${v:,.0f}"
def age_text(v): return "Not reached" if v is None else f"{v:.1f}"
def years_text(v): return "Not reached" if v is None else f"{v:.1f} years"

def future_value_monthly(start_value, monthly_contribution, annual_growth_rate, months):
    values, balance = [], float(start_value)
    monthly_rate = annual_growth_rate / 12
    for m in range(months + 1):
        values.append(balance)
        balance = balance * (1 + monthly_rate) + monthly_contribution
    return values

def debt_paydown_series(balance, annual_interest_rate, monthly_repayment, extra_repayment=0, months=600):
    rows, debt = [], float(balance)
    monthly_rate = annual_interest_rate / 12
    payment = float(monthly_repayment) + float(extra_repayment)
    for m in range(months + 1):
        rows.append({"month": m, "balance": max(debt, 0)})
        if debt <= 0:
            debt = 0
            continue
        interest = debt * monthly_rate
        principal = max(payment - interest, 0)
        debt = max(0, debt - principal)
        if payment <= interest and debt > 0:
            debt = debt + interest - payment
    return pd.DataFrame(rows[:months+1])

def calculate_total_bad_debt(s):
    return s["home_loan_balance"] + s["car_loan_balance"] + s["credit_card_balance"] + s["personal_loan_balance"]
def calculate_total_bad_debt_repayment(s):
    return s["home_loan_monthly_repayment"] + s["car_loan_monthly_repayment"] + s["credit_card_monthly_repayment"] + s["personal_loan_monthly_repayment"] + s["extra_bad_debt_repayment"]

def build_forecast(s, years=40):
    months = years * 12
    portfolio_growth = pct_to_rate(s["portfolio_growth_rate_pct"])
    super_growth = pct_to_rate(s["super_growth_rate_pct"])
    dividend_yield = pct_to_rate(s["dividend_yield_pct"])
    inflation_rate = pct_to_rate(s["inflation_rate_pct"])
    super_drawdown = pct_to_rate(s["super_drawdown_pct"])
    combined_super = s["super_balance_1"] + s["super_balance_2"]

    portfolio_values = future_value_monthly(s["current_portfolio"], s["monthly_investment"], portfolio_growth, months)
    super_values = future_value_monthly(combined_super, 0, super_growth, months)

    home_df = debt_paydown_series(s["home_loan_balance"], pct_to_rate(s["home_loan_interest_pct"]), s["home_loan_monthly_repayment"], s["extra_bad_debt_repayment"], months)
    car_df = debt_paydown_series(s["car_loan_balance"], pct_to_rate(s["car_loan_interest_pct"]), s["car_loan_monthly_repayment"], 0, months)
    credit_df = debt_paydown_series(s["credit_card_balance"], pct_to_rate(s["credit_card_interest_pct"]), s["credit_card_monthly_repayment"], 0, months)
    personal_df = debt_paydown_series(s["personal_loan_balance"], pct_to_rate(s["personal_loan_interest_pct"]), s["personal_loan_monthly_repayment"], 0, months)
    inv_df = debt_paydown_series(s["investment_loan_balance"], pct_to_rate(s["investment_loan_interest_pct"]), s["investment_loan_monthly_repayment"], 0, months)

    home_l, car_l, credit_l, personal_l, inv_l = [dict(zip(df["month"], df["balance"])) for df in [home_df, car_df, credit_df, personal_df, inv_df]]

    rows = []
    for m in range(months + 1):
        age = s["current_age"] + m / 12
        portfolio = portfolio_values[m]
        super_balance = super_values[m]
        dividend_income = portfolio * dividend_yield
        super_income = super_balance * super_drawdown if age >= s["super_access_age"] else 0
        retirement_income = dividend_income + super_income
        target_income = s["target_income"] * ((1 + inflation_rate) ** (m / 12))
        home = home_l.get(m, 0); car = car_l.get(m, 0); credit = credit_l.get(m, 0); personal = personal_l.get(m, 0)
        bad_debt = home + car + credit + personal
        investment_loan = inv_l.get(m, 0)
        income_test = dividend_income if age < s["super_access_age"] else retirement_income
        financial_freedom = bad_debt <= 0 and income_test >= target_income
        rows.append({
            "month": m, "age": age, "portfolio": portfolio, "super": super_balance,
            "dividend_income": dividend_income, "super_income": super_income,
            "retirement_income": retirement_income, "target_income": target_income,
            "home_loan": home, "car_loan": car, "credit_card": credit, "personal_loan": personal,
            "bad_debt": bad_debt, "investment_loan": investment_loan, "financial_freedom": financial_freedom,
        })
    return pd.DataFrame(rows)

def first_true_age(df, col):
    hits = df[df[col] == True]
    return None if hits.empty else float(hits.iloc[0]["age"])
def first_zero_bad_debt_age(df):
    hits = df[df["bad_debt"] <= 0]
    return None if hits.empty else float(hits.iloc[0]["age"])
def value_at_age(df, age, col):
    row = df.iloc[(df["age"] - age).abs().argsort()[:1]]
    return float(row[col].iloc[0])
def pre_super_check(df, s):
    pre = df[(df["age"] >= s["target_retirement_age"]) & (df["age"] < s["super_access_age"]) & (df["month"] % 12 == 0)]
    if pre.empty: return {"required":0,"dividends":0,"cash":s.get("cash_balance",0),"gap":0,"ready":False}
    required = pre["target_income"].sum()
    dividends = pre["dividend_income"].sum()
    cash = s.get("cash_balance", 0)
    gap = required - dividends - cash
    return {"required":required, "dividends":dividends, "cash":cash, "gap":gap, "ready":gap<=0}

def load_history():
    return pd.read_csv(SNAPSHOT_PATH) if SNAPSHOT_PATH.exists() else pd.DataFrame()
def monthly_movement(history, col):
    if history.empty or len(history) < 2 or col not in history.columns:
        return None, None
    h = history.sort_values("month").reset_index(drop=True)
    previous = float(h[col].iloc[-2])
    current = float(h[col].iloc[-1])
    change = current - previous
    pct = None if previous == 0 else (change / previous) * 100
    return change, pct
def format_signed_money(value):
    if value is None: return "—"
    sign = "+" if value >= 0 else "-"
    return f"{sign}{money(abs(value))}"
def format_signed_pct(value):
    if value is None: return "—"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"
def card(title, value, note="", status=""):
    cls = {"good":"status-good","watch":"status-watch","bad":"status-bad"}.get(status,"")
    st.markdown(f"""<div class="metric-card"><div class="eyebrow">{title}</div><div class="value {cls}">{value}</div><div class="note">{note}</div></div>""", unsafe_allow_html=True)
def style_plot(fig, height=350):
    fig.update_layout(height=height, template="plotly_white", margin=dict(l=10,r=10,t=30,b=20),
                      font=dict(family="Inter", size=12, color="#334155"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      hovermode="x unified")
    fig.update_xaxes(showgrid=False, linecolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#eef2f7", zerolinecolor="#e5e7eb")
    return fig

settings = load_settings()

st.sidebar.title("Inputs")
st.sidebar.caption("Manual values. Forecasts and history are calculated automatically.")

with st.sidebar.expander("Core Assumptions", expanded=True):
    settings["current_age"] = st.number_input("Current Age", value=float(settings["current_age"]), step=0.5, help="Your current age. Used as the starting point for all forecasts.")
    settings["target_retirement_age"] = st.number_input("Target Retirement Age", value=float(settings["target_retirement_age"]), step=0.5, help="Age you are testing as the point where work may become optional.")
    settings["target_income"] = st.number_input("Target Annual Income", value=int(settings["target_income"]), step=5000, help="Annual income required from target retirement age onward. Include lifestyle costs and investment loan servicing.")
    settings["inflation_rate_pct"] = st.number_input("Inflation Assumption %", value=float(settings["inflation_rate_pct"]), step=0.01, format="%.2f", help="Planning assumption used to increase target income over time.")

with st.sidebar.expander("Investment Portfolio"):
    settings["current_portfolio"] = st.number_input("Portfolio Value", value=int(settings["current_portfolio"]), step=10000, help="Current value of non-super investments.")
    settings["monthly_investment"] = st.number_input("Monthly Investment", value=int(settings["monthly_investment"]), step=500, help="Monthly contribution to the investment portfolio.")
    settings["dividend_yield_pct"] = st.number_input("Dividend Yield %", value=float(settings["dividend_yield_pct"]), step=0.01, format="%.2f", help="Expected annual dividend yield.")
    settings["portfolio_growth_rate_pct"] = st.number_input("Long-Term Forecast Growth %", value=float(settings["portfolio_growth_rate_pct"]), step=0.01, format="%.2f", help="Long-term capital growth assumption.")

with st.sidebar.expander("Superannuation"):
    settings["super_balance_1"] = st.number_input("Super Balance 1", value=int(settings["super_balance_1"]), step=10000, help="First super balance.")
    settings["super_balance_2"] = st.number_input("Super Balance 2", value=int(settings["super_balance_2"]), step=10000, help="Second super balance.")
    st.info(f"Combined Super: {money(settings['super_balance_1'] + settings['super_balance_2'])}")
    settings["super_growth_rate_pct"] = st.number_input("Long-Term Super Growth %", value=float(settings["super_growth_rate_pct"]), step=0.01, format="%.2f")
    settings["super_drawdown_pct"] = st.number_input("Super Drawdown %", value=float(settings["super_drawdown_pct"]), step=0.01, format="%.2f", help="Annual income assumed from super after age 60.")

with st.sidebar.expander("Bad Debt"):
    st.markdown("**Home Loan**")
    settings["home_loan_balance"] = st.number_input("Home Loan Balance", value=int(settings["home_loan_balance"]), step=10000)
    settings["home_loan_interest_pct"] = st.number_input("Home Loan Interest %", value=float(settings["home_loan_interest_pct"]), step=0.01, format="%.2f")
    settings["home_loan_monthly_repayment"] = st.number_input("Home Loan Monthly Repayment", value=int(settings["home_loan_monthly_repayment"]), step=500)
    st.markdown("**Car Loan**")
    settings["car_loan_balance"] = st.number_input("Car Loan Balance", value=int(settings["car_loan_balance"]), step=1000)
    settings["car_loan_interest_pct"] = st.number_input("Car Loan Interest %", value=float(settings["car_loan_interest_pct"]), step=0.01, format="%.2f")
    settings["car_loan_monthly_repayment"] = st.number_input("Car Loan Monthly Repayment", value=int(settings["car_loan_monthly_repayment"]), step=100)
    st.markdown("**Credit Card**")
    settings["credit_card_balance"] = st.number_input("Credit Card Balance", value=int(settings["credit_card_balance"]), step=500)
    settings["credit_card_interest_pct"] = st.number_input("Credit Card Interest %", value=float(settings["credit_card_interest_pct"]), step=0.01, format="%.2f")
    settings["credit_card_monthly_repayment"] = st.number_input("Credit Card Monthly Repayment", value=int(settings["credit_card_monthly_repayment"]), step=100)
    st.markdown("**Other Personal Loan**")
    settings["personal_loan_balance"] = st.number_input("Personal Loan Balance", value=int(settings["personal_loan_balance"]), step=1000)
    settings["personal_loan_interest_pct"] = st.number_input("Personal Loan Interest %", value=float(settings["personal_loan_interest_pct"]), step=0.01, format="%.2f")
    settings["personal_loan_monthly_repayment"] = st.number_input("Personal Loan Monthly Repayment", value=int(settings["personal_loan_monthly_repayment"]), step=100)
    settings["extra_bad_debt_repayment"] = st.number_input("Extra Bad Debt Repayment", value=int(settings["extra_bad_debt_repayment"]), step=500, help="Extra monthly repayment applied to bad debt.")

with st.sidebar.expander("Investment Loan"):
    settings["investment_loan_balance"] = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000)
    settings["investment_loan_interest_pct"] = st.number_input("Investment Loan Interest %", value=float(settings["investment_loan_interest_pct"]), step=0.01, format="%.2f")
    settings["investment_loan_monthly_repayment"] = st.number_input("Investment Loan Monthly Repayment", value=int(settings["investment_loan_monthly_repayment"]), step=500)

with st.sidebar.expander("Cash"):
    settings["cash_balance"] = st.number_input("Cash Balance", value=int(settings.get("cash_balance",0)), step=1000)

if st.sidebar.button("Save Inputs", use_container_width=True):
    save_settings(settings)
    st.sidebar.success("Inputs saved")

forecast = build_forecast(settings)
annual = forecast[forecast["month"] % 12 == 0].copy()
freedom_age = first_true_age(forecast, "financial_freedom")
bad_debt_free_age = first_zero_bad_debt_age(forecast)
pre60 = pre_super_check(forecast, settings)

combined_super = settings["super_balance_1"] + settings["super_balance_2"]
total_bad_debt = calculate_total_bad_debt(settings)
current_dividends = settings["current_portfolio"] * pct_to_rate(settings["dividend_yield_pct"])
years_remaining = None if freedom_age is None else max(freedom_age - settings["current_age"], 0)
net_position = settings["current_portfolio"] + combined_super + settings.get("cash_balance",0) - total_bad_debt - settings["investment_loan_balance"]

history = load_history()
portfolio_change, portfolio_pct = monthly_movement(history, "portfolio_value")
super_change, super_pct = monthly_movement(history, "combined_super")
bad_debt_change, bad_debt_pct = monthly_movement(history, "total_bad_debt")
cash_change, cash_pct = monthly_movement(history, "cash_balance")

target_age = settings["target_retirement_age"]
target_income_at_goal = value_at_age(forecast, target_age, "target_income")
dividends_at_goal = value_at_age(forecast, target_age, "dividend_income")
income_gap_at_goal = target_income_at_goal - dividends_at_goal
extra_capital_required = max(0, income_gap_at_goal / pct_to_rate(settings["dividend_yield_pct"])) if settings["dividend_yield_pct"] > 0 else 0
required_portfolio_at_goal = target_income_at_goal / pct_to_rate(settings["dividend_yield_pct"]) if settings["dividend_yield_pct"] > 0 else 0
progress_pct = min(100, max(0, (settings["current_portfolio"] / required_portfolio_at_goal) * 100)) if required_portfolio_at_goal > 0 else 0

if freedom_age is None:
    hero_years = "—"
    hero_note = "Not reached in forecast period"
    hero_status = "bad"
    hero_status_text = "Needs focus"
else:
    hero_years = f"{years_remaining:.1f}"
    hero_note = "Until financial freedom"
    if freedom_age <= target_age:
        hero_status = "good"
        hero_status_text = "Ahead of plan"
    elif freedom_age <= settings["super_access_age"]:
        hero_status = "watch"
        hero_status_text = "Close to plan"
    else:
        hero_status = "bad"
        hero_status_text = "Behind target"

st.markdown(f"""
<div class="app-header">
    <div class="title-block">
        <h1>Financial Freedom</h1>
        <div class="subtitle">How many more years do we need to work?</div>
    </div>
    <div class="asof">As of latest monthly snapshot</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
    <div>
        <div class="hero-kicker">Core answer</div>
        <div class="hero-number">{hero_years}</div>
        <div class="hero-label">years until financial freedom</div>
        <div class="hero-status {hero_status}">{hero_status_text}</div>
    </div>
    <div class="hero-right">
        <div class="progress-label">
            <span>Financial freedom progress</span>
            <span>{progress_pct:.0f}%</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{progress_pct:.0f}%"></div>
        </div>
        <div class="small-note">
            Current portfolio is <b>{money(settings["current_portfolio"])}</b>. 
            Approximate portfolio required by target age is <b>{money(required_portfolio_at_goal)}</b>. 
            Gap remaining is <b>{money(max(0, required_portfolio_at_goal - settings["current_portfolio"]))}</b>.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: card("Financial freedom age", age_text(freedom_age), years_text(years_remaining), hero_status)
with c2: card("Age 55 income gap", money(income_gap_at_goal), "Target income less projected dividends", "good" if income_gap_at_goal<=0 else "bad")
with c3: card("Debt free age", age_text(bad_debt_free_age), f"{money(total_bad_debt)} bad debt remaining", "good" if bad_debt_free_age and bad_debt_free_age<=target_age else "watch")
with c4: card("Extra capital needed", money(extra_capital_required), "At current dividend yield", "good" if extra_capital_required<=0 else "watch")

st.markdown('<div class="block-spacer"></div>', unsafe_allow_html=True)

mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    st.metric("Portfolio movement", format_signed_money(portfolio_change), format_signed_pct(portfolio_pct), help="Change from last saved monthly snapshot. Can be positive or negative.")
with mc2:
    st.metric("Super movement", format_signed_money(super_change), format_signed_pct(super_pct), help="Combined super change from last saved monthly snapshot.")
with mc3:
    # for debt, negative is good, but Streamlit delta colour is not controlled reliably. Text explains it.
    st.metric("Bad debt movement", format_signed_money(bad_debt_change), format_signed_pct(bad_debt_pct), help="Change in total bad debt from last month. Negative is good because debt reduced.")
with mc4:
    st.metric("Cash movement", format_signed_money(cash_change), format_signed_pct(cash_pct), help="Cash balance change from last saved monthly snapshot.")

st.divider()

left, centre, right = st.columns([1.0,1.55,1.35])

with left:
    st.markdown('<div class="panel"><div class="panel-title">What’s missing?</div><div class="panel-subtitle">The gap to retire at the target age.</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-box">
    To retire at <b>{target_age:.1f}</b>, projected dividends need to cover 
    <b>{money(target_income_at_goal)}</b> per year.<br><br>
    Current trajectory produces <b>{money(dividends_at_goal)}</b> at that age.<br><br>
    Missing income: <b>{money(income_gap_at_goal)}</b><br>
    Equivalent extra capital: <b>{money(extra_capital_required)}</b>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with centre:
    st.markdown('<div class="panel"><div class="panel-title">Path to target retirement age</div><div class="panel-subtitle">Starts today and tests whether dividends reach the target income by the goal age.</div>', unsafe_allow_html=True)
    plus150 = settings.copy(); plus150["current_portfolio"] += 150000
    plus150_df = build_forecast(plus150)
    higher_monthly = settings.copy(); higher_monthly["monthly_investment"] += 2000
    higher_monthly_df = build_forecast(higher_monthly)

    path_df = forecast[(forecast["age"] >= settings["current_age"]) & (forecast["age"] <= settings["super_access_age"]) & (forecast["month"] % 12 == 0)]
    p150_path = plus150_df[(plus150_df["age"] >= settings["current_age"]) & (plus150_df["age"] <= settings["super_access_age"]) & (plus150_df["month"] % 12 == 0)]
    hm_path = higher_monthly_df[(higher_monthly_df["age"] >= settings["current_age"]) & (higher_monthly_df["age"] <= settings["super_access_age"]) & (higher_monthly_df["month"] % 12 == 0)]

    fig_path = go.Figure()
    fig_path.add_trace(go.Scatter(x=path_df["age"], y=path_df["target_income"], mode="lines", name="Target income", line=dict(color="#94a3b8", width=3, dash="dash")))
    fig_path.add_trace(go.Scatter(x=path_df["age"], y=path_df["dividend_income"], mode="lines+markers", name="Base dividends", line=dict(color="#0f3b68", width=4)))
    fig_path.add_trace(go.Scatter(x=p150_path["age"], y=p150_path["dividend_income"], mode="lines", name="+$150k now", line=dict(color="#16a34a", width=3)))
    fig_path.add_trace(go.Scatter(x=hm_path["age"], y=hm_path["dividend_income"], mode="lines", name="+$2k/month", line=dict(color="#d97706", width=3)))
    fig_path.add_vline(x=target_age, line_width=2, line_dash="dot", line_color="#dc2626")
    fig_path.add_annotation(x=target_age, y=path_df["target_income"].max(), text="Target age", showarrow=False, yshift=18, font=dict(color="#dc2626"))
    st.plotly_chart(style_plot(fig_path, height=395), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">Debt elimination</div><div class="panel-subtitle">Auto-scaled to the useful payoff period.</div>', unsafe_allow_html=True)
    x_max = max(settings["current_age"] + 1, (bad_debt_free_age if bad_debt_free_age is not None else settings["current_age"] + 10) + 1)
    debt_df = annual[(annual["age"] >= settings["current_age"]) & (annual["age"] <= x_max)]
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Scatter(x=debt_df["age"], y=debt_df["bad_debt"], mode="lines+markers", name="Bad debt", line=dict(color="#dc2626", width=4)))
    fig_debt.add_trace(go.Scatter(x=debt_df["age"], y=debt_df["home_loan"], mode="lines", name="Home loan", line=dict(color="#0f3b68", width=3, dash="dot")))
    if bad_debt_free_age is not None:
        fig_debt.add_vline(x=bad_debt_free_age, line_width=2, line_dash="dot", line_color="#16a34a")
    st.plotly_chart(style_plot(fig_debt, height=395), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

a,b,c = st.columns(3)

with a:
    st.markdown('<div class="panel"><div class="panel-title">55–60 funding</div><div class="panel-subtitle">Pre-super period. Dividends and cash only.</div>', unsafe_allow_html=True)
    st.metric("Required 55–60", money(pre60["required"]), help="Total target income required from target retirement age to super access age.")
    st.metric("Dividends 55–60", money(pre60["dividends"]), help="Projected dividend income during that period.")
    st.metric("Cash available", money(pre60["cash"]), help="Cash balance included as part of the pre-super funding check.")
    st.metric("Pre-super gap", money(pre60["gap"]), help="Required income minus dividends and cash.")
    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="panel"><div class="panel-title">Post-60 income mix</div><div class="panel-subtitle">After super access, income comes from dividends and super.</div>', unsafe_allow_html=True)
    post_df = forecast[(forecast["age"] >= settings["super_access_age"]) & (forecast["age"] <= settings["super_access_age"]+10) & (forecast["month"]%12==0)].copy()
    fig_post = go.Figure()
    fig_post.add_trace(go.Bar(x=post_df["age"], y=post_df["dividend_income"], name="Dividends", marker_color="#0f3b68"))
    fig_post.add_trace(go.Bar(x=post_df["age"], y=post_df["super_income"], name="Super income", marker_color="#16a34a"))
    fig_post.add_trace(go.Scatter(x=post_df["age"], y=post_df["target_income"], mode="lines", name="Target", line=dict(color="#94a3b8", width=3, dash="dash")))
    fig_post.update_layout(barmode="stack")
    st.plotly_chart(style_plot(fig_post, height=325), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c:
    st.markdown('<div class="panel"><div class="panel-title">Current position</div><div class="panel-subtitle">Balance sheet snapshot.</div>', unsafe_allow_html=True)
    st.metric("Portfolio", money(settings["current_portfolio"]))
    st.metric("Combined super", money(settings["super_balance_1"] + settings["super_balance_2"]))
    st.metric("Bad debt", money(total_bad_debt))
    st.metric("Net position", money(net_position))
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.subheader("Scenario Lab")
st.caption("Use the levers to see what moves the answer. Negative movement is good because it brings financial freedom forward.")

s1,s2,s3,s4 = st.columns(4)
with s1: scenario_income = st.slider("Target income", 80000, 180000, int(settings["target_income"]), 5000, help="Scenario target annual income.")
with s2: scenario_monthly_investment = st.slider("Monthly investment", 0, 10000, int(settings["monthly_investment"]), 500, help="Impacts portfolio growth and dividends.")
with s3: scenario_extra_debt = st.slider("Extra bad debt repayment", 0, 10000, int(settings["extra_bad_debt_repayment"]), 500, help="Impacts bad debt free age.")
with s4: scenario_growth_pct = st.slider("Portfolio growth %", 0.0, 12.0, float(settings["portfolio_growth_rate_pct"]), 0.1, help="Scenario capital growth assumption.")

scenario_settings = settings.copy()
scenario_settings["target_income"] = scenario_income
scenario_settings["monthly_investment"] = scenario_monthly_investment
scenario_settings["extra_bad_debt_repayment"] = scenario_extra_debt
scenario_settings["portfolio_growth_rate_pct"] = scenario_growth_pct
scenario_df = build_forecast(scenario_settings)
scenario_age = first_true_age(scenario_df, "financial_freedom")
scenario_bad_debt_age = first_zero_bad_debt_age(scenario_df)
scenario_target_income = value_at_age(scenario_df, scenario_settings["target_retirement_age"], "target_income")
scenario_dividends = value_at_age(scenario_df, scenario_settings["target_retirement_age"], "dividend_income")
scenario_gap_at_target = scenario_target_income - scenario_dividends

m1,m2,m3,m4 = st.columns(4)
with m1: st.metric("Scenario freedom age", age_text(scenario_age), help="Projected financial freedom age using all scenario levers.")
with m2: st.metric("Scenario debt free age", age_text(scenario_bad_debt_age), help="Bad debt free age after scenario extra repayments.")
with m3: st.metric("Scenario gap at target age", money(scenario_gap_at_target), help="Target income less projected dividends at the target retirement age.")
with m4:
    movement_label = "—" if freedom_age is None or scenario_age is None else f"{scenario_age - freedom_age:+.1f} years"
    st.metric("Movement vs base case", movement_label, help="Scenario Financial Freedom Age minus Base Case. Negative is better.")

st.divider()

st.subheader("Monthly Snapshot & History")
st.caption("Dummy data is pre-loaded. Save current values once per month to build your real history.")

snap_left,snap_right = st.columns([1,2])
with snap_left:
    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    notes = st.text_area("Notes", height=80)
    if st.button("Save Current Month Snapshot", use_container_width=True):
        cols = ["month","portfolio_value","super_balance_1","super_balance_2","combined_super","home_loan_balance","car_loan_balance","credit_card_balance","personal_loan_balance","total_bad_debt","investment_loan_balance","cash_balance","annual_dividend_income","notes"]
        hist = pd.read_csv(SNAPSHOT_PATH) if SNAPSHOT_PATH.exists() else pd.DataFrame(columns=cols)
        for col in cols:
            if col not in hist.columns: hist[col] = None
        new = {"month":month,"portfolio_value":settings["current_portfolio"],"super_balance_1":settings["super_balance_1"],"super_balance_2":settings["super_balance_2"],"combined_super":combined_super,
               "home_loan_balance":settings["home_loan_balance"],"car_loan_balance":settings["car_loan_balance"],"credit_card_balance":settings["credit_card_balance"],"personal_loan_balance":settings["personal_loan_balance"],
               "total_bad_debt":calculate_total_bad_debt(settings),"investment_loan_balance":settings["investment_loan_balance"],"cash_balance":settings.get("cash_balance",0),
               "annual_dividend_income":settings["current_portfolio"]*pct_to_rate(settings["dividend_yield_pct"]),"notes":notes}
        hist = hist[hist["month"] != month]
        hist = pd.concat([hist, pd.DataFrame([new])], ignore_index=True)[cols]
        hist.to_csv(SNAPSHOT_PATH, index=False)
        st.success("Snapshot saved")

with snap_right:
    hist = load_history()
    if not hist.empty:
        hist = hist.sort_values("month")
        fig_hist = go.Figure()
        for col,name,color in [("portfolio_value","Portfolio","#0f3b68"),("combined_super","Combined super","#2563eb"),("total_bad_debt","Bad debt","#dc2626"),("investment_loan_balance","Investment loan","#d97706")]:
            if col in hist.columns:
                fig_hist.add_trace(go.Scatter(x=hist["month"], y=hist[col], mode="lines+markers", name=name, line=dict(color=color, width=3)))
        st.plotly_chart(style_plot(fig_hist, height=330), use_container_width=True)
        with st.expander("View snapshot table"):
            st.dataframe(hist, use_container_width=True)
    else:
        st.info("No monthly snapshots saved yet.")
