
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    "home_loan_balance": 300000,
    "home_loan_interest_pct": 6.0,
    "home_loan_monthly_repayment": 4000,
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
    "investment_loan_balance": 100000,
    "investment_loan_interest_pct": 0.0,
    "investment_loan_monthly_repayment": 1000,
    "cash_balance": 25000,
}

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    padding-top: 2.0rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0f1f33 100%);
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stTextArea label {
    color: #e5e7eb !important;
}

[data-testid="stSidebar"] summary {
    background-color: rgba(255,255,255,0.06);
    border-radius: 10px;
}

h1 {
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #0f172a;
}

h2, h3 {
    color: #0f172a;
    letter-spacing: -0.03em;
}

.exec-subtitle {
    color: #64748b;
    font-size: 1.0rem;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
}

.executive-summary {
    background: linear-gradient(135deg, #0f172a 0%, #172554 100%);
    color: #ffffff;
    padding: 22px 26px;
    border-radius: 18px;
    margin: 18px 0 24px 0;
    box-shadow: 0 14px 35px rgba(15, 23, 42, 0.18);
}

.executive-summary .label {
    color: #93c5fd;
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 7px;
}

.executive-summary .text {
    font-size: 1.15rem;
    line-height: 1.55;
    font-weight: 500;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px 18px 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    min-height: 135px;
}

.metric-card .eyebrow {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-card .value {
    font-size: 1.95rem;
    color: #0f172a;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-top: 6px;
}

.metric-card .note {
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 6px;
}

.status-good {
    color: #16a34a !important;
}

.status-watch {
    color: #d97706 !important;
}

.status-bad {
    color: #dc2626 !important;
}

.panel {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 26px rgba(15, 23, 42, 0.055);
    margin-bottom: 20px;
}

.panel-title {
    font-weight: 800;
    font-size: 1.2rem;
    color: #0f172a;
    margin-bottom: 6px;
}

.panel-subtitle {
    color: #64748b;
    font-size: 0.88rem;
    margin-bottom: 12px;
}

.roadmap-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
}

.roadmap-dot {
    min-width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #dbeafe;
    color: #1d4ed8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 800;
}

.roadmap-title {
    font-weight: 800;
    color: #0f172a;
}

.roadmap-note {
    color: #64748b;
    font-size: 0.85rem;
}

.small-table {
    font-size: 0.9rem;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 14px 16px;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)


# ---------- Helpers ----------
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

def debt_paydown(balance, annual_interest_rate, monthly_repayment, extra_repayment=0, months=600):
    rows = []
    debt = float(balance)
    monthly_rate = annual_interest_rate / 12
    payment = float(monthly_repayment) + float(extra_repayment)
    for m in range(months + 1):
        rows.append({"month": m, "balance": max(debt, 0)})
        if debt <= 0:
            break
        interest = debt * monthly_rate
        principal = max(payment - interest, 0)
        debt = debt - principal
        if payment <= interest and debt > 0:
            break
    return pd.DataFrame(rows)

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
    combined_super = settings["super_balance_1"] + settings["super_balance_2"]

    portfolio_values = future_value_monthly(settings["current_portfolio"], settings["monthly_investment"], portfolio_growth, months)
    super_values = future_value_monthly(combined_super, 0, super_growth, months)

    home_df = debt_paydown(settings["home_loan_balance"], pct_to_rate(settings["home_loan_interest_pct"]), settings["home_loan_monthly_repayment"], settings["extra_bad_debt_repayment"], months)
    car_df = debt_paydown(settings["car_loan_balance"], pct_to_rate(settings["car_loan_interest_pct"]), settings["car_loan_monthly_repayment"], 0, months)
    credit_df = debt_paydown(settings["credit_card_balance"], pct_to_rate(settings["credit_card_interest_pct"]), settings["credit_card_monthly_repayment"], 0, months)
    personal_df = debt_paydown(settings["personal_loan_balance"], pct_to_rate(settings["personal_loan_interest_pct"]), settings["personal_loan_monthly_repayment"], 0, months)
    inv_loan_df = debt_paydown(settings["investment_loan_balance"], pct_to_rate(settings["investment_loan_interest_pct"]), settings["investment_loan_monthly_repayment"], 0, months)

    def lookup(df):
        return dict(zip(df["month"], df["balance"]))

    home_lookup = lookup(home_df)
    car_lookup = lookup(car_df)
    credit_lookup = lookup(credit_df)
    personal_lookup = lookup(personal_df)
    inv_lookup = lookup(inv_loan_df)

    rows = []
    current_age = settings["current_age"]
    for m in range(months + 1):
        age = current_age + m / 12
        portfolio = portfolio_values[m]
        super_balance = super_values[m]
        dividend_income = portfolio * dividend_yield
        target_income = settings["target_income"] * ((1 + inflation_rate) ** (m / 12))
        home = home_lookup.get(m, 0)
        car = car_lookup.get(m, 0)
        credit = credit_lookup.get(m, 0)
        personal = personal_lookup.get(m, 0)
        total_bad_debt = home + car + credit + personal
        investment_loan = inv_lookup.get(m, 0)
        investment_loan_payment_annual = settings["investment_loan_monthly_repayment"] * 12 if investment_loan > 0 else 0
        financial_freedom = total_bad_debt <= 0 and dividend_income >= target_income + investment_loan_payment_annual

        rows.append({
            "month": m,
            "age": age,
            "portfolio": portfolio,
            "super": super_balance,
            "dividend_income": dividend_income,
            "target_income": target_income,
            "home_loan": home,
            "car_loan": car,
            "credit_card": credit,
            "personal_loan": personal,
            "bad_debt": total_bad_debt,
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

def bridge_summary(df, settings):
    bridge = df[(df["age"] >= settings["target_retirement_age"]) & (df["age"] < settings["super_access_age"])].copy()
    if bridge.empty:
        return {"bridge_required": 0, "bridge_income": 0, "bridge_gap": 0}
    annual_rows = bridge[bridge["month"] % 12 == 0]
    bridge_required = annual_rows["target_income"].sum()
    bridge_income = annual_rows["dividend_income"].sum()
    return {"bridge_required": bridge_required, "bridge_income": bridge_income, "bridge_gap": bridge_required - bridge_income}

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
    status_class = {
        "good": "status-good",
        "watch": "status-watch",
        "bad": "status-bad",
    }.get(status, "")
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


# ---------- Inputs ----------
settings = load_settings()

st.sidebar.title("Inputs")
st.sidebar.caption("Manual values. Forecasts and history are calculated automatically.")

with st.sidebar.expander("Core Assumptions", expanded=True):
    settings["current_age"] = st.number_input("Current Age", value=float(settings["current_age"]), step=0.5)
    settings["target_retirement_age"] = st.number_input("Target Retirement Age", value=float(settings["target_retirement_age"]), step=0.5)
    settings["target_income"] = st.number_input("Target Annual Income", value=int(settings["target_income"]), step=5000)
    settings["inflation_rate_pct"] = st.number_input("Inflation Assumption %", value=float(settings["inflation_rate_pct"]), step=0.1, format="%.1f")

with st.sidebar.expander("Investment Portfolio"):
    settings["current_portfolio"] = st.number_input("Portfolio Value", value=int(settings["current_portfolio"]), step=10000)
    settings["monthly_investment"] = st.number_input("Monthly Investment", value=int(settings["monthly_investment"]), step=500)
    settings["dividend_yield_pct"] = st.number_input("Dividend Yield %", value=float(settings["dividend_yield_pct"]), step=0.1, format="%.1f")
    settings["portfolio_growth_rate_pct"] = st.number_input("Long-Term Forecast Growth %", value=float(settings["portfolio_growth_rate_pct"]), step=0.1, format="%.1f")

with st.sidebar.expander("Superannuation"):
    settings["super_balance_1"] = st.number_input("Super Balance 1", value=int(settings["super_balance_1"]), step=10000)
    settings["super_balance_2"] = st.number_input("Super Balance 2", value=int(settings["super_balance_2"]), step=10000)
    st.info(f"Combined Super: {money(settings['super_balance_1'] + settings['super_balance_2'])}")
    settings["super_growth_rate_pct"] = st.number_input("Long-Term Super Growth %", value=float(settings["super_growth_rate_pct"]), step=0.1, format="%.1f")

with st.sidebar.expander("Bad Debt"):
    st.markdown("**Home Loan**")
    settings["home_loan_balance"] = st.number_input("Home Loan Balance", value=int(settings["home_loan_balance"]), step=10000)
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

    settings["extra_bad_debt_repayment"] = st.number_input("Extra Bad Debt Repayment", value=int(settings["extra_bad_debt_repayment"]), step=500)

with st.sidebar.expander("Investment Loan"):
    settings["investment_loan_balance"] = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000)
    settings["investment_loan_interest_pct"] = st.number_input("Investment Loan Interest %", value=float(settings["investment_loan_interest_pct"]), step=0.1, format="%.1f")
    settings["investment_loan_monthly_repayment"] = st.number_input("Investment Loan Monthly Repayment", value=int(settings["investment_loan_monthly_repayment"]), step=500)

with st.sidebar.expander("Cash"):
    settings["cash_balance"] = st.number_input("Cash Balance", value=int(settings.get("cash_balance", 0)), step=1000)

if st.sidebar.button("Save Inputs", use_container_width=True):
    save_settings(settings)
    st.sidebar.success("Inputs saved")


# ---------- Calculations ----------
forecast = build_forecast(settings)
annual = forecast[forecast["month"] % 12 == 0].copy()
freedom_age = first_true_age(forecast, "financial_freedom")
bad_debt_free_age = first_zero_bad_debt_age(forecast)
bridge = bridge_summary(forecast, settings)

combined_super = settings["super_balance_1"] + settings["super_balance_2"]
total_bad_debt = calculate_total_bad_debt(settings)
total_bad_debt_repayment = calculate_total_bad_debt_repayment(settings)
current_dividends = settings["current_portfolio"] * pct_to_rate(settings["dividend_yield_pct"])
freedom_ratio = current_dividends / settings["target_income"] if settings["target_income"] else 0
years_remaining = None if freedom_age is None else max(freedom_age - settings["current_age"], 0)
net_investable_assets = settings["current_portfolio"] + combined_super + settings.get("cash_balance", 0)
net_position = net_investable_assets - total_bad_debt - settings["investment_loan_balance"]

history = load_history()
growth = calculate_history_growth(history)

if freedom_age is None:
    exec_message = "Based on the current assumptions, Financial Freedom is not reached within the forecast period. The primary constraint is the gap between passive income and the target lifestyle income."
else:
    exec_message = f"Based on the current assumptions, Financial Freedom is projected at age {freedom_age:.1f}, approximately {years_remaining:.1f} years from today. The key milestones are clearing bad debt at age {age_text(bad_debt_free_age)} and closing the retirement bridge gap of {money(bridge['bridge_gap'])}."

# ---------- Dashboard ----------
st.title("Financial Freedom Planner")
st.markdown('<div class="exec-subtitle">A roadmap to making work optional</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="executive-summary">
    <div class="label">Executive Summary</div>
    <div class="text">{exec_message}</div>
</div>
""", unsafe_allow_html=True)

# Hero cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    status = "good" if freedom_age is not None and freedom_age <= settings["target_retirement_age"] else "watch"
    card("Financial Freedom", age_text(freedom_age), years_text(years_remaining), status)
with c2:
    status = "good" if freedom_ratio >= 1 else "watch" if freedom_ratio >= 0.6 else "bad"
    card("Income Replacement", f"{freedom_ratio:.0%}", f"{money(current_dividends)} annual dividends", status)
with c3:
    status = "good" if bad_debt_free_age is not None and bad_debt_free_age <= settings["target_retirement_age"] else "watch"
    card("Debt Freedom", age_text(bad_debt_free_age), f"{money(total_bad_debt)} bad debt remaining", status)
with c4:
    status = "good" if bridge["bridge_gap"] <= 0 else "bad"
    bridge_note = "Bridge funded" if bridge["bridge_gap"] <= 0 else "Needs attention"
    card("Retirement Bridge", money(bridge["bridge_gap"]), bridge_note, status)

st.markdown("")

# Current position
p1, p2, p3, p4 = st.columns(4)
with p1:
    st.metric("Investable Assets", money(net_investable_assets), help="Portfolio + combined super + cash.")
with p2:
    st.metric("Portfolio Value", money(settings["current_portfolio"]), help="Current non-super investment portfolio.")
with p3:
    st.metric("Combined Super", money(combined_super), help="Super Balance 1 plus Super Balance 2.")
with p4:
    st.metric("Net Position", money(net_position), help="Investable assets less bad debt and investment loan.")

st.divider()

# Main charts
left, centre, right = st.columns([1.05, 1.45, 1.45])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Freedom Roadmap</div><div class="panel-subtitle">Major milestones from today to work optional.</div>', unsafe_allow_html=True)

    roadmap = [
        ("Today", f"Age {settings['current_age']:.1f}", True),
        ("Bad Debt Cleared", f"Age {age_text(bad_debt_free_age)}", bad_debt_free_age is not None),
        ("Super Available", f"Age {settings['super_access_age']:.1f}", True),
        ("Bridge Ready", "Funded" if bridge["bridge_gap"] <= 0 else f"Gap {money(bridge['bridge_gap'])}", bridge["bridge_gap"] <= 0),
        ("Financial Freedom", f"Age {age_text(freedom_age)}", freedom_age is not None),
    ]

    for i, (title, note, done) in enumerate(roadmap, start=1):
        icon = "✓" if done else "!"
        st.markdown(f"""
        <div class="roadmap-item">
            <div class="roadmap-dot">{icon}</div>
            <div>
                <div class="roadmap-title">{title}</div>
                <div class="roadmap-note">{note}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <br>
        <div class="panel-title">Actual Growth</div>
        <div class="panel-subtitle">Calculated from monthly snapshots.</div>
    """, unsafe_allow_html=True)

    st.write(f"Portfolio monthly: **{format_growth(growth['portfolio_monthly'])}**")
    st.write(f"Portfolio 3-month: **{format_growth(growth['portfolio_3m'])}**")
    st.write(f"Portfolio 12-month: **{format_growth(growth['portfolio_12m'])}**")
    st.write(f"Super monthly: **{format_growth(growth['super_monthly'])}**")
    st.write(f"Super 3-month: **{format_growth(growth['super_3m'])}**")
    st.write(f"Super 12-month: **{format_growth(growth['super_12m'])}**")
    st.markdown('</div>', unsafe_allow_html=True)

with centre:
    st.markdown('<div class="panel"><div class="panel-title">Income Forecast</div><div class="panel-subtitle">Dividend income compared with target lifestyle income.</div>', unsafe_allow_html=True)

    fig_income = go.Figure()
    fig_income.add_trace(go.Scatter(
        x=annual["age"], y=annual["target_income"],
        mode="lines",
        name="Target income",
        line=dict(color="#94a3b8", width=3, dash="dash")
    ))
    fig_income.add_trace(go.Scatter(
        x=annual["age"], y=annual["dividend_income"],
        mode="lines",
        name="Dividend income",
        line=dict(color="#0f3b68", width=4)
    ))

    if freedom_age is not None:
        point = annual.iloc[(annual["age"] - freedom_age).abs().argsort()[:1]]
        fig_income.add_trace(go.Scatter(
            x=point["age"], y=point["dividend_income"],
            mode="markers+text",
            name="Freedom point",
            marker=dict(size=12, color="#d97706"),
            text=["Freedom"],
            textposition="top center"
        ))

    st.plotly_chart(style_plot(fig_income, height=400), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">Balance Sheet Forecast</div><div class="panel-subtitle">Assets grow while bad debt and investment debt reduce.</div>', unsafe_allow_html=True)

    fig_balance = go.Figure()
    fig_balance.add_trace(go.Scatter(x=annual["age"], y=annual["portfolio"], mode="lines", name="Portfolio", line=dict(color="#0f3b68", width=4)))
    fig_balance.add_trace(go.Scatter(x=annual["age"], y=annual["super"], mode="lines", name="Super", line=dict(color="#2563eb", width=3)))
    fig_balance.add_trace(go.Scatter(x=annual["age"], y=annual["bad_debt"], mode="lines", name="Bad debt", line=dict(color="#dc2626", width=3)))
    fig_balance.add_trace(go.Scatter(x=annual["age"], y=annual["investment_loan"], mode="lines", name="Investment loan", line=dict(color="#d97706", width=3, dash="dot")))

    st.plotly_chart(style_plot(fig_balance, height=400), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Detail panels
a, b, c = st.columns(3)

with a:
    st.markdown('<div class="panel"><div class="panel-title">Bad Debt Breakdown</div><div class="panel-subtitle">Debt that delays financial freedom.</div>', unsafe_allow_html=True)
    debt_now = pd.DataFrame({
        "Debt": ["Home Loan", "Car Loan", "Credit Card", "Personal Loan"],
        "Balance": [settings["home_loan_balance"], settings["car_loan_balance"], settings["credit_card_balance"], settings["personal_loan_balance"]],
    })
    st.metric("Total Bad Debt", money(total_bad_debt))
    st.metric("Monthly Servicing", money(total_bad_debt_repayment))
    debt_bar = px.bar(debt_now, x="Debt", y="Balance")
    debt_bar.update_traces(marker_color="#0f3b68")
    st.plotly_chart(style_plot(debt_bar, height=270), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="panel"><div class="panel-title">Retirement Bridge</div><div class="panel-subtitle">Funding the period before super access.</div>', unsafe_allow_html=True)
    st.metric("Bridge Required", money(bridge["bridge_required"]))
    st.metric("Bridge Income", money(bridge["bridge_income"]))
    st.metric("Bridge Gap", money(bridge["bridge_gap"]))

    bridge_df = forecast[
        (forecast["age"] >= settings["target_retirement_age"])
        & (forecast["age"] <= settings["super_access_age"])
        & (forecast["month"] % 12 == 0)
    ]
    bridge_fig = go.Figure()
    bridge_fig.add_trace(go.Bar(x=bridge_df["age"], y=bridge_df["target_income"], name="Required", marker_color="#cbd5e1"))
    bridge_fig.add_trace(go.Bar(x=bridge_df["age"], y=bridge_df["dividend_income"], name="Dividends", marker_color="#0f3b68"))
    bridge_fig.update_layout(barmode="group")
    st.plotly_chart(style_plot(bridge_fig, height=270), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c:
    st.markdown('<div class="panel"><div class="panel-title">Investment Leverage</div><div class="panel-subtitle">Good debt tracked separately from bad debt.</div>', unsafe_allow_html=True)
    st.metric("Investment Loan", money(settings["investment_loan_balance"]))
    st.metric("Annual Loan Repayment", money(settings["investment_loan_monthly_repayment"] * 12))
    leverage_fig = go.Figure()
    leverage_fig.add_trace(go.Scatter(x=annual["age"], y=annual["portfolio"], mode="lines", name="Portfolio", line=dict(color="#0f3b68", width=4)))
    leverage_fig.add_trace(go.Scatter(x=annual["age"], y=annual["investment_loan"], mode="lines", name="Investment loan", line=dict(color="#d97706", width=3)))
    st.plotly_chart(style_plot(leverage_fig, height=270), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Scenario Test
st.subheader("Scenario Test")
st.caption("Change the levers below to test how the Financial Freedom age moves. These do not change the saved inputs.")

s1, s2, s3, s4 = st.columns(4)
with s1:
    scenario_income = st.slider("Target income", 80000, 180000, int(settings["target_income"]), 5000)
with s2:
    scenario_monthly_investment = st.slider("Monthly investment", 0, 10000, int(settings["monthly_investment"]), 500)
with s3:
    scenario_extra_debt = st.slider("Extra bad debt repayment", 0, 10000, int(settings["extra_bad_debt_repayment"]), 500)
with s4:
    scenario_growth_pct = st.slider("Portfolio growth %", 0.0, 12.0, float(settings["portfolio_growth_rate_pct"]), 0.1)

scenario_settings = settings.copy()
scenario_settings["target_income"] = scenario_income
scenario_settings["monthly_investment"] = scenario_monthly_investment
scenario_settings["extra_bad_debt_repayment"] = scenario_extra_debt
scenario_settings["portfolio_growth_rate_pct"] = scenario_growth_pct

scenario_df = build_forecast(scenario_settings)
scenario_age = first_true_age(scenario_df, "financial_freedom")
scenario_years = None if scenario_age is None else scenario_age - settings["current_age"]

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Scenario Freedom Age", age_text(scenario_age))
with m2:
    st.metric("Scenario Years Remaining", years_text(scenario_years))
with m3:
    delta = "" if freedom_age is None or scenario_age is None else f"{scenario_age - freedom_age:+.1f} years"
    st.metric("Movement vs Base Case", delta if delta else "—")

st.divider()

# Monthly snapshot
st.subheader("Monthly Snapshot & History")
st.caption("Save current values once per month to build actual performance history and rolling growth.")

snap_left, snap_right = st.columns([1, 2])

with snap_left:
    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    snapshot_notes = st.text_area("Notes", height=80)

    if st.button("Save Current Month Snapshot", use_container_width=True):
        expected_columns = [
            "month", "portfolio_value", "super_balance_1", "super_balance_2", "combined_super",
            "home_loan_balance", "car_loan_balance", "credit_card_balance", "personal_loan_balance",
            "total_bad_debt", "investment_loan_balance", "cash_balance", "annual_dividend_income", "notes",
        ]

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
            "combined_super": combined_super,
            "home_loan_balance": settings["home_loan_balance"],
            "car_loan_balance": settings["car_loan_balance"],
            "credit_card_balance": settings["credit_card_balance"],
            "personal_loan_balance": settings["personal_loan_balance"],
            "total_bad_debt": total_bad_debt,
            "investment_loan_balance": settings["investment_loan_balance"],
            "cash_balance": settings.get("cash_balance", 0),
            "annual_dividend_income": current_dividends,
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
        for col, name, color in [
            ("portfolio_value", "Portfolio", "#0f3b68"),
            ("combined_super", "Combined super", "#2563eb"),
            ("total_bad_debt", "Bad debt", "#dc2626"),
            ("investment_loan_balance", "Investment loan", "#d97706"),
        ]:
            if col in snapshot_history.columns:
                hist_fig.add_trace(go.Scatter(x=snapshot_history["month"], y=snapshot_history[col], mode="lines+markers", name=name, line=dict(color=color, width=3)))
        st.plotly_chart(style_plot(hist_fig, height=330), use_container_width=True)

        with st.expander("View snapshot table"):
            st.dataframe(snapshot_history, use_container_width=True)
    else:
        st.info("No monthly snapshots saved yet.")
