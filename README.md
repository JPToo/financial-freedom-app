
import numpy as np
import pandas as pd

def money(value):
    return f"${value:,.0f}"

def money2(value):
    return f"${value:,.2f}"

def calculate_mortgage_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        return principal / months
    return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

def future_value_lump_sum(present_value, annual_return, years):
    return present_value * ((1 + annual_return / 100) ** years)

def future_value_monthly_contribution(monthly_contribution, annual_return, years):
    monthly_rate = annual_return / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        return monthly_contribution * months
    return monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)

def prepare_wealth_data(df):
    df = df.copy()
    for col in ["Units", "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Average Buy Price"]
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Current Yield %"] = np.where(df["Market Value"] > 0, df["Annual Income"] / df["Market Value"] * 100, 0)
    df["Yield on Cost %"] = np.where(df["Cost Base"] > 0, df["Annual Income"] / df["Cost Base"] * 100, 0)
    df["Franking Credits"] = df["Annual Income"] * (df["Franking %"] / 100) * (30 / 70)
    total = df["Market Value"].sum()
    df["Allocation %"] = np.where(total > 0, df["Market Value"] / total * 100, 0)
    return df
