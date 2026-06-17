
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Financial Freedom Dashboard V12.1", page_icon="💰", layout="wide")

DATA_DIR = Path("data")
SETTINGS_PATH = DATA_DIR / "settings.json"
SNAPSHOT_PATH = DATA_DIR / "monthly_snapshots.csv"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_SETTINGS = {
    "current_age": 50,
    "target_retirement_age": 55,
    "super_access_age": 60,
    "target_income": 120000,
    "inflation_rate": 0.03,
    "portfolio_growth_rate": 0.06,
    "dividend_yield": 0.05,
    "super_growth_rate": 0.06,
    "current_portfolio": 900000,
    "current_super": 650000,
    "bad_debt_balance": 300000,
    "bad_debt_interest_rate": 0.06,
    "bad_debt_monthly_repayment": 4000,
    "bad_debt_extra_repayment": 0,
    "investment_loan_balance": 100000,
    "investment_loan_interest_rate": 0.00,
    "investment_loan_monthly_repayment": 1000,
    "monthly_investment": 3000,
    "cash_balance": 25000,
}

def load_settings():
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)

def money(value):
    value = float(value)
    if abs(value) >= 1000000:
        return f"${value/1000000:.2f}M"
    return f"${value:,.0f}"

def future_value_monthly(start_value, monthly_contribution, annual_growth_rate, months):
    values = []
    balance = float(start_value)
    monthly_rate = annual_growth_rate / 12
    for month in range(months + 1):
        values.append(balance)
        balance = balance * (1 + monthly_rate) + monthly_contribution
    return values

def debt_paydown(balance, annual_interest_rate, monthly_repayment, extra_repayment, months=600):
    rows = []
    debt = float(balance)
    monthly_rate = annual_interest_rate / 12
    payment = monthly_repayment + extra_repayment
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

def build_forecast(settings, years=40):
    months = years * 12
    portfolio_values = future_value_monthly(settings["current_portfolio"], settings["monthly_investment"], settings["portfolio_growth_rate"], months)
    super_values = future_value_monthly(settings["current_super"], 0, settings["super_growth_rate"], months)

    bad_debt_df = debt_paydown(settings["bad_debt_balance"], settings["bad_debt_interest_rate"], settings["bad_debt_monthly_repayment"], settings["bad_debt_extra_repayment"], months)
    investment_loan_df = debt_paydown(settings["investment_loan_balance"], settings["investment_loan_interest_rate"], settings["investment_loan_monthly_repayment"], 0, months)

    bad_debt_lookup = dict(zip(bad_debt_df["month"], bad_debt_df["balance"]))
    inv_loan_lookup = dict(zip(investment_loan_df["month"], investment_loan_df["balance"]))

    rows = []
    current_age = settings["current_age"]

    for m in range(months + 1):
        age = current_age + m / 12
        portfolio = portfolio_values[m]
        super_balance = super_values[m]
        dividend_income = portfolio * settings["dividend_yield"]
        target_income = settings["target_income"] * ((1 + settings["inflation_rate"]) ** (m / 12))
        bad_debt = bad_debt_lookup.get(m, 0)
        investment_loan = inv_loan_lookup.get(m, 0)
        investment_loan_payment_annual = settings["investment_loan_monthly_repayment"] * 12 if investment_loan > 0 else 0
        financial_freedom = bad_debt <= 0 and dividend_income >= target_income + investment_loan_payment_annual

        rows.append({
            "month": m,
            "age": age,
            "portfolio": portfolio,
            "super": super_balance,
            "dividend_income": dividend_income,
            "target_income": target_income,
            "bad_debt": bad_debt,
            "investment_loan": investment_loan,
            "financial_freedom": financial_freedom,
        })

    return pd.DataFrame(rows)

def first_true_age(df, column):
    hits = df[df[column] == True]
    return None if hits.empty else float(hits.iloc[0]["age"])

def first_zero_debt_age(df):
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

def progress_gauge(value, title, subtitle):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=max(0, min(value, 100)),
        number={"suffix": "%"},
        title={"text": f"<b>{title}</b><br><span style='font-size:0.8em;color:gray'>{subtitle}</span>"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.28}}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=60, b=20))
    return fig

settings = load_settings()

st.sidebar.title("⚙️ Inputs")
st.sidebar.caption("Manual inputs only. The dashboard does the forecasting.")

with st.sidebar.expander("Core Assumptions", expanded=True):
    settings["current_age"] = st.number_input("Current Age", value=float(settings["current_age"]), step=0.5)
    settings["target_retirement_age"] = st.number_input("Target Retirement Age", value=float(settings["target_retirement_age"]), step=0.5)
    settings["target_income"] = st.number_input("Target Annual Income", value=int(settings["target_income"]), step=5000)
    settings["inflation_rate"] = st.number_input("Inflation", value=float(settings["inflation_rate"]), step=0.005, format="%.3f")

