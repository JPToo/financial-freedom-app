
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from datetime import date

from calculations import build_forecast, first_true_age, first_zero_debt_age, bridge_summary

st.set_page_config(
    page_title="Financial Freedom Dashboard V12",
    page_icon="💰",
    layout="wide"
)

DATA_DIR = Path(".")
SETTINGS_PATH = DATA_DIR / "settings.json"
SNAPSHOT_PATH = DATA_DIR / "monthly_snapshots.csv"

def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)

def money(value):
    return f"${value:,.0f}"

def pct(value):
    return f"{value * 100:.1f}%"

def metric_with_help(label, value, help_text):
    st.metric(label, value, help=help_text)

settings = load_settings()

st.sidebar.title("Financial Freedom V12")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Freedom Summary",
        "📅 Freedom Date",
        "🌉 Retirement Bridge",
        "📈 Investment Portfolio",
        "🏦 Superannuation",
        "💰 Dividend Income",
        "🏠 Bad Debt",
        "🚀 Investment Leverage",
        "🎯 Scenario Planner",
        "📒 Monthly Snapshot",
        "⚙️ Assumptions",
    ]
)

forecast = build_forecast(settings)
freedom_age = first_true_age(forecast, "financial_freedom")
bad_debt_free_age = first_zero_debt_age(forecast)
bridge = bridge_summary(forecast, settings)

