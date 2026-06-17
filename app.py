
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from datetime import date
import math

st.set_page_config(page_title="Financial Freedom Dashboard V12.2", page_icon="💰", layout="wide")

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

def load_settings():
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r") as f:
        data = json.load(f)

    # Add any missing keys from defaults to avoid errors after upgrades.
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
            # Debt will not reduce with these settings.
            break

    return pd.DataFrame(rows)

def calculate_total_bad_debt(settings):
    return (
        settings["home_loan_balance"]
        + settings["car_loan_balance"]
        + settings["credit_card_balance"]
        + settings["personal_loan_balance"]
    )

def calculate_total_bad_debt_repayment(settings):
    return (
        settings["home_loan_monthly_repayment"]
        + settings["car_loan_monthly_repayment"]
        + settings["credit_card_monthly_repayment"]
        + settings["personal_loan_monthly_repayment"]
        + settings["extra_bad_debt_repayment"]
    )

def build_forecast(settings, years=40):
    months = years * 12

    portfolio_growth = pct_to_rate(settings["portfolio_growth_rate_pct"])
    super_growth = pct_to_rate(settings["super_growth_rate_pct"])
    dividend_yield = pct_to_rate(settings["dividend_yield_pct"])
    inflation_rate = pct_to_rate(settings["inflation_rate_pct"])

    combined_super = settings["super_balance_1"] + settings["super_balance_2"]

    portfolio_values = future_value_monthly(
        settings["current_portfolio"],
        settings["monthly_investment"],
        portfolio_growth,
        months,
    )

    super_values = future_value_monthly(
        combined_super,
        0,
        super_growth,
        months,
    )

    home_df = debt_paydown(
        settings["home_loan_balance"],
        pct_to_rate(settings["home_loan_interest_pct"]),
        settings["home_loan_monthly_repayment"],
        settings["extra_bad_debt_repayment"],
        months,
    )

    car_df = debt_paydown(
        settings["car_loan_balance"],
        pct_to_rate(settings["car_loan_interest_pct"]),
        settings["car_loan_monthly_repayment"],
        0,
        months,
    )

    credit_df = debt_paydown(
        settings["credit_card_balance"],
        pct_to_rate(settings["credit_card_interest_pct"]),
        settings["credit_card_monthly_repayment"],
        0,
        months,
    )

    personal_df = debt_paydown(
        settings["personal_loan_balance"],
        pct_to_rate(settings["personal_loan_interest_pct"]),
        settings["personal_loan_monthly_repayment"],
        0,
        months,
    )

    inv_loan_df = debt_paydown(
        settings["investment_loan_balance"],
        pct_to_rate(settings["investment_loan_interest_pct"]),
        settings["investment_loan_monthly_repayment"],
        0,
        months,
    )

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
    bridge = df[
        (df["age"] >= settings["target_retirement_age"])
        & (df["age"] < settings["super_access_age"])
    ].copy()

    if bridge.empty:
        return {"bridge_required": 0, "bridge_income": 0, "bridge_gap": 0}

    annual_rows = bridge[bridge["month"] % 12 == 0]
    bridge_required = annual_rows["target_income"].sum()
    bridge_income = annual_rows["dividend_income"].sum()

    return {
        "bridge_required": bridge_required,
        "bridge_income": bridge_income,
        "bridge_gap": bridge_required - bridge_income,
    }

def progress_gauge(value, title, subtitle):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=max(0, min(value, 100)),
        number={"suffix": "%"},
        title={"text": f"<b>{title}</b><br><span style='font-size:0.8em;color:gray'>{subtitle}</span>"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"thickness": 0.28},
            "steps": [
                {"range": [0, 50], "color": "#f1f5f9"},
                {"range": [50, 80], "color": "#e2e8f0"},
                {"range": [80, 100], "color": "#cbd5e1"},
            ],
        },
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def load_history():
    if SNAPSHOT_PATH.exists():
        return pd.read_csv(SNAPSHOT_PATH)
    return pd.DataFrame()

