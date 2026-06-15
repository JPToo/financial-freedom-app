
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Financial Freedom Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: #f4f7fb;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061224 0%, #0d1b33 100%);
        min-width: 285px;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    div[data-testid="stSidebarUserContent"] {
        padding-top: 1rem;
    }

    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #edf4ff 100%);
        border: 1px solid #dbe5f2;
        border-radius: 24px;
        padding: 26px 30px;
        margin-bottom: 20px;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #475569;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #dbe5f2;
        border-radius: 20px;
        padding: 18px 18px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.055);
        height: 124px;
    }

    .metric-label {
        font-size: 12px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 24px;
        color: #0f172a;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .metric-green {
        color: #16a34a;
        font-size: 12px;
        font-weight: 800;
    }

    .metric-red {
        color: #dc2626;
        font-size: 12px;
        font-weight: 800;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #dbe5f2;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
        margin-bottom: 20px;
    }

    .panel-dark {
        background: linear-gradient(180deg, #081427 0%, #101d34 100%);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 22px;
        padding: 24px;
        color: #f8fafc;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14);
        margin-bottom: 20px;
    }

    .panel-title {
        font-size: 20px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 14px;
    }

    .panel-title-light {
        font-size: 20px;
        font-weight: 900;
        color: #f8fafc;
        margin-bottom: 14px;
    }

    .muted {
        color: #64748b;
        font-size: 13px;
    }

    .muted-light {
        color: #cbd5e1;
        font-size: 13px;
    }

    .progress-big {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        color: #16a34a;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    .status-good {
        background: rgba(22, 163, 74, 0.12);
        color: #166534;
        border-radius: 999px;
        padding: 5px 10px;
        font-weight: 800;
        font-size: 12px;
    }

    .status-hold {
        background: rgba(245, 158, 11, 0.16);
        color: #92400e;
        border-radius: 999px;
        padding: 5px 10px;
        font-weight: 800;
        font-size: 12px;
    }

    .status-watch {
        background: rgba(220, 38, 38, 0.12);
        color: #991b1b;
        border-radius: 999px;
        padding: 5px 10px;
        font-weight: 800;
        font-size: 12px;
    }

    .mini-pill {
        display: inline-block;
        background: #eef4ff;
        border: 1px solid #dbe5f2;
        color: #1e293b;
        padding: 7px 11px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .sidebar-note {
        font-size: 12px;
        color: #cbd5e1;
    }

    h1, h2, h3 {
        color: #0f172a;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    .stProgress > div > div > div > div {
        background-color: #16a34a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Dummy Data
# ============================================================
@st.cache_data
def sample_data():
    data = [
        ["CBA.AX", "Commonwealth Bank", "Share", "Financials", "Bank", 220, 92.40, 131.48, 4.65, 100, "Quarterly", "Large cap bank"],
        ["NAB.AX", "National Australia Bank", "Share", "Financials", "Bank", 520, 29.10, 37.25, 1.72, 100, "Semi-annual", "Large cap bank"],
        ["WBC.AX", "Westpac Banking Corp", "Share", "Financials", "Bank", 610, 22.80, 28.95, 1.50, 100, "Semi-annual", "Large cap bank"],
        ["ANZ.AX", "ANZ Group", "Share", "Financials", "Bank", 430, 24.60, 30.10, 1.66, 100, "Semi-annual", "Large cap bank"],

        ["BHP.AX", "BHP Group", "Share", "Resources", "Mining", 380, 38.25, 43.60, 2.20, 100, "Semi-annual", "Major miner"],
        ["RIO.AX", "Rio Tinto", "Share", "Resources", "Mining", 95, 103.00, 126.20, 5.60, 100, "Semi-annual", "Major miner"],
        ["FMG.AX", "Fortescue", "Share", "Resources", "Mining", 420, 18.90, 23.40, 1.60, 100, "Semi-annual", "Iron ore"],
        ["WDS.AX", "Woodside Energy", "Share", "Energy", "Energy", 650, 27.80, 28.97, 1.54, 100, "Semi-annual", "Energy / LNG"],

        ["WES.AX", "Wesfarmers", "Share", "Industrials", "Retail / Industrial", 160, 54.10, 67.80, 2.06, 100, "Semi-annual", "Quality industrial"],
        ["WOW.AX", "Woolworths Group", "Share", "Consumer Staples", "Retail", 210, 34.50, 32.15, 1.04, 100, "Semi-annual", "Defensive retail"],
        ["COL.AX", "Coles Group", "Share", "Consumer Staples", "Retail", 290, 15.60, 17.90, 0.72, 100, "Semi-annual", "Defensive retail"],
        ["TCL.AX", "Transurban", "Share", "Infrastructure", "Toll roads", 900, 13.10, 12.80, 0.62, 0, "Semi-annual", "Infrastructure income"],

        ["CSL.AX", "CSL", "Share", "Healthcare", "Healthcare", 38, 278.00, 289.50, 4.10, 10, "Semi-annual", "Growth / healthcare"],
        ["RMD.AX", "ResMed", "Share", "Healthcare", "Healthcare", 85, 28.40, 34.75, 0.24, 0, "Quarterly", "Growth / healthcare"],
        ["GMG.AX", "Goodman Group", "Share", "Property", "Industrial property", 260, 19.90, 33.10, 0.30, 0, "Semi-annual", "Property growth"],
        ["SCG.AX", "Scentre Group", "Share", "Property", "Retail property", 1350, 2.75, 3.40, 0.17, 0, "Semi-annual", "Property income"],

        ["VAS.AX", "Vanguard Australian Shares ETF", "ETF", "ETF - Australia", "Broad market ETF", 980, 86.30, 101.50, 4.80, 75, "Quarterly", "Core Australian ETF"],
        ["VHY.AX", "Vanguard Australian High Yield ETF", "ETF", "ETF - Dividend", "Dividend ETF", 720, 63.20, 70.85, 4.70, 80, "Quarterly", "High yield ETF"],
        ["VGS.AX", "Vanguard International Shares ETF", "ETF", "ETF - International", "Global ETF", 620, 95.80, 128.40, 3.15, 0, "Quarterly", "Global diversification"],
        ["IVV.AX", "iShares S&P 500 ETF", "ETF", "ETF - International", "US ETF", 140, 42.50, 58.90, 0.86, 0, "Quarterly", "US market exposure"],
        ["A200.AX", "Betashares Australia 200 ETF", "ETF", "ETF - Australia", "Broad market ETF", 690, 112.30, 132.60, 5.20, 75, "Quarterly", "Low-cost Australian ETF"],
        ["HACK.AX", "Betashares Global Cybersecurity ETF", "ETF", "ETF - Thematic", "Technology ETF", 230, 9.40, 12.15, 0.10, 0, "Annual", "Thematic growth"],

        ["CASH", "Cash / Offset", "Cash", "Cash", "Cash", 1, 35000.00, 35000.00, 1400.00, 0, "Monthly", "Cash buffer"]
    ]

    return pd.DataFrame(data, columns=[
        "Ticker", "Name", "Asset Type", "Sector", "Sub Sector", "Units",
        "Average Buy Price", "Current Price", "Annual Dividend Per Unit",
        "Franking %", "Payment Frequency", "Notes"
    ])

# ============================================================
# Helpers
# ============================================================
def money(x):
    return f"${x:,.0f}"

def money2(x):
    return f"${x:,.2f}"

def pct(x):
    return f"{x:.1f}%"

def classify(row):
    if row["Asset Type"] == "Cash":
        return "Hold"
    if row["Portfolio Allocation %"] > 12 and row["Asset Type"] == "Share":
        return "Hold"
    if row["Current Yield %"] >= 5.0 and row["Portfolio Allocation %"] < 10:
        return "Accumulate"
    if row["Current Yield %"] < 1.5 and row["Asset Type"] != "ETF":
        return "Watch"
    return "Hold"

def prepare(df):
    required = [
        "Ticker", "Name", "Asset Type", "Sector", "Sub Sector", "Units",
        "Average Buy Price", "Current Price", "Annual Dividend Per Unit",
        "Franking %", "Payment Frequency", "Notes"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"CSV is missing columns: {missing}")
        st.stop()

    df = df.copy()
    for col in ["Units", "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Average Buy Price"]
    df["Capital Gain/Loss"] = df["Market Value"] - df["Cost Base"]
    df["Capital Gain/Loss %"] = np.where(df["Cost Base"] > 0, df["Capital Gain/Loss"] / df["Cost Base"] * 100, 0)
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Monthly Income"] = df["Annual Income"] / 12
    df["Current Yield %"] = np.where(df["Market Value"] > 0, df["Annual Income"] / df["Market Value"] * 100, 0)
    df["Yield on Cost %"] = np.where(df["Cost Base"] > 0, df["Annual Income"] / df["Cost Base"] * 100, 0)
    df["Franking Credit Estimate"] = df["Annual Income"] * (df["Franking %"] / 100) * (30 / 70)
    total_value = df["Market Value"].sum()
    df["Portfolio Allocation %"] = np.where(total_value > 0, df["Market Value"] / total_value * 100, 0)
    df["Status"] = df.apply(classify, axis=1)
    return df

def card(label, value, sub="", red=False):
    cls = "metric-red" if red else "metric-green"
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="{cls}">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f"""
    <div class="hero">
      <div class="hero-title">{title}</div>
      <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# Sidebar
# ============================================================
st.sidebar.markdown("## 📈 Wealth Builder")
st.sidebar.markdown("**Dividend Freedom**")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Holdings", "Income Forecast", "What to Buy Next", "Upload Data", "About"]
)

target_income = st.sidebar.number_input(
    "Annual Income Goal",
    min_value=10000,
    max_value=500000,
    value=120000,
    step=5000
)

uploaded = st.sidebar.file_uploader("Upload holdings CSV", type=["csv"])

raw = pd.read_csv(uploaded) if uploaded else sample_data()
df = prepare(raw)

portfolio_value = df["Market Value"].sum()
annual_income = df["Annual Income"].sum()
monthly_income = annual_income / 12
daily_income = annual_income / 365
income_gap = max(target_income - annual_income, 0)
portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
progress = min(annual_income / target_income * 100, 100)
required_portfolio = target_income / (portfolio_yield / 100) if portfolio_yield else 0
franking = df["Franking Credit Estimate"].sum()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Income Goal")
st.sidebar.markdown(f"**{money(target_income)} / year**")
st.sidebar.progress(progress / 100)
st.sidebar.caption(f"{progress:.1f}% complete")
st.sidebar.markdown(f"<span class='sidebar-note'>Current income: {money(annual_income)} / year</span>", unsafe_allow_html=True)

# ============================================================
# Dashboard
# ============================================================
if page == "Dashboard":
    hero("Dashboard Overview", f"Your journey to {money(target_income)} per year in dividend income")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: card("Portfolio Value", money(portfolio_value), "dummy sample portfolio")
    with c2: card("Annual Income", money(annual_income), f"{portfolio_yield:.2f}% portfolio yield")
    with c3: card("Monthly Income", money(monthly_income), f"{money(daily_income)} / day")
    with c4: card("Income Goal", money(target_income), f"{progress:.1f}% complete")
    with c5: card("Income Gap", money(income_gap), f"{money(income_gap/12)} / month", red=True)
    with c6: card("Portfolio Needed", money(required_portfolio), f"at {portfolio_yield:.2f}% yield")

    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1.05, 1.5, 1.1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Annual Income Progress</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-big">{progress:.0f}%</div>', unsafe_allow_html=True)
        st.progress(progress / 100)
        st.markdown(f"<center><span class='muted'>{money(annual_income)} of {money(target_income)} annual goal</span></center>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<center><b>{money(income_gap)}</b><br><span class='muted'>income gap still to close</span></center>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with middle:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Income Forecast</div>', unsafe_allow_html=True)
        years = list(range(datetime.now().year, datetime.now().year + 12))
        rows = []
        for i, y in enumerate(years):
            rows.append({
                "Year": y,
                "Current Trend": annual_income * ((1.06) ** i),
                "Accelerated Plan": annual_income * ((1.11) ** i),
                "Goal": target_income
            })
        forecast = pd.DataFrame(rows).set_index("Year")
        st.line_chart(forecast)
        st.markdown("<span class='muted'>Dummy forecast only. Real version will let you set contributions, growth and dividend assumptions.</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Portfolio Allocation</div>', unsafe_allow_html=True)
        allocation = df.groupby("Asset Type")["Market Value"].sum().sort_values(ascending=False)
        st.bar_chart(allocation)
        st.markdown("<span class='muted'>Shares, ETFs and cash now shown as separate buckets.</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    b1, b2, b3 = st.columns([1.25, 1.25, 1])
    with b1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Top Income Contributors</div>', unsafe_allow_html=True)
        top = df.sort_values("Annual Income", ascending=False).head(7)
        st.bar_chart(top.set_index("Ticker")["Annual Income"])
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Sector Exposure</div>', unsafe_allow_html=True)
        sectors = df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(sectors)
        st.markdown('</div>', unsafe_allow_html=True)

    with b3:
        st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-light">Income Summary</div>', unsafe_allow_html=True)
        st.markdown(f"**Annual income:** {money(annual_income)}")
        st.markdown(f"**Monthly income:** {money(monthly_income)}")
        st.markdown(f"**Daily income:** {money(daily_income)}")
        st.markdown(f"**Franking estimate:** {money(franking)}")
        st.markdown("---")
        st.markdown("### Risk Notes")
        st.markdown(f"<span class='muted-light'>Largest holding: {df.sort_values('Market Value', ascending=False).iloc[0]['Ticker']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='muted-light'>Highest yield: {df.sort_values('Current Yield %', ascending=False).iloc[0]['Ticker']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title-light">Holdings Snapshot</div>', unsafe_allow_html=True)
    snap = df[["Ticker", "Name", "Asset Type", "Sector", "Units", "Market Value", "Annual Income", "Current Yield %", "Portfolio Allocation %", "Status"]].copy()
    snap["Market Value"] = snap["Market Value"].map(money)
    snap["Annual Income"] = snap["Annual Income"].map(money)
    snap["Current Yield %"] = snap["Current Yield %"].map(lambda x: f"{x:.2f}%")
    snap["Portfolio Allocation %"] = snap["Portfolio Allocation %"].map(lambda x: f"{x:.1f}%")
    st.dataframe(snap, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Holdings
# ============================================================
elif page == "Holdings":
    hero("Holdings Overview", "All shares, ETFs and cash in one place")

    st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title-light">Portfolio Holdings</div>', unsafe_allow_html=True)
    view = df[[
        "Ticker", "Name", "Asset Type", "Sector", "Sub Sector", "Units",
        "Average Buy Price", "Current Price", "Market Value", "Annual Income",
        "Current Yield %", "Yield on Cost %", "Franking %", "Payment Frequency", "Status"
    ]].copy()
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Forecast
# ============================================================
elif page == "Income Forecast":
    hero("Income Forecast", "Test how contributions and yield change your retirement income path")

    annual_contribution = st.number_input("Annual new investment", min_value=0, max_value=500000, value=35000, step=5000)
    assumed_yield = st.slider("Assumed future portfolio yield", 2.0, 8.0, float(round(portfolio_yield, 2)), 0.1)
    assumed_growth = st.slider("Assumed annual capital growth", 0.0, 10.0, 4.0, 0.25)
    years_out = st.slider("Forecast years", 1, 30, 20)

    rows = []
    value = portfolio_value
    for i in range(1, years_out + 1):
        value = (value + annual_contribution) * (1 + assumed_growth / 100)
        income = value * assumed_yield / 100
        rows.append({
            "Year": datetime.now().year + i,
            "Portfolio Value": value,
            "Projected Income": income,
            "Goal": target_income,
            "Income Gap": max(target_income - income, 0)
        })
    proj = pd.DataFrame(rows)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Projected Annual Dividend Income</div>', unsafe_allow_html=True)
    st.line_chart(proj.set_index("Year")[["Projected Income", "Goal"]])
    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(proj, use_container_width=True, hide_index=True)

# ============================================================
# What to Buy Next
# ============================================================
elif page == "What to Buy Next":
    hero("What to Buy Next", "A rules-based view to guide the next dollar invested")

    s1, s2 = st.columns(2)

    with s1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Accumulation Candidates</div>', unsafe_allow_html=True)
        acc = df[df["Status"] == "Accumulate"].sort_values("Current Yield %", ascending=False)
        if len(acc):
            st.dataframe(acc[["Ticker", "Name", "Sector", "Current Yield %", "Portfolio Allocation %", "Annual Income", "Notes"]], use_container_width=True, hide_index=True)
        else:
            st.info("No holdings meet the simple accumulate rule in this sample.")
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Concentration Watch</div>', unsafe_allow_html=True)
        high = df[df["Portfolio Allocation %"] > 12].sort_values("Portfolio Allocation %", ascending=False)
        if len(high):
            st.warning("These holdings are above 12% of the sample portfolio.")
            st.dataframe(high[["Ticker", "Name", "Portfolio Allocation %", "Market Value"]], use_container_width=True, hide_index=True)
        else:
            st.success("No holdings above the concentration threshold.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Decision Engine Logic</div>', unsafe_allow_html=True)
    st.markdown("""
    <span class="mini-pill">Accumulate: yield ≥ 5% and allocation < 10%</span>
    <span class="mini-pill">Hold: quality/income position or already enough exposure</span>
    <span class="mini-pill">Watch: low yield single share or concentration issue</span>
    """, unsafe_allow_html=True)
    st.warning("This is educational and rules-based only. It is not financial advice.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Upload
# ============================================================
elif page == "Upload Data":
    hero("Upload Data", "Use a CSV as the first simple database")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Required CSV Columns</div>', unsafe_allow_html=True)
    st.code("Ticker,Name,Asset Type,Sector,Sub Sector,Units,Average Buy Price,Current Price,Annual Dividend Per Unit,Franking %,Payment Frequency,Notes")
    st.download_button(
        "Download richer sample CSV",
        data=sample_data().to_csv(index=False),
        file_name="sample_holdings_richer.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# About
# ============================================================
else:
    hero("About", "Educational app for dividend-funded retirement planning")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.write("""
This app is a prototype. It currently uses dummy data or CSV upload.

The next useful improvements are:
- live price lookup,
- dividend history,
- better ETF distribution data,
- local PC private version,
- iPhone-friendly layout,
- login/security for private use.
""")
    st.warning("Educational only. Not financial advice.")
    st.markdown('</div>', unsafe_allow_html=True)
