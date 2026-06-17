
import pandas as pd
import numpy as np
from datetime import datetime


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

    portfolio_values = future_value_monthly(
        settings["current_portfolio"],
        settings["monthly_investment"],
        settings["portfolio_growth_rate"],
        months,
    )

    super_values = future_value_monthly(
        settings["current_super"],
        0,
        settings["super_growth_rate"],
        months,
    )

    bad_debt_df = debt_paydown(
        settings["bad_debt_balance"],
        settings["bad_debt_interest_rate"],
        settings["bad_debt_monthly_repayment"],
        settings["bad_debt_extra_repayment"],
        months,
    )

    investment_loan_df = debt_paydown(
        settings["investment_loan_balance"],
        settings["investment_loan_interest_rate"],
        settings["investment_loan_monthly_repayment"],
        0,
        months,
    )

    rows = []
    current_age = settings["current_age"]

    for m in range(months + 1):
        age = current_age + m / 12
        portfolio = portfolio_values[m]
        super_balance = super_values[m]
        dividend_income = portfolio * settings["dividend_yield"]

        bad_debt = (
            bad_debt_df.loc[bad_debt_df["month"] == m, "balance"].iloc[0]
            if m in set(bad_debt_df["month"])
            else 0
        )

        investment_loan = (
            investment_loan_df.loc[investment_loan_df["month"] == m, "balance"].iloc[0]
            if m in set(investment_loan_df["month"])
            else 0
        )

        target_income = settings["target_income"] * ((1 + settings["inflation_rate"]) ** (m / 12))

        investment_loan_payment_annual = (
            settings["investment_loan_monthly_repayment"] * 12
            if investment_loan > 0
            else 0
        )

        bad_debt_cleared = bad_debt <= 0
        freedom_cashflow = dividend_income - target_income - investment_loan_payment_annual

        financial_freedom = (
            bad_debt_cleared
            and dividend_income >= target_income + investment_loan_payment_annual
        )

        rows.append({
            "month": m,
            "age": age,
            "portfolio": portfolio,
            "super": super_balance,
            "dividend_income": dividend_income,
            "target_income": target_income,
            "bad_debt": bad_debt,
            "investment_loan": investment_loan,
            "freedom_cashflow": freedom_cashflow,
            "financial_freedom": financial_freedom,
        })

    return pd.DataFrame(rows)


def first_true_age(df, column):
    hits = df[df[column] == True]
    if hits.empty:
        return None
    return hits.iloc[0]["age"]


def first_zero_debt_age(df):
    hits = df[df["bad_debt"] <= 0]
    if hits.empty:
        return None
    return hits.iloc[0]["age"]


def bridge_summary(df, settings):
    start_age = settings["target_retirement_age"]
    end_age = settings["super_access_age"]

    bridge = df[(df["age"] >= start_age) & (df["age"] < end_age)].copy()

    if bridge.empty:
        return {
            "bridge_required": 0,
            "bridge_income": 0,
            "bridge_gap": 0,
        }

    annual_rows = bridge[bridge["month"] % 12 == 0]
    bridge_required = annual_rows["target_income"].sum()
    bridge_income = annual_rows["dividend_income"].sum()
    bridge_gap = bridge_required - bridge_income

    return {
        "bridge_required": bridge_required,
        "bridge_income": bridge_income,
        "bridge_gap": bridge_gap,
    }