def calculate_history_growth(history):
    if history.empty or len(history) < 2:
        return {
            "portfolio_monthly": None,
            "portfolio_3m": None,
            "portfolio_12m": None,
            "super_monthly": None,
            "super_3m": None,
            "super_12m": None,
        }

    history = history.sort_values("month").reset_index(drop=True)

    def growth(column, periods):
        if len(history) <= periods:
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
        return "Not enough data"
    return f"{value:.1f}%"

settings = load_settings()

st.sidebar.title("⚙️ Inputs")
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
    combined_super_input = settings["super_balance_1"] + settings["super_balance_2"]
    st.info(f"Combined Super: {money(combined_super_input)}")
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

if st.sidebar.button("💾 Save Inputs", use_container_width=True):
    save_settings(settings)
    st.sidebar.success("Inputs saved")

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

history = load_history()
growth = calculate_history_growth(history)

st.title("Financial Freedom Dashboard V12.2")
st.caption("Single-page command centre: How many more years do we need to work?")

h1, h2, h3, h4, h5, h6 = st.columns(6)
with h1:
    st.metric("Freedom Age", "Not reached" if freedom_age is None else f"{freedom_age:.1f}", help="The first age where bad debt is cleared and dividend income covers target income plus investment loan repayments.")
with h2:
    st.metric("Years Remaining", "Not reached" if years_remaining is None else f"{years_remaining:.1f}", help="Estimated years until work becomes optional.")
with h3:
    st.metric("Freedom Ratio", f"{freedom_ratio:.0%}", help="Current annual dividend income divided by target annual income.")
with h4:
    st.metric("Bad Debt Free Age", "Not cleared" if bad_debt_free_age is None else f"{bad_debt_free_age:.1f}", help="Estimated age when all bad debt reaches zero.")
with h5:
    st.metric("Bridge Gap", money(bridge["bridge_gap"]), help="Estimated gap between required income and dividend income from target retirement age to super access age.")
with h6:
    st.metric("Annual Dividends", money(current_dividends), help="Current portfolio value multiplied by dividend yield.")

st.divider()

# Current position row
p1, p2, p3, p4 = st.columns(4)
with p1:
    st.metric("Portfolio Value", money(settings["current_portfolio"]), help="Current non-super investment portfolio.")
with p2:
    st.metric("Combined Super", money(combined_super), help="Super Balance 1 plus Super Balance 2.")
with p3:
    st.metric("Total Bad Debt", money(total_bad_debt), help="Home loan + car loan + credit card + personal loan.")
with p4:
    st.metric("Investment Loan", money(settings["investment_loan_balance"]), help="Investment loan is tracked separately from bad debt.")

st.divider()

left, centre, right = st.columns([1.1, 1.4, 1.4])

with left:
    st.subheader("Freedom Progress")
    st.plotly_chart(progress_gauge(freedom_ratio * 100, "Income Replacement", "Dividends vs target income"), use_container_width=True)

    st.markdown("#### Rolling Actual Growth")
    st.write(f"Portfolio monthly: **{format_growth(growth['portfolio_monthly'])}**")
    st.write(f"Portfolio 3-month: **{format_growth(growth['portfolio_3m'])}**")
    st.write(f"Portfolio 12-month: **{format_growth(growth['portfolio_12m'])}**")
    st.write(f"Super monthly: **{format_growth(growth['super_monthly'])}**")
    st.write(f"Super 3-month: **{format_growth(growth['super_3m'])}**")
    st.write(f"Super 12-month: **{format_growth(growth['super_12m'])}**")

with centre:
    st.subheader("Income Forecast")
    fig_income = px.line(
        annual,
        x="age",
        y=["dividend_income", "target_income"],
        labels={"value": "Annual Income", "age": "Age", "variable": "Category"},
    )
    fig_income.update_layout(height=380, legend_title_text="")
    st.plotly_chart(fig_income, use_container_width=True)