if page == "🏠 Freedom Summary":
    st.title("Financial Freedom Dashboard V12")
    st.caption("Answering the question: How many more years do we need to work?")

    years_remaining = None if freedom_age is None else max(freedom_age - settings["current_age"], 0)
    freedom_ratio = (settings["current_portfolio"] * settings["dividend_yield"]) / settings["target_income"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_with_help(
            "Financial Freedom Age",
            "Not reached" if freedom_age is None else f"{freedom_age:.1f}",
            "The first age where bad debt is cleared and dividend income can cover target income plus investment loan repayments."
        )
    with c2:
        metric_with_help(
            "Years Remaining",
            "Not reached" if years_remaining is None else f"{years_remaining:.1f}",
            "Estimated number of years until work becomes optional based on the current assumptions."
        )
    with c3:
        metric_with_help(
            "Freedom Ratio",
            f"{freedom_ratio:.0%}",
            "Current dividend income divided by target annual income. 100% means dividends cover the income target before debt checks."
        )
    with c4:
        metric_with_help(
            "Bad Debt Free Age",
            "Not cleared" if bad_debt_free_age is None else f"{bad_debt_free_age:.1f}",
            "The estimated age when bad debt such as the home loan reaches zero."
        )

    st.divider()

    chart_df = forecast[forecast["month"] % 12 == 0].copy()
    fig = px.line(
        chart_df,
        x="age",
        y=["portfolio", "super", "bad_debt", "investment_loan"],
        labels={"value": "Balance", "age": "Age", "variable": "Category"},
        title="Financial Freedom Forecast"
    )
    st.plotly_chart(fig, use_container_width=True)

    income_fig = px.line(
        chart_df,
        x="age",
        y=["dividend_income", "target_income"],
        labels={"value": "Annual Income", "age": "Age", "variable": "Category"},
        title="Dividend Income vs Target Income"
    )
    st.plotly_chart(income_fig, use_container_width=True)

elif page == "📅 Freedom Date":
    st.title("Freedom Date")
    st.write("Change the target income and assumptions to see what happens to the Financial Freedom Age.")

    c1, c2, c3 = st.columns(3)
    with c1:
        settings["current_age"] = st.number_input("Current Age", value=float(settings["current_age"]), step=0.5)
    with c2:
        settings["target_retirement_age"] = st.number_input("Target Retirement Age", value=float(settings["target_retirement_age"]), step=0.5)
    with c3:
        settings["target_income"] = st.number_input("Target Annual Income", value=int(settings["target_income"]), step=5000)

    c4, c5, c6 = st.columns(3)
    with c4:
        settings["dividend_yield"] = st.number_input("Dividend Yield", value=float(settings["dividend_yield"]), step=0.005, format="%.3f")
    with c5:
        settings["portfolio_growth_rate"] = st.number_input("Portfolio Growth Rate", value=float(settings["portfolio_growth_rate"]), step=0.005, format="%.3f")
    with c6:
        settings["inflation_rate"] = st.number_input("Inflation Rate", value=float(settings["inflation_rate"]), step=0.005, format="%.3f")

    if st.button("Save Freedom Date Assumptions"):
        save_settings(settings)
        st.success("Assumptions saved. Refresh or change page to recalculate.")

    st.subheader("Current Result")
    forecast = build_forecast(settings)
    freedom_age = first_true_age(forecast, "financial_freedom")
    st.metric("Financial Freedom Age", "Not reached" if freedom_age is None else f"{freedom_age:.1f}")

elif page == "🌉 Retirement Bridge":
    st.title("Retirement Bridge: 55 to 60")
    st.write("This checks whether the investment portfolio can support the years before super becomes available.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Bridge Required", money(bridge["bridge_required"]))
    with c2:
        st.metric("Dividend Income During Bridge", money(bridge["bridge_income"]))
    with c3:
        st.metric("Bridge Gap", money(bridge["bridge_gap"]))

    bridge_df = forecast[
        (forecast["age"] >= settings["target_retirement_age"])
        & (forecast["age"] <= settings["super_access_age"])
        & (forecast["month"] % 12 == 0)
    ]

    fig = px.bar(
        bridge_df,
        x="age",
        y=["target_income", "dividend_income"],
        barmode="group",
        title="Bridge Income Requirement vs Dividend Income",
        labels={"value": "Annual Amount", "age": "Age", "variable": "Category"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Investment Portfolio":
    st.title("Investment Portfolio")
    st.write("This is not a portfolio tracker. It models portfolio growth, compounding and dividend income.")

    c1, c2, c3 = st.columns(3)
    with c1:
        settings["current_portfolio"] = st.number_input("Current Portfolio Value", value=int(settings["current_portfolio"]), step=10000)
    with c2:
        settings["monthly_investment"] = st.number_input("Monthly Investment", value=int(settings["monthly_investment"]), step=500)
    with c3:
        settings["dividend_yield"] = st.number_input("Dividend Yield", value=float(settings["dividend_yield"]), step=0.005, format="%.3f")

    if st.button("Save Portfolio Inputs"):
        save_settings(settings)
        st.success("Portfolio inputs saved.")

    chart_df = forecast[forecast["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y="portfolio", title="Portfolio Growth Forecast")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏦 Superannuation":
    st.title("Superannuation")
    st.write("Simple monthly / annual balance forecast. Employer contribution and salary sacrifice are intentionally excluded.")

    c1, c2 = st.columns(2)
    with c1:
        settings["current_super"] = st.number_input("Current Super Balance", value=int(settings["current_super"]), step=10000)
    with c2:
        settings["super_growth_rate"] = st.number_input("Super Growth Rate", value=float(settings["super_growth_rate"]), step=0.005, format="%.3f")

    if st.button("Save Super Inputs"):
        save_settings(settings)
        st.success("Super inputs saved.")

    chart_df = forecast[forecast["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y="super", title="Superannuation Forecast")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Dividend Income":
    st.title("Dividend Income")
    st.write("Tracks income replacement and how dividends grow as the portfolio compounds.")

    current_dividends = settings["current_portfolio"] * settings["dividend_yield"]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Current Annual Dividends", money(current_dividends))
    with c2:
        st.metric("Target Annual Income", money(settings["target_income"]))
    with c3:
        st.metric("Dividend Coverage", f"{current_dividends / settings['target_income']:.0%}")

    chart_df = forecast[forecast["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y=["dividend_income", "target_income"], title="Dividend Income Forecast")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏠 Bad Debt":
    st.title("Bad Debt")
    st.write("Bad debt is tracked separately from investment debt. The goal is to clear this first.")

    c1, c2 = st.columns(2)
    with c1:
        settings["bad_debt_balance"] = st.number_input("Bad Debt Balance", value=int(settings["bad_debt_balance"]), step=10000)
        settings["bad_debt_interest_rate"] = st.number_input("Bad Debt Interest Rate", value=float(settings["bad_debt_interest_rate"]), step=0.005, format="%.3f")
    with c2:
        settings["bad_debt_monthly_repayment"] = st.number_input("Monthly Repayment", value=int(settings["bad_debt_monthly_repayment"]), step=500)
        settings["bad_debt_extra_repayment"] = st.number_input("Extra Monthly Repayment", value=int(settings["bad_debt_extra_repayment"]), step=500)

    if st.button("Save Bad Debt Inputs"):
        save_settings(settings)
        st.success("Bad debt inputs saved.")

    chart_df = forecast[forecast["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y="bad_debt", title="Bad Debt Paydown Forecast")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🚀 Investment Leverage":
    st.title("Investment Leverage")
    st.write("Good debt is modelled separately. No tax modelling in Version 12.")

    c1, c2, c3 = st.columns(3)
    with c1:
        settings["investment_loan_balance"] = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000)
    with c2:
        settings["investment_loan_interest_rate"] = st.number_input("Investment Loan Interest Rate", value=float(settings["investment_loan_interest_rate"]), step=0.005, format="%.3f")
    with c3:
        settings["investment_loan_monthly_repayment"] = st.number_input("Investment Loan Monthly Repayment", value=int(settings["investment_loan_monthly_repayment"]), step=500)

    if st.button("Save Investment Loan Inputs"):
        save_settings(settings)
        st.success("Investment leverage inputs saved.")

    chart_df = forecast[forecast["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y=["portfolio", "investment_loan"], title="Investment Assets vs Investment Loan")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Scenario Planner":
    st.title("Scenario Planner")
    st.write("Test how income target, extra investment, and extra debt repayment change your Financial Freedom Age.")

    scenario_income = st.slider("Target Income", 80000, 180000, int(settings["target_income"]), 5000)
    scenario_monthly_investment = st.slider("Monthly Investment", 0, 10000, int(settings["monthly_investment"]), 500)
    scenario_extra_debt = st.slider("Extra Bad Debt Repayment", 0, 10000, int(settings["bad_debt_extra_repayment"]), 500)

    scenario_settings = settings.copy()
    scenario_settings["target_income"] = scenario_income
    scenario_settings["monthly_investment"] = scenario_monthly_investment
    scenario_settings["bad_debt_extra_repayment"] = scenario_extra_debt

    scenario_df = build_forecast(scenario_settings)
    scenario_age = first_true_age(scenario_df, "financial_freedom")

    st.metric("Scenario Financial Freedom Age", "Not reached" if scenario_age is None else f"{scenario_age:.1f}")

    chart_df = scenario_df[scenario_df["month"] % 12 == 0]
    fig = px.line(chart_df, x="age", y=["portfolio", "bad_debt", "dividend_income", "target_income"], title="Scenario Forecast")
    st.plotly_chart(fig, use_container_width=True)

elif page == "📒 Monthly Snapshot":
    st.title("Monthly Snapshot")
    st.write("Save a monthly record of your actual balances. The dashboard uses this to build actual performance history.")

    month = st.date_input("Snapshot Month", value=date.today()).strftime("%Y-%m")
    portfolio_value = st.number_input("Portfolio Value", value=int(settings["current_portfolio"]), step=10000)
    super_balance = st.number_input("Super Balance", value=int(settings["current_super"]), step=10000)
    bad_debt_balance = st.number_input("Bad Debt Balance", value=int(settings["bad_debt_balance"]), step=10000)
    investment_loan_balance = st.number_input("Investment Loan Balance", value=int(settings["investment_loan_balance"]), step=10000)
    cash_balance = st.number_input("Cash Balance", value=0, step=1000)
    annual_dividend_income = st.number_input("Annual Dividend Income", value=int(settings["current_portfolio"] * settings["dividend_yield"]), step=1000)
    notes = st.text_area("Notes")

    if st.button("Save Monthly Snapshot"):
        if SNAPSHOT_PATH.exists():
            df = pd.read_csv(SNAPSHOT_PATH)
        else:
            df = pd.DataFrame()

        new_row = {
            "month": month,
            "portfolio_value": portfolio_value,
            "super_balance": super_balance,
            "bad_debt_balance": bad_debt_balance,
            "investment_loan_balance": investment_loan_balance,
            "cash_balance": cash_balance,
            "annual_dividend_income": annual_dividend_income,
            "notes": notes,
        }

        df = df[df["month"] != month] if "month" in df.columns else df
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(SNAPSHOT_PATH, index=False)
        st.success("Monthly snapshot saved.")

    if SNAPSHOT_PATH.exists():
        history = pd.read_csv(SNAPSHOT_PATH)
        if not history.empty:
            st.subheader("Historical Snapshots")
            st.dataframe(history, use_container_width=True)
            fig = px.line(history, x="month", y=["portfolio_value", "super_balance", "bad_debt_balance", "investment_loan_balance"], title="Actual History")
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Assumptions":
    st.title("Assumptions")
    st.write("Core model assumptions used across the dashboard.")

    editable = {}
    for key, value in settings.items():
        if isinstance(value, int):
            editable[key] = st.number_input(key, value=value, step=1000 if "balance" in key or "portfolio" in key or "income" in key else 1)
        elif isinstance(value, float):
            editable[key] = st.number_input(key, value=float(value), step=0.005, format="%.3f")
        else:
            editable[key] = st.text_input(key, value=str(value))

    if st.button("Save All Assumptions"):
        save_settings(editable)
        st.success("All assumptions saved.")
