
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Financial Freedom Planner", page_icon="💼", layout="wide")

DATA_DIR = Path("data")
SETTINGS_PATH = DATA_DIR / "settings.json"
SNAPSHOT_PATH = DATA_DIR / "monthly_snapshots.csv"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_SETTINGS = {
    "current_age": 50,
    "target_retirement_age": 55,
    "super_access_age": 60,
    "target_income": 120000,
    "inflation_rate_pct": 3.0,
    "current_portfolio": 900000,
    "monthly_investment": 3000,
    "dividend_yield_pct": 5.0,
    "portfolio_growth_rate_pct": 6.0,
    "super_balance_1": 400000,
    "super_balance_2": 250000,
    "super_growth_rate_pct": 6.0,
    "super_drawdown_pct": 4.0,
    "home_loan_balance": 155000,
    "home_loan_interest_pct": 6.0,
    "home_loan_monthly_repayment": 6000,
    "car_loan_balance": 0,
    "car_loan_interest_pct": 8.0,
    "car_loan_monthly_repayment": 0,
    "credit_card_balance": 0,
    "credit_card_interest_pct": 20.0,
    "credit_card_monthly_repayment": 0,
    "personal_loan_balance": 0,
    "personal_loan_interest_pct": 10.0,
    "personal_loan_monthly_repayment": 0,
    "extra_bad_debt_repayment": 0,
    "investment_loan_balance": 500000,
    "investment_loan_interest_pct": 0.0,
    "investment_loan_monthly_repayment": 2800,
    "cash_balance": 25000,
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding-top: 2rem; padding-left: 3rem; padding-right: 3rem; max-width: 1450px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #07111f 0%, #0f1f33 100%); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] summary { color: #f8fafc !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    color: #0f172a !important; background-color: #ffffff !important; caret-color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-baseweb="input"], [data-testid="stSidebar"] div[data-baseweb="input"] * {
    background-color: #ffffff !important; color: #0f172a !important;
}
[data-testid="stSidebar"] button { color: #0f172a !important; }
[data-testid="stSidebar"] summary { background-color: rgba(255,255,255,0.06); border-radius: 10px; }
h1 { font-weight: 800; letter-spacing: -0.04em; color: #0f172a; }
.exec-subtitle { color: #64748b; font-size: 1.0rem; margin-top: -0.5rem; margin-bottom: 1rem; }
.executive-summary {
    background: linear-gradient(135deg, #0f172a 0%, #172554 100%); color: #ffffff;
    padding: 22px 26px; border-radius: 18px; margin: 18px 0 24px 0;
    box-shadow: 0 14px 35px rgba(15, 23, 42, 0.18);
}
.executive-summary .label { color: #93c5fd; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 7px; }
.executive-summary .text { font-size: 1.15rem; line-height: 1.55; font-weight: 500; }
.metric-card {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 18px;
    padding: 18px 18px 16px 18px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); min-height: 135px;
}
.metric-card .eyebrow { font-size: 0.72rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-card .value { font-size: 1.95rem; color: #0f172a; font-weight: 800; letter-spacing: -0.04em; margin-top: 6px; }
.metric-card .note { font-size: 0.82rem; color: #64748b; margin-top: 6px; }
.status-good { color: #16a34a !important; } .status-watch { color: #d97706 !important; } .status-bad { color: #dc2626 !important; }
.panel {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 20px; padding: 22px;
    box-shadow: 0 8px 26px rgba(15, 23, 42, 0.055); margin-bottom: 20px;
}
.panel-title { font-weight: 800; font-size: 1.2rem; color: #0f172a; margin-bottom: 6px; }
.panel-subtitle { color: #64748b; font-size: 0.88rem; margin-bottom: 12px; }
div[data-testid="stMetric"] {
    background: #ffffff; border: 1px solid #e5e7eb; padding: 14px 16px; border-radius: 16px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}
div[data-testid="stMetricLabel"] { color: #64748b; font-weight: 700; }
div[data-testid="stMetricValue"] { color: #0f172a; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

def load_settings():
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r") as f:
        data = json.load(f)
    for key, value in DEFAULT_SETTINGS.items():
        if key not in data:
            data[key] = value
    return data

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)

def pct_to_rate(value):
    return float(value) / 100

def money(value):
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    return f"${value:,.0f}"

def age_text(value):
    return "Not reached" if value is None else f"{value:.1f}"

def years_text(value):
    return "Not reached" if value is None else f"{value:.1f} years"

def future_value_monthly(start_value, monthly_contribution, annual_growth_rate, months):
    values = []
    balance = float(start_value)
    monthly_rate = annual_growth_rate / 12
    for month in range(months + 1):
        values.append(balance)
        balance = balance * (1 + monthly_rate) + monthly_contribution
    return values

def debt_paydown_series(balance, annual_interest_rate, monthly_repayment, extra_repayment=0, months=600):
    rows = []
    debt = float(balance)
    monthly_rate = annual_interest_rate / 12
    payment = float(monthly_repayment) + float(extra_repayment)
    for m in range(months + 1):
        rows.append({"month": m, "balance": max(debt, 0)})
        if debt <= 0:
            continue
        interest = debt * monthly_rate
        principal = max(payment - interest, 0)
        debt = max(0, debt - principal)
        if payment <= interest and debt > 0:
            # Still carry debt forward if repayment cannot cover interest.
            debt = debt + interest - payment
    return pd.DataFrame(rows[:months+1])

def calculate_total_bad_debt(settings):
    return settings["home_loan_balance"] + settings["car_loan_balance"] + settings["credit_card_balance"] + settings["personal_loan_balance"]

def calculate_total_bad_debt_repayment(settings):
    return settings["home_loan_monthly_repayment"] + settings["car_loan_monthly_repayment"] + settings["credit_card_monthly_repayment"] + settings["personal_loan_monthly_repayment"] + settings["extra_bad_debt_repayment"]

def build_forecast(settings, years=40):
    months = years * 12
    portfolio_growth = pct_to_rate(settings["portfolio_growth_rate_pct"])
    super_growth = pct_to_rate(settings["super_growth_rate_pct"])
    dividend_yield = pct_to_rate(settings["dividend_yield_pct"])
    inflation_rate = pct_to_rate(settings["inflation_rate_pct"])
    super_drawdown = pct_to_rate(settings["super_drawdown_pct"])
    combined_super = settings["super_balance_1"] + settings["super_balance_2"]

    portfolio_values = future_value_monthly(settings["current_portfolio"], settings["monthly_investment"], portfolio_growth, months)
    super_values = future_value_monthly(combined_super, 0, super_growth, months)

    # Scenario extra debt repayment is deliberately applied to home loan in this version.
    # This makes the lever visible and keeps the model simple.
    home_df = debt_paydown_series(settings["home_loan_balance"], pct_to_rate(settings["home_loan_interest_pct"]), settings["home_loan_monthly_repayment"], settings["extra_bad_debt_repayment"], months)
    car_df = debt_paydown_series(settings["car_loan_balance"], pct_to_rate(settings["car_loan_interest_pct"]), settings["car_loan_monthly_repayment"], 0, months)
    credit_df = debt_paydown_series(settings["credit_card_balance"], pct_to_rate(settings["credit_card_interest_pct"]), settings["credit_card_monthly_repayment"], 0, months)
    personal_df = debt_paydown_series(settings["personal_loan_balance"], pct_to_rate(settings["personal_loan_interest_pct"]), settings["personal_loan_monthly_repayment"], 0, months)
    inv_df = debt_paydown_series(settings["investment_loan_balance"], pct_to_rate(settings["investment_loan_interest_pct"]), settings["investment_loan_monthly_repayment"], 0, months)

    lookups = [dict(zip(df["month"], df["balance"])) for df in [home_df, car_df, credit_df, personal_df, inv_df]]
    home_lookup, car_lookup, credit_lookup, personal_lookup, inv_lookup = lookups

    rows = []
    for m in range(months + 1):
        age = settings["current_age"] + m / 12
        portfolio = portfolio_values[m]
        super_balance = super_values[m]
        dividend_income = portfolio * dividend_yield
        super_income = super_balance * super_drawdown if age >= settings["super_access_age"] else 0
        post60_retirement_income = dividend_income + super_income
        target_income = settings["target_income"] * ((1 + inflation_rate) ** (m / 12))

        home = home_lookup.get(m, 0)
        car = car_lookup.get(m, 0)
        credit = credit_lookup.get(m, 0)
        personal = personal_lookup.get(m, 0)
        bad_debt = home + car + credit + personal
        investment_loan = inv_lookup.get(m, 0)

        # Key corrected logic:
        # Before super access, only dividend income is tested against the target.
        # From super access onward, dividend income + super income is tested.
        # Target income is assumed to include lifestyle + investment loan servicing requirement.
        if age < settings["super_access_age"]:
            income_test = dividend_income
        else:
            income_test = post60_retirement_income

        financial_freedom = bad_debt <= 0 and income_test >= target_income

        rows.append({
            "month": m,
            "age": age,
            "portfolio": portfolio,
            "super": super_balance,
            "dividend_income": dividend_income,
            "super_income": super_income,
            "retirement_income": post60_retirement_income,
            "target_income": target_income,
            "home_loan": home,
            "car_loan": car,
            "credit_card": credit,
            "personal_loan": personal,
            "bad_debt": bad_debt,
            "investment_loan": investment_loan,
            "financial_freedom": financial_freedom,
        })
    return pd.DataFrame(rows)

def first_true_age(df, column):
    hits = df[df[column] == True]
    return None if hits.empty else float(hits.iloc[0]["age"])

def first_zero_bad_debt_age(df):
    hits = df[df["bad_debt"] <= 0]
    return None if hits.empty else float(hits.iloc[0]["age"])

def pre_super_check(df, settings):
    pre = df[(df["age"] >= settings["target_retirement_age"]) & (df["age"] < settings["super_access_age"]) & (df["month"] % 12 == 0)]
    if pre.empty:
        return {"required": 0, "dividends": 0, "cash": settings.get("cash_balance", 0), "gap": 0, "ready": False}
    required = pre["target_income"].sum()
    dividends = pre["dividend_income"].sum()
    cash = settings.get("cash_balance", 0)
    gap = required - dividends - cash
    return {"required": required, "dividends": dividends, "cash": cash, "gap": gap, "ready": gap <= 0}

def post_super_check(df, settings):
    post = df[(df["age"] >= settings["super_access_age"]) & (df["month"] % 12 == 0)].copy()
    if post.empty:
        return {"ready_age": None}
    post["ready"] = post["retirement_income"] >= post["target_income"]
    hit = post[post["ready"]]
    return {"ready_age": None if hit.empty else float(hit.iloc[0]["age"])}

def load_history():
    if SNAPSHOT_PATH.exists():
        return pd.read_csv(SNAPSHOT_PATH)
    return pd.DataFrame()

def calculate_history_growth(history):
    if history.empty or len(history) < 2:
        return {"portfolio_monthly": None, "portfolio_3m": None, "portfolio_12m": None, "super_monthly": None, "super_3m": None, "super_12m": None}
    history = history.sort_values("month").reset_index(drop=True)
    def growth(column, periods):
        if len(history) <= periods or column not in history.columns:
            return None
        old = history[column].iloc[-1 - periods]
        new = history[column].iloc[-1]
        if old == 0:
            return None
        return (new / old - 1) * 100
    return {
        "portfolio_monthly": growth("portfolio_value", 1),
        "portfolio_3m": growth("portfolio_value", 3),
        "portfolio_12m": growth("portfolio_value", 12),
        "super_monthly": growth("combined_super", 1),
        "super_3m": growth("combined_super", 3),
        "super_12m": growth("combined_super", 12),
    }

def format_growth(value):
    if value is None or pd.isna(value):
        return "—"
    return f"{value:.1f}%"

def card(title, value, note="", status=""):
    status_class = {"good": "status-good", "watch": "status-watch", "bad": "status-bad"}.get(status, "")
    st.markdown(f"""
    <div class="metric-card">
        <div class="eyebrow">{title}</div>
        <div class="value {status_class}">{value}</div>
        <div class="note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def style_plot(fig, height=350):
    fig.update_layout(
        height=height,
        template="plotly_white",
        margin=dict(l=10, r=10, t=30, b=20),
        font=dict(family="Inter", size=12, color="#334155"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#eef2f7", zerolinecolor="#e5e7eb")
    return fig

settings = load_settings()

st.sidebar.title("Inputs")
st.sidebar.caption("Manual values. Forecasts and history are calculated automatically.")

with st.sidebar.expander("Core Assumptions", expanded=True):
    settings["current_age"] = st.number_input("Current Age", value=float(settings["current_age"]), step=0.5, help="Your current age. Used as the starting point for all forecasts.")
    settings["target_retirement_age"] = st.number_input("Target Retirement Age", value=float(settings["target_retirement_age"]), step=0.5, help="Age you are testing as the point where work may become optional. The 55-60 check starts here.")
    settings["target_income"] = st.number_input("Target Annual Income", value=int(settings["target_income"]), step=5000, help="Annual income required from age 55 onward. This should include lifestyle costs and investment loan servicing.")
    settings["inflation_rate_pct"] = st.number_input("Inflation Assumption %", value=float(settings["inflation_rate_pct"]), step=0.1, format="%.1f", help="Planning assumption used to increase target income over time.")

with st.sidebar.expander("Investment Portfolio"):
    settings["current_portfolio"] = st.number_input("Portfolio Value", value=int(settings["current_portfolio"]), step=10000, help="Current value of non-super investments.")
    settings["monthly_investment"] = st.number_input("Monthly Investment", value=int(settings["monthly_investment"]), step=500, help="Monthly contribution to the investment portfolio.")
    settings["dividend_yield_pct"] = st.number_input("Dividend Yield %", value=float(settings["dividend_yield_pct"]), step=0.1, format="%.1f", help="Expected annual dividend yield from the investment portfolio.")
    settings["portfolio_growth_rate_pct"] = st.number_input("Long-Term Forecast Growth %", value=float(settings["portfolio_growth_rate_pct"]), step=0.1, format="%.1f", help="Long-term capital growth assumption for the investment portfolio.")

with st.sidebar.expander("Superannuation"):
    settings["super_balance_1"] = st.number_input("Super Balance 1", value=int(settings["super_balance_1"]), step=10000, help="First superannuation balance.")
    settings["super_balance_2"] = st.number_input("Super Balance 2", value=int(settings["super_balance_2"]), step=10000, help="Second superannuation balance.")
    st.info(f"Combined Super: {money(settings['super_balance_1'] + settings['super_balance_2'])}")
    settings["super_growth_rate_pct"] = st.number_input("Long-Term Super Growth %", value=float(settings["super_growth_rate_pct"]), step=0.1, format="%.1f", help="Growth assumption applied to combined super.")
    settings["super_drawdown_pct"] = st.number_input("Super Drawdown %", value=float(settings["super_drawdown_pct"]), step=0.1, format="%.1f", help="Annual income assumed from super after age 60.")

with st.sidebar.expander("Bad Debt"):
    st.markdown("**Home Loan**")
    settings["home_loan_balance"] = st.number_input("Home Loan Balance", value=int(settings["home_loan_balance"]), step=10000, help="Remaining home loan balance.")
    settings["home_loan_interest_pct"] = st.number_input("Home Loan Interest %", value=float(settings["home_loan_interest_pct"]), step=0.1, format="%.1f")
    settings["home_loan_monthly_repayment"] = st.number_input("Home Loan Monthly Repayment", value=int(settings["home_loan_monthly_repayment"]), step=500)

    st.markdown("**Car Loan**")
    settings["car_loan_balance"] = st.number_input("Car Loan Balance", value=int(settings["car_loan_balance"]), step=1000)
    settings["car_loan_interest_pct"] = st.number_input("Car Loan Interest %", value=float(settings["car_loan_interest_pct"]), step=0.1, format="%.1f")
    settings["car_loan_monthly_repayment"] = st.number_input("Car Loan Monthly Repayment", value=int(settings["car_loan_monthly_repayment"]), step=100)

    st.markdown("**Credit Card**")
    settings["credit_card_balance"] = st.number_input("Credit Card Balance", value=int(settings["credit_card_balance"]), step=500)
    settings["credit_card_interest_pct"] = st.number_input("Credit Card Interest %", value=float(settings["credit_card_interest_pct"]), step=0.1, format="%.1f")
    settings["credit_card_monthly_repayment"] = st.number_input("Credit Card Monthly Repayment", value=int(settings["credit_card_monthly_repayment"]), step=100)

    st.markdown("**Other Personal Loan**")
    settings["personal_loan_balance"] = st.number_input("Personal Loan Balance", value=int(settings["personal_loan_balance"]), step=1000)
    settings["personal_loan_interest_pct"] = st.number_input("Personal Loan Interest %", value=float(settings["personal_loan_interest_pct"]), step=0.1, format="%.1f")
    settings["personal_loan_monthly_repayment"] = st.number_input("Personal Loan Monthly Repayment", value=int(settings["personal_loan_monthly_repayment"]), step=100)

    settings["extra_bad_debt_repayment"] = st.number_input("Extra Bad Debt Repayment", value=int(settings["extra_bad_debt_repayment"]), step=500, help="Extra monthly repayment applied to bad debt. The scenario slider also uses this.")

with st.sidebar.expander("Investment Loan"):
    settings["investment_loan_balance"] = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000, help="Good debt used for investments. This is not included in bad debt.")
    settings["investment_loan_interest_pct"] = st.number_input("Investment Loan Interest %", value=float(settings["investment_loan_interest_pct"]), step=0.1, format="%.1f")
    settings["investment_loan_monthly_repayment"] = st.number_input("Investment Loan Monthly Repayment", value=int(settings["investment_loan_monthly_repayment"]), step=500, help="Monthly investment loan repayment. Target income should be set high enough to cover this plus lifestyle costs.")

with st.sidebar.expander("Cash"):
    settings["cash_balance"] = st.number_input("Cash Balance", value=int(settings.get("cash_balance", 0)), step=1000, help="Cash available to support the 55-60 period.")

if st.sidebar.button("Save Inputs", use_container_width=True):
    save_settings(settings)
    st.sidebar.success("Inputs saved")

forecast = build_forecast(settings)
annual = forecast[forecast["month"] % 12 == 0].copy()
freedom_age = first_true_age(forecast, "financial_freedom")
bad_debt_free_age = first_zero_bad_debt_age(forecast)
pre60 = pre_super_check(forecast, settings)
post60 = post_super_check(forecast, settings)

combined_super = settings["super_balance_1"] + settings["super_balance_2"]
total_bad_debt = calculate_total_bad_debt(settings)
total_bad_debt_repayment = calculate_total_bad_debt_repayment(settings)
current_dividends = settings["current_portfolio"] * pct_to_rate(settings["dividend_yield_pct"])
years_remaining = None if freedom_age is None else max(freedom_age - settings["current_age"], 0)
net_investable_assets = settings["current_portfolio"] + combined_super + settings.get("cash_balance", 0)
net_position = net_investable_assets - total_bad_debt - settings["investment_loan_balance"]

history = load_history()
growth = calculate_history_growth(history)

if freedom_age is None:
    exec_message = "Based on the current assumptions, Financial Freedom is not reached within the forecast period. The key check is whether dividends can cover the 55-60 period and whether dividends plus super can cover the target income from age 60."
else:
    exec_message = f"Based on the current assumptions, Financial Freedom is projected at age {freedom_age:.1f}, approximately {years_remaining:.1f} years from today. The 55-60 period is tested using dividends and cash; from age {settings['super_access_age']:.0f}, super income is included."

st.title("Financial Freedom Planner")
st.markdown('<div class="exec-subtitle">A roadmap to making work optional</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="executive-summary">
    <div class="label">Executive Summary</div>
    <div class="text">{exec_message}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    status = "good" if freedom_age is not None and freedom_age <= settings["target_retirement_age"] else "watch"
    card("Financial Freedom", age_text(freedom_age), years_text(years_remaining), status)
with c2:
    status = "good" if pre60["ready"] else "bad"
    card("Age 55–60 Check", "Ready" if pre60["ready"] else money(pre60["gap"]), "Gap after dividends and cash", status)
with c3:
    status = "good" if bad_debt_free_age is not None and bad_debt_free_age <= settings["target_retirement_age"] else "watch"
    card("Debt Freedom", age_text(bad_debt_free_age), f"{money(total_bad_debt)} bad debt remaining", status)
with c4:
    status = "good" if post60["ready_age"] is not None and post60["ready_age"] <= settings["super_access_age"] else "watch"
    card("Post-60 Income", age_text(post60["ready_age"]), "Dividends + super vs target", status)

p1, p2, p3, p4 = st.columns(4)
with p1:
    st.metric("Target Annual Income", money(settings["target_income"]), help="Core assumption. This should cover lifestyle and investment loan servicing.")
with p2:
    st.metric("Portfolio Dividends", money(current_dividends), help="Current annual dividend income from the investment portfolio.")
with p3:
    st.metric("Combined Super", money(combined_super), help="Super Balance 1 plus Super Balance 2.")
with p4:
    st.metric("Net Position", money(net_position), help="Investable assets less bad debt and investment loan.")

st.divider()

left, centre, right = st.columns([1.0, 1.5, 1.5])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Freedom Logic</div><div class="panel-subtitle">The dashboard checks two separate periods.</div>', unsafe_allow_html=True)
    st.markdown(f"""
    **1. Age {settings['target_retirement_age']:.0f}–{settings['super_access_age']:.0f}: pre-super period**  
    Dividends + cash must cover the target income.

    **2. Age {settings['super_access_age']:.0f} onward: super enabled**  
    Dividends + super income must cover the target income.

    **Bad debt must be cleared** before work becomes optional.
    """)
    st.markdown("#### Actual Growth")
    st.write(f"Portfolio monthly: **{format_growth(growth['portfolio_monthly'])}**")
    st.write(f"Portfolio 3-month: **{format_growth(growth['portfolio_3m'])}**")
    st.write(f"Portfolio 12-month: **{format_growth(growth['portfolio_12m'])}**")
    st.write(f"Super monthly: **{format_growth(growth['super_monthly'])}**")
    st.write(f"Super 3-month: **{format_growth(growth['super_3m'])}**")
    st.write(f"Super 12-month: **{format_growth(growth['super_12m'])}**")
    st.markdown('</div>', unsafe_allow_html=True)

with centre:
    st.markdown('<div class="panel"><div class="panel-title">Age 55–60 Independence Check</div><div class="panel-subtitle">Critical pre-super period. This chart deliberately excludes super.</div>', unsafe_allow_html=True)
    pre_df = forecast[(forecast["age"] >= settings["target_retirement_age"]) & (forecast["age"] <= settings["super_access_age"]) & (forecast["month"] % 12 == 0)]
    fig_pre = go.Figure()
    fig_pre.add_trace(go.Scatter(x=pre_df["age"], y=pre_df["target_income"], mode="lines+markers", name="Target income", line=dict(color="#94a3b8", width=3, dash="dash")))
    fig_pre.add_trace(go.Scatter(x=pre_df["age"], y=pre_df["dividend_income"], mode="lines+markers", name="Dividend income", line=dict(color="#0f3b68", width=4)))
    fig_pre.add_vline(x=settings["target_retirement_age"], line_width=2, line_dash="dot", line_color="#d97706")
    fig_pre.add_annotation(x=settings["target_retirement_age"], y=pre_df["target_income"].max(), text="Target retirement age", showarrow=False, yshift=18, font=dict(color="#d97706"))
    st.plotly_chart(style_plot(fig_pre, height=400), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">Bad Debt Reduction</div><div class="panel-subtitle">Shows how many years to remove bad debt. Impacted by extra repayments.</div>', unsafe_allow_html=True)
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Scatter(x=annual["age"], y=annual["bad_debt"], mode="lines", name="Total bad debt", line=dict(color="#dc2626", width=4)))
    fig_debt.add_trace(go.Scatter(x=annual["age"], y=annual["home_loan"], mode="lines", name="Home loan", line=dict(color="#0f3b68", width=3, dash="dot")))
    if bad_debt_free_age is not None:
        fig_debt.add_vline(x=bad_debt_free_age, line_width=2, line_dash="dot", line_color="#16a34a")
    st.plotly_chart(style_plot(fig_debt, height=400), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

a, b, c = st.columns(3)

with a:
    st.markdown('<div class="panel"><div class="panel-title">Bad Debt Breakdown</div><div class="panel-subtitle">What needs to be cleared before work is optional.</div>', unsafe_allow_html=True)
    debt_now = pd.DataFrame({"Debt": ["Home Loan", "Car Loan", "Credit Card", "Personal Loan"], "Balance": [settings["home_loan_balance"], settings["car_loan_balance"], settings["credit_card_balance"], settings["personal_loan_balance"]]})
    st.metric("Total Bad Debt", money(total_bad_debt), help="All bad debt balances added together.")
    st.metric("Monthly Servicing", money(total_bad_debt_repayment), help="Total monthly repayments across all bad debt plus extra repayment.")
    debt_bar = px.bar(debt_now, x="Debt", y="Balance")
    debt_bar.update_traces(marker_color="#0f3b68")
    st.plotly_chart(style_plot(debt_bar, height=260), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="panel"><div class="panel-title">55–60 Funding Summary</div><div class="panel-subtitle">This replaces the old confusing bridge concept.</div>', unsafe_allow_html=True)
    st.metric("Required 55–60", money(pre60["required"]), help="Total target income required from target retirement age to super access age.")
    st.metric("Dividends 55–60", money(pre60["dividends"]), help="Projected dividend income during the same period.")
    st.metric("Cash Available", money(pre60["cash"]), help="Cash balance included as part of the pre-super funding check.")
    st.metric("Pre-Super Gap", money(pre60["gap"]), help="Required income minus dividends and cash. If positive, the 55-60 period is not fully funded.")
    st.markdown('</div>', unsafe_allow_html=True)

with c:
    st.markdown('<div class="panel"><div class="panel-title">Post-60 Income Mix</div><div class="panel-subtitle">After super access, income comes from dividends and super.</div>', unsafe_allow_html=True)
    post_df = forecast[(forecast["age"] >= settings["super_access_age"]) & (forecast["age"] <= settings["super_access_age"] + 10) & (forecast["month"] % 12 == 0)].copy()
    fig_post = go.Figure()
    fig_post.add_trace(go.Bar(x=post_df["age"], y=post_df["dividend_income"], name="Dividends", marker_color="#0f3b68"))
    fig_post.add_trace(go.Bar(x=post_df["age"], y=post_df["super_income"], name="Super income", marker_color="#16a34a"))
    fig_post.add_trace(go.Scatter(x=post_df["age"], y=post_df["target_income"], mode="lines", name="Target income", line=dict(color="#94a3b8", width=3, dash="dash")))
    fig_post.update_layout(barmode="stack")
    st.plotly_chart(style_plot(fig_post, height=345), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.subheader("Scenario Test")
st.caption("These levers recalculate the full forecast: 55–60 income check, bad debt reduction, and post-60 retirement income.")

s1, s2, s3, s4 = st.columns(4)
with s1:
    scenario_income = st.slider("Target income", 80000, 180000, int(settings["target_income"]), 5000, help="Scenario target annual income.")
with s2:
    scenario_monthly_investment = st.slider("Monthly investment", 0, 10000, int(settings["monthly_investment"]), 500, help="Scenario monthly investment. Impacts portfolio growth and dividend income.")
with s3:
    scenario_extra_debt = st.slider("Extra bad debt repayment", 0, 10000, int(settings["extra_bad_debt_repayment"]), 500, help="Scenario extra monthly repayment against bad debt. Impacts bad debt free age.")
with s4:
    scenario_growth_pct = st.slider("Portfolio growth %", 0.0, 12.0, float(settings["portfolio_growth_rate_pct"]), 0.1, help="Scenario long-term portfolio capital growth assumption.")

scenario_settings = settings.copy()
scenario_settings["target_income"] = scenario_income
scenario_settings["monthly_investment"] = scenario_monthly_investment
scenario_settings["extra_bad_debt_repayment"] = scenario_extra_debt
scenario_settings["portfolio_growth_rate_pct"] = scenario_growth_pct

scenario_df = build_forecast(scenario_settings)
scenario_age = first_true_age(scenario_df, "financial_freedom")
scenario_bad_debt_age = first_zero_bad_debt_age(scenario_df)
scenario_pre60 = pre_super_check(scenario_df, scenario_settings)
scenario_post60 = post_super_check(scenario_df, scenario_settings)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Scenario Freedom Age", age_text(scenario_age), help="Projected financial freedom age using all scenario levers.")
with m2:
    st.metric("Scenario Bad Debt Free Age", age_text(scenario_bad_debt_age), help="Bad debt free age after applying scenario extra repayments.")
with m3:
    st.metric("Scenario 55–60 Gap", money(scenario_pre60["gap"]), help="Pre-super funding gap after applying scenario levers.")
with m4:
    if freedom_age is None or scenario_age is None:
        movement_label = "—"
    else:
        movement = scenario_age - freedom_age
        movement_label = f"{movement:+.1f} years"
    st.metric("Movement vs Base Case", movement_label, help="Scenario Financial Freedom Age minus Base Case Financial Freedom Age. Negative is better because it means work becomes optional earlier.")

st.divider()

st.subheader("Monthly Snapshot & History")
st.caption("Dummy data has been pre-loaded so you can see the history view. Save current values once per month to build your real history.")

snap_left, snap_right = st.columns([1, 2])
with snap_left:
    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    snapshot_notes = st.text_area("Notes", height=80)
    if st.button("Save Current Month Snapshot", use_container_width=True):
        expected_columns = ["month", "portfolio_value", "super_balance_1", "super_balance_2", "combined_super", "home_loan_balance", "car_loan_balance", "credit_card_balance", "personal_loan_balance", "total_bad_debt", "investment_loan_balance", "cash_balance", "annual_dividend_income", "notes"]
        if SNAPSHOT_PATH.exists():
            snapshot_history = pd.read_csv(SNAPSHOT_PATH)
        else:
            snapshot_history = pd.DataFrame(columns=expected_columns)
        for col in expected_columns:
            if col not in snapshot_history.columns:
                snapshot_history[col] = None
        new_row = {
            "month": month,
            "portfolio_value": settings["current_portfolio"],
            "super_balance_1": settings["super_balance_1"],
            "super_balance_2": settings["super_balance_2"],
            "combined_super": settings["super_balance_1"] + settings["super_balance_2"],
            "home_loan_balance": settings["home_loan_balance"],
            "car_loan_balance": settings["car_loan_balance"],
            "credit_card_balance": settings["credit_card_balance"],
            "personal_loan_balance": settings["personal_loan_balance"],
            "total_bad_debt": calculate_total_bad_debt(settings),
            "investment_loan_balance": settings["investment_loan_balance"],
            "cash_balance": settings.get("cash_balance", 0),
            "annual_dividend_income": settings["current_portfolio"] * pct_to_rate(settings["dividend_yield_pct"]),
            "notes": snapshot_notes,
        }
        snapshot_history = snapshot_history[snapshot_history["month"] != month]
        snapshot_history = pd.concat([snapshot_history, pd.DataFrame([new_row])], ignore_index=True)
        snapshot_history = snapshot_history[expected_columns]
        snapshot_history.to_csv(SNAPSHOT_PATH, index=False)
        st.success("Snapshot saved")

with snap_right:
    snapshot_history = load_history()
    if not snapshot_history.empty:
        snapshot_history = snapshot_history.sort_values("month")
        hist_fig = go.Figure()
        for col, name, color in [("portfolio_value", "Portfolio", "#0f3b68"), ("combined_super", "Combined super", "#2563eb"), ("total_bad_debt", "Bad debt", "#dc2626"), ("investment_loan_balance", "Investment loan", "#d97706")]:
            if col in snapshot_history.columns:
                hist_fig.add_trace(go.Scatter(x=snapshot_history["month"], y=snapshot_history[col], mode="lines+markers", name=name, line=dict(color=color, width=3)))
        st.plotly_chart(style_plot(hist_fig, height=330), use_container_width=True)
        with st.expander("View snapshot table"):
            st.dataframe(snapshot_history, use_container_width=True)
    else:
        st.info("No monthly snapshots saved yet.")