with right:
    st.subheader("Balance Sheet Forecast")
    fig_balance = px.line(
        annual,
        x="age",
        y=["portfolio", "super", "bad_debt", "investment_loan"],
        labels={"value": "Balance", "age": "Age", "variable": "Category"},
    )
    fig_balance.update_layout(height=380, legend_title_text="")
    st.plotly_chart(fig_balance, use_container_width=True)

st.divider()

a, b, c = st.columns(3)

with a:
    st.subheader("Bad Debt Breakdown")
    debt_now = pd.DataFrame({
        "Debt": ["Home Loan", "Car Loan", "Credit Card", "Personal Loan"],
        "Balance": [
            settings["home_loan_balance"],
            settings["car_loan_balance"],
            settings["credit_card_balance"],
            settings["personal_loan_balance"],
        ],
    })
    st.metric("Total Bad Debt", money(total_bad_debt))
    st.metric("Monthly Bad Debt Repayment", money(total_bad_debt_repayment))
    debt_bar = px.bar(debt_now, x="Debt", y="Balance", title=None)
    debt_bar.update_layout(height=300)
    st.plotly_chart(debt_bar, use_container_width=True)

with b:
    st.subheader("Retirement Bridge")
    st.metric("Bridge Required", money(bridge["bridge_required"]))
    st.metric("Bridge Income", money(bridge["bridge_income"]))
    st.metric("Bridge Gap", money(bridge["bridge_gap"]))

    bridge_df = forecast[
        (forecast["age"] >= settings["target_retirement_age"])
        & (forecast["age"] <= settings["super_access_age"])
        & (forecast["month"] % 12 == 0)
    ]
    bridge_fig = px.bar(
        bridge_df,
        x="age",
        y=["target_income", "dividend_income"],
        barmode="group",
        labels={"value": "Annual Amount", "age": "Age", "variable": "Category"},
    )
    bridge_fig.update_layout(height=300, legend_title_text="")
    st.plotly_chart(bridge_fig, use_container_width=True)

with c:
    st.subheader("Investment Leverage")
    st.metric("Investment Loan", money(settings["investment_loan_balance"]))
    st.metric("Annual Loan Repayment", money(settings["investment_loan_monthly_repayment"] * 12))
    leverage_fig = px.line(
        annual,
        x="age",
        y=["portfolio", "investment_loan"],
        labels={"value": "Amount", "age": "Age", "variable": "Category"},
    )
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

st.metric(
    "Scenario Result",
    "Not reached" if scenario_age is None else f"Freedom age {scenario_age:.1f}",
    help="This updates based on the scenario sliders without changing saved inputs."
)

st.divider()

st.subheader("Monthly Snapshot & History")
st.caption("Save the current sidebar values once per month to build actual history and calculate rolling growth.")

snap_left, snap_right = st.columns([1, 2])

with snap_left:
    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    snapshot_notes = st.text_area("Notes", height=80)

    if st.button("Save Current Month Snapshot", use_container_width=True):
        expected_columns = [
            "month",
            "portfolio_value",
            "super_balance_1",
            "super_balance_2",
            "combined_super",
            "home_loan_balance",
            "car_loan_balance",
            "credit_card_balance",
            "personal_loan_balance",
            "total_bad_debt",
            "investment_loan_balance",
            "cash_balance",
            "annual_dividend_income",
            "notes",
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

        hist_fig = px.line(
            snapshot_history,
            x="month",
            y=["portfolio_value", "combined_super", "total_bad_debt", "investment_loan_balance"],
            labels={"value": "Balance", "month": "Month", "variable": "Category"},
        )
        hist_fig.update_layout(height=320, legend_title_text="")
        st.plotly_chart(hist_fig, use_container_width=True)

        with st.expander("View snapshot table"):
            st.dataframe(snapshot_history, use_container_width=True)
    else:
        st.info("No monthly snapshots saved yet.")
