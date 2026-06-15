
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Dividend Freedom Dashboard",
    page_icon="📈",
    layout="wide"
)

TARGET_INCOME_DEFAULT = 120000

@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        "Ticker": ["CBA.AX", "BHP.AX", "WDS.AX", "WES.AX", "VAS.AX", "VGS.AX", "VHY.AX"],
        "Name": [
            "Commonwealth Bank",
            "BHP Group",
            "Woodside Energy",
            "Wesfarmers",
            "Vanguard Australian Shares ETF",
            "Vanguard International Shares ETF",
            "Vanguard Australian High Yield ETF"
        ],
        "Asset Type": ["Share", "Share", "Share", "Share", "ETF", "ETF", "ETF"],
        "Sector": ["Financials", "Resources", "Energy", "Industrials", "ETF - Australia", "ETF - International", "ETF - Dividend"],
        "Units": [200, 150, 400, 100, 500, 300, 400],
        "Average Buy Price": [88.50, 40.20, 28.10, 56.30, 88.60, 102.30, 68.20],
        "Current Price": [131.48, 48.17, 28.97, 66.42, 95.21, 111.92, 71.45],
        "Annual Dividend Per Unit": [4.48, 2.31, 1.54, 2.12, 4.72, 4.94, 4.45],
        "Franking %": [100, 100, 100, 100, 75, 0, 80]
    })

def classify_status(row):
    current_yield = row["Current Yield %"]
    allocation = row["Portfolio Allocation %"]
    if allocation > 25:
        return "Hold - concentration risk"
    if current_yield >= 5 and allocation < 20:
        return "Accumulate"
    if current_yield >= 3:
        return "Hold"
    return "Watch"

def prepare_data(df):
    required_cols = [
        "Ticker", "Name", "Asset Type", "Sector", "Units",
        "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    df = df.copy()
    numeric_cols = ["Units", "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Average Buy Price"]
    df["Capital Gain/Loss"] = df["Market Value"] - df["Cost Base"]
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Current Yield %"] = np.where(df["Market Value"] > 0, df["Annual Income"] / df["Market Value"] * 100, 0)
    df["Yield on Cost %"] = np.where(df["Cost Base"] > 0, df["Annual Income"] / df["Cost Base"] * 100, 0)

    # Franking credit estimate: gross-up factor for Australian company tax rate of 30%.
    df["Franking Credit Estimate"] = df["Annual Income"] * (df["Franking %"] / 100) * (30 / 70)

    total_value = df["Market Value"].sum()
    df["Portfolio Allocation %"] = np.where(total_value > 0, df["Market Value"] / total_value * 100, 0)
    df["Status"] = df.apply(classify_status, axis=1)
    return df

st.sidebar.title("📈 Wealth Builder")
st.sidebar.caption("Dividend Freedom Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Holdings", "Income Forecast", "What to Buy Next", "Upload Data", "About"]
)

target_income = st.sidebar.number_input(
    "Annual income goal",
    min_value=10000,
    max_value=500000,
    value=TARGET_INCOME_DEFAULT,
    step=5000
)