with st.sidebar.expander("Investments"):
    settings["current_portfolio"] = st.number_input("Portfolio Value", value=int(settings["current_portfolio"]), step=10000)
    settings["monthly_investment"] = st.number_input("Monthly Investment", value=int(settings["monthly_investment"]), step=500)
    settings["dividend_yield"] = st.number_input("Dividend Yield", value=float(settings["dividend_yield"]), step=0.005, format="%.3f")
    settings["portfolio_growth_rate"] = st.number_input("Capital Growth", value=float(settings["portfolio_growth_rate"]), step=0.005, format="%.3f")

with st.sidebar.expander("Super"):
    settings["current_super"] = st.number_input("Super Balance", value=int(settings["current_super"]), step=10000)
    settings["super_growth_rate"] = st.number_input("Super Growth", value=float(settings["super_growth_rate"]), step=0.005, format="%.3f")

with st.sidebar.expander("Bad Debt"):
    settings["bad_debt_balance"] = st.number_input("Bad Debt Balance", value=int(settings["bad_debt_balance"]), step=10000)
    settings["bad_debt_interest_rate"] = st.number_input("Bad Debt Interest", value=float(settings["bad_debt_interest_rate"]), step=0.005, format="%.3f")
    settings["bad_debt_monthly_repayment"] = st.number_input("Bad Debt Monthly Repayment", value=int(settings["bad_debt_monthly_repayment"]), step=500)
    settings["bad_debt_extra_repayment"] = st.number_input("Extra Bad Debt Repayment", value=int(settings["bad_debt_extra_repayment"]), step=500)

with st.sidebar.expander("Investment Loan"):
    settings["investment_loan_balance"] = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000)
    settings["investment_loan_interest_rate"] = st.number_input("Investment Loan Interest", value=float(settings["investment_loan_interest_rate"]), step=0.005, format="%.3f")
    settings["investment_loan_monthly_repayment"] = st.number_input("Investment Loan Monthly Repayment", value=int(settings["investment_loan_monthly_repayment"]), step=500)

with st.sidebar.expander("Cash"):
    settings["cash_balance"] = st.number_input("Cash Balance", value=int(settings.get("cash_balance", 0)), step=1000)

if st.sidebar.button("💾 Save Inputs", use_container_width=True):
    save_settings(settings)
    st.sidebar.success("Inputs saved")

forecast = build_forecast(settings)
annual = forecast[forecast["month"] % 12 == 0].copy()
freedom_age = first_true_age(forecast, "financial_freedom")
bad_debt_free_age = first_zero_debt_age(forecast)
bridge = bridge_summary(forecast, settings)

current_dividends = settings["current_portfolio"] * settings["dividend_yield"]
freedom_ratio = current_dividends / settings["target_income"] if settings["target_income"] else 0
years_remaining = None if freedom_age is None else max(freedom_age - settings["current_age"], 0)

st.title("Financial Freedom Dashboard V12.1")
st.caption("Single-page command centre: How many more years do we need to work?")

h1, h2, h3, h4, h5, h6 = st.columns(6)
with h1:
    st.metric("Freedom Age", "Not reached" if freedom_age is None else f"{freedom_age:.1f}", help="The first age where bad debt is cleared and dividend income covers target income plus investment loan repayments.")
with h2:
    st.metric("Years Remaining", "Not reached" if years_remaining is None else f"{years_remaining:.1f}", help="Estimated years until work becomes optional.")
with h3:
    st.metric("Freedom Ratio", f"{freedom_ratio:.0%}", help="Current annual dividend income divided by target annual income.")
with h4:
    st.metric("Bad Debt Free Age", "Not cleared" if bad_debt_free_age is None else f"{bad_debt_free_age:.1f}", help="Estimated age when bad debt reaches zero.")
with h5:
    st.metric("Bridge Gap", money(bridge["bridge_gap"]), help="Estimated gap between required income and dividend income from target retirement age to super access age.")
with h6:
    st.metric("Annual Dividends", money(current_dividends), help="Current portfolio value multiplied by dividend yield.")

st.divider()

left, centre, right = st.columns([1.1, 1.4, 1.4])

with left:
    st.subheader("Freedom Progress")
    st.plotly_chart(progress_gauge(freedom_ratio * 100, "Income Replacement", "Dividends vs target income"), use_container_width=True)
    st.markdown("#### Freedom Journey")
    journey = [
        ("Bad debt cleared", bad_debt_free_age is not None and bad_debt_free_age <= settings["target_retirement_age"]),
        ("Bridge ready", bridge["bridge_gap"] <= 0),
        ("Dividend target met", freedom_ratio >= 1),
        ("Financial freedom", freedom_age is not None),
    ]
    for label, done in journey:
        st.write(f"{'✅' if done else '⏳'} {label}")

with centre:
    st.subheader("Income Forecast")
    fig_income = px.line(annual, x="age", y=["dividend_income", "target_income"], labels={"value": "Annual Income", "age": "Age", "variable": "Category"})
    fig_income.update_layout(height=360, legend_title_text="")
    st.plotly_chart(fig_income, use_container_width=True)

with right:
    st.subheader("Balance Sheet Forecast")
    fig_balance = px.line(annual, x="age", y=["portfolio", "super", "bad_debt", "investment_loan"], labels={"value": "Balance", "age": "Age", "variable": "Category"})
    fig_balance.update_layout(height=360, legend_title_text="")
    st.plotly_chart(fig_balance, use_container_width=True)