uploaded_file = st.sidebar.file_uploader("Upload holdings CSV", type=["csv"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
else:
    raw_df = load_sample_data()

df = prepare_data(raw_df)

portfolio_value = df["Market Value"].sum()
annual_income = df["Annual Income"].sum()
monthly_income = annual_income / 12
income_gap = max(target_income - annual_income, 0)
portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
estimated_required_portfolio = target_income / (portfolio_yield / 100) if portfolio_yield > 0 else 0
progress = min(annual_income / target_income * 100, 100) if target_income else 0

st.title("Dividend Freedom Dashboard")
st.caption("Educational portfolio tracker only — not financial advice.")

if page == "Dashboard":
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Portfolio Value", f"${portfolio_value:,.0f}")
    c2.metric("Annual Income", f"${annual_income:,.0f}")
    c3.metric("Monthly Income", f"${monthly_income:,.0f}")
    c4.metric("Income Goal", f"${target_income:,.0f}", f"{progress:.1f}% achieved")
    c5.metric("Income Gap", f"${income_gap:,.0f}")

    st.progress(progress / 100)
    st.subheader("Income Progress")
    st.write(f"You are generating **${annual_income:,.0f} per year**, against a target of **${target_income:,.0f} per year**.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Portfolio by Asset Type")
        asset_summary = df.groupby("Asset Type")["Market Value"].sum().sort_values(ascending=False)
        st.bar_chart(asset_summary)

    with col2:
        st.subheader("Annual Income by Holding")
        income_summary = df.set_index("Ticker")["Annual Income"].sort_values(ascending=False)
        st.bar_chart(income_summary)

    st.subheader("Key Numbers")
    st.dataframe(
        pd.DataFrame({
            "Metric": [
                "Portfolio value",
                "Annual dividend/distribution income",
                "Monthly income equivalent",
                "Current portfolio yield",
                "Estimated portfolio required at current yield",
                "Estimated franking credits"
            ],
            "Value": [
                f"${portfolio_value:,.0f}",
                f"${annual_income:,.0f}",
                f"${monthly_income:,.0f}",
                f"{portfolio_yield:.2f}%",
                f"${estimated_required_portfolio:,.0f}",
                f"${df['Franking Credit Estimate'].sum():,.0f}"
            ]
        }),
        hide_index=True,
        use_container_width=True
    )

elif page == "Holdings":
    st.subheader("Holdings Overview")
    display_cols = [
        "Ticker", "Name", "Asset Type", "Sector", "Units", "Average Buy Price",
        "Current Price", "Market Value", "Annual Income", "Current Yield %",
        "Yield on Cost %", "Portfolio Allocation %", "Status"
    ]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

elif page == "Income Forecast":
    st.subheader("Income Forecast")
    annual_contribution = st.number_input("Annual new investment", min_value=0, max_value=500000, value=25000, step=5000)
    assumed_yield = st.slider("Assumed future portfolio yield", 2.0, 8.0, float(round(portfolio_yield, 2)), 0.1)
    years = st.slider("Forecast years", 1, 30, 15)

    forecast = []
    value = portfolio_value
    for year in range(1, years + 1):
        value += annual_contribution
        income = value * assumed_yield / 100
        forecast.append({
            "Year": datetime.now().year + year,
            "Estimated Portfolio Value": value,
            "Estimated Annual Income": income,
            "Income Target": target_income
        })

    fdf = pd.DataFrame(forecast)
    st.line_chart(fdf.set_index("Year")[["Estimated Annual Income", "Income Target"]])
    st.dataframe(fdf, use_container_width=True, hide_index=True)

elif page == "What to Buy Next":
    st.subheader("Rules-Based Guidance")
    st.info("This is not a recommendation. It is a simple rules-based view to support education and discussion.")

    sector_alloc = df.groupby("Sector")["Market Value"].sum().reset_index()
    sector_alloc["Allocation %"] = sector_alloc["Market Value"] / portfolio_value * 100 if portfolio_value else 0
    st.write("### Sector Allocation")
    st.dataframe(sector_alloc.sort_values("Allocation %", ascending=False), use_container_width=True, hide_index=True)

    st.write("### Potential Accumulation Candidates")
    candidates = df[df["Status"].str.contains("Accumulate")].sort_values(["Current Yield %", "Portfolio Allocation %"], ascending=[False, True])
    if len(candidates) == 0:
        st.write("No holdings currently meet the simple accumulate rule.")
    else:
        st.dataframe(candidates[["Ticker", "Name", "Current Yield %", "Portfolio Allocation %", "Annual Income", "Status"]], use_container_width=True, hide_index=True)

    st.write("### Concentration Watch")
    concentration = df[df["Portfolio Allocation %"] > 25]
    if len(concentration) == 0:
        st.success("No single holding is above 25% of the portfolio in this sample.")
    else:
        st.warning("One or more holdings are above 25% allocation.")
        st.dataframe(concentration[["Ticker", "Name", "Portfolio Allocation %", "Market Value"]], use_container_width=True, hide_index=True)

elif page == "Upload Data":
    st.subheader("Upload Your Own Holdings")
    st.write("For privacy, test real data locally on your own PC rather than uploading personal wealth data to a public app.")
    st.write("CSV columns required:")
    st.code("Ticker,Name,Asset Type,Sector,Units,Average Buy Price,Current Price,Annual Dividend Per Unit,Franking %")
    st.download_button(
        label="Download sample CSV",
        data=load_sample_data().to_csv(index=False),
        file_name="sample_holdings.csv",
        mime="text/csv"
    )

else:
    st.subheader("About")
    st.write("""
This educational app helps track progress toward a dividend-funded retirement income goal.

It currently uses dummy data unless you upload a CSV. The first production version should be run locally on your PC for privacy.

Future versions could add live ASX pricing, automated ETF distribution history, tax/franking views, and broker export imports.
""")