st.divider()

a, b, c = st.columns(3)

with a:
    st.subheader("Bad Debt Paydown")
    st.metric("Current Bad Debt", money(settings["bad_debt_balance"]))
    st.metric("Monthly Repayment", money(settings["bad_debt_monthly_repayment"] + settings["bad_debt_extra_repayment"]))
    debt_fig = px.area(annual, x="age", y="bad_debt", labels={"bad_debt": "Bad Debt", "age": "Age"})
    debt_fig.update_layout(height=300)
    st.plotly_chart(debt_fig, use_container_width=True)

with b:
    st.subheader("Retirement Bridge")
    st.metric("Bridge Required", money(bridge["bridge_required"]))
    st.metric("Bridge Income", money(bridge["bridge_income"]))
    st.metric("Bridge Gap", money(bridge["bridge_gap"]))
    bridge_df = forecast[(forecast["age"] >= settings["target_retirement_age"]) & (forecast["age"] <= settings["super_access_age"]) & (forecast["month"] % 12 == 0)]
    bridge_fig = px.bar(bridge_df, x="age", y=["target_income", "dividend_income"], barmode="group", labels={"value": "Annual Amount", "age": "Age", "variable": "Category"})
    bridge_fig.update_layout(height=300, legend_title_text="")
    st.plotly_chart(bridge_fig, use_container_width=True)

with c:
    st.subheader("Investment Leverage")
    st.metric("Investment Loan", money(settings["investment_loan_balance"]))
    st.metric("Annual Loan Repayment", money(settings["investment_loan_monthly_repayment"] * 12))
    leverage_fig = px.line(annual, x="age", y=["portfolio", "investment_loan"], labels={"value": "Amount", "age": "Age", "variable": "Category"})
    leverage_fig.update_layout(height=300, legend_title_text="")
    st.plotly_chart(leverage_fig, use_container_width=True)

st.divider()

st.subheader("Scenario Test")
s1, s2, s3, s4 = st.columns(4)
with s1:
    scenario_income = st.slider("Target income", 80000, 180000, int(settings["target_income"]), 5000)
with s2:
    scenario_monthly_investment = st.slider("Monthly investment", 0, 10000, int(settings["monthly_investment"]), 500)
with s3:
    scenario_extra_debt = st.slider("Extra debt repayment", 0, 10000, int(settings["bad_debt_extra_repayment"]), 500)
with s4:
    scenario_growth = st.slider("Portfolio growth", 0.00, 0.12, float(settings["portfolio_growth_rate"]), 0.005)

scenario_settings = settings.copy()
scenario_settings["target_income"] = scenario_income
scenario_settings["monthly_investment"] = scenario_monthly_investment
scenario_settings["bad_debt_extra_repayment"] = scenario_extra_debt
scenario_settings["portfolio_growth_rate"] = scenario_growth

scenario_df = build_forecast(scenario_settings)
scenario_age = first_true_age(scenario_df, "financial_freedom")
st.metric("Scenario Result", "Not reached" if scenario_age is None else f"Freedom age {scenario_age:.1f}", help="This updates based on the scenario sliders without changing saved inputs.")

st.divider()

st.subheader("Monthly Snapshot & History")
st.caption("Save the current sidebar values once per month to build actual history.")

snap_left, snap_right = st.columns([1, 2])

with snap_left:
    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    snapshot_notes = st.text_area("Notes", height=80)
    if st.button("Save Current Month Snapshot", use_container_width=True):
        if SNAPSHOT_PATH.exists():
            history = pd.read_csv(SNAPSHOT_PATH)
        else:
            history = pd.DataFrame(columns=["month", "portfolio_value", "super_balance", "bad_debt_balance", "investment_loan_balance", "cash_balance", "annual_dividend_income", "notes"])
        new_row = {
            "month": month,
            "portfolio_value": settings["current_portfolio"],
            "super_balance": settings["current_super"],
            "bad_debt_balance": settings["bad_debt_balance"],
            "investment_loan_balance": settings["investment_loan_balance"],
            "cash_balance": settings.get("cash_balance", 0),
            "annual_dividend_income": current_dividends,
            "notes": snapshot_notes,
        }
        if not history.empty and "month" in history.columns:
            history = history[history["month"] != month]
        history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)
        history.to_csv(SNAPSHOT_PATH, index=False)
        st.success("Snapshot saved")

with snap_right:
    if SNAPSHOT_PATH.exists():
        history = pd.read_csv(SNAPSHOT_PATH)
    else:
        history = pd.DataFrame()
    if not history.empty:
        history = history.sort_values("month")
        hist_fig = px.line(history, x="month", y=["portfolio_value", "super_balance", "bad_debt_balance", "investment_loan_balance"], labels={"value": "Balance", "month": "Month", "variable": "Category"})
        hist_fig.update_layout(height=320, legend_title_text="")
        st.plotly_chart(hist_fig, use_container_width=True)
        with st.expander("View snapshot table"):
            st.dataframe(history, use_container_width=True)
    else:
        st.info("No monthly snapshots saved yet.")
