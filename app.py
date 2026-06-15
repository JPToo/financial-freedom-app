
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

TARGET_DEFAULT = 120000

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081427 0%, #101d34 100%);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #eef4ff 100%);
        border: 1px solid #dbe4f0;
        border-radius: 22px;
        padding: 24px 28px;
        margin-bottom: 18px;
        box-shadow: 0 8px 28px rgba(15, 23, 42, 0.06);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #475569;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #dbe4f0;
        border-radius: 18px;
        padding: 18px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.055);
        min-height: 126px;
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 25px;
        color: #0f172a;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .metric-delta-green {
        color: #16a34a;
        font-size: 13px;
        font-weight: 700;
    }

    .metric-delta-red {
        color: #dc2626;
        font-size: 13px;
        font-weight: 700;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #dbe4f0;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
        margin-bottom: 18px;
    }

    .panel-dark {
        background: linear-gradient(180deg, #0b1629 0%, #111d33 100%);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 20px;
        padding: 22px;
        color: white;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.16);
        margin-bottom: 18px;
    }

    .panel-title {
        font-size: 19px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 14px;
    }

    .panel-title-light {
        font-size: 19px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 14px;
    }

    .big-progress {
        font-size: 42px;
        font-weight: 900;
        color: #16a34a;
        text-align: center;
        margin-top: 15px;
    }

    .small-muted {
        color: #64748b;
        font-size: 13px;
    }

    .small-muted-light {
        color: #cbd5e1;
        font-size: 13px;
    }

    .recommend-good {
        background: rgba(22, 163, 74, 0.12);
        color: #166534;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 800;
    }

    .recommend-hold {
        background: rgba(245, 158, 11, 0.16);
        color: #92400e;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 800;
    }

    .recommend-watch {
        background: rgba(220, 38, 38, 0.12);
        color: #991b1b;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 800;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dbe4f0;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
    }

    .footer-note {
        color: #64748b;
        font-size: 12px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Data
# -----------------------------
@st.cache_data
def sample_data():
    return pd.DataFrame({
        "Ticker": ["CBA.AX", "BHP.AX", "WDS.AX", "WES.AX", "VAS.AX", "VGS.AX", "VHY.AX", "CASH"],
        "Name": [
            "Commonwealth Bank",
            "BHP Group",
            "Woodside Energy",
            "Wesfarmers",
            "Vanguard Australian Shares ETF",
            "Vanguard International Shares ETF",
            "Vanguard High Yield Australian Shares ETF",
            "Cash Position"
        ],
        "Asset Type": ["Share", "Share", "Share", "Share", "ETF", "ETF", "ETF", "Cash"],
        "Sector": ["Financials", "Resources", "Energy", "Industrials", "ETF - Australia", "ETF - International", "ETF - Dividend", "Cash"],
        "Units": [200, 150, 400, 100, 500, 300, 400, 1],
        "Average Buy Price": [88.50, 40.20, 28.10, 56.30, 88.60, 102.30, 68.20, 4734.00],
        "Current Price": [131.48, 48.17, 28.97, 66.42, 95.21, 111.92, 71.45, 4734.00],
        "Annual Dividend Per Unit": [4.48, 2.31, 1.54, 2.12, 4.72, 4.94, 4.45, 95.00],
        "Franking %": [100, 100, 100, 100, 75, 0, 80, 0]
    })

def clean_money(value):
    return f"${value:,.0f}"

def classify(row):
    if row["Portfolio Allocation %"] > 25:
        return "Hold"
    if row["Current Yield %"] >= 5 and row["Portfolio Allocation %"] < 20:
        return "Accumulate"
    if row["Current Yield %"] >= 3:
        return "Hold"
    return "Watch"

def prepare(df):
    required = ["Ticker", "Name", "Asset Type", "Sector", "Units", "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Your CSV is missing these columns: {missing}")
        st.stop()

    df = df.copy()
    for col in ["Units", "Average Buy Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Average Buy Price"]
    df["Capital Gain/Loss"] = df["Market Value"] - df["Cost Base"]
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Monthly Income"] = df["Annual Income"] / 12
    df["Daily Income"] = df["Annual Income"] / 365
    df["Current Yield %"] = np.where(df["Market Value"] > 0, df["Annual Income"] / df["Market Value"] * 100, 0)
    df["Yield on Cost %"] = np.where(df["Cost Base"] > 0, df["Annual Income"] / df["Cost Base"] * 100, 0)
    df["Franking Credit Estimate"] = df["Annual Income"] * (df["Franking %"] / 100) * (30 / 70)
    total_value = df["Market Value"].sum()
    df["Portfolio Allocation %"] = np.where(total_value > 0, df["Market Value"] / total_value * 100, 0)
    df["Status"] = df.apply(classify, axis=1)
    return df

def metric_card(label, value, delta="", delta_type="green"):
    delta_class = "metric-delta-green" if delta_type == "green" else "metric-delta-red"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="{delta_class}">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## 📈 Wealth Builder")
st.sidebar.markdown("Dividend Freedom")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Holdings", "Income Forecast", "What to Buy Next", "Upload Data", "About"]
)

target_income = st.sidebar.number_input(
    "Annual Income Goal",
    min_value=10000,
    max_value=500000,
    value=TARGET_DEFAULT,
    step=5000
)

uploaded = st.sidebar.file_uploader("Upload holdings CSV", type=["csv"])

if uploaded:
    raw = pd.read_csv(uploaded)
else:
    raw = sample_data()

df = prepare(raw)

portfolio_value = df["Market Value"].sum()
annual_income = df["Annual Income"].sum()
monthly_income = annual_income / 12
daily_income = annual_income / 365
income_gap = max(target_income - annual_income, 0)
portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
progress = min(annual_income / target_income * 100, 100) if target_income else 0
required_portfolio = target_income / (portfolio_yield / 100) if portfolio_yield else 0
franking = df["Franking Credit Estimate"].sum()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Income Goal")
st.sidebar.markdown(f"**{clean_money(target_income)} / year**")
st.sidebar.progress(progress / 100)
st.sidebar.caption(f"{progress:.1f}% complete")

# -----------------------------
# Pages
# -----------------------------
if page == "Dashboard":
    hero("Dashboard Overview", f"Your journey to {clean_money(target_income)} per year in dividend income")

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        metric_card("Portfolio Value", clean_money(portfolio_value), "+ sample portfolio", "green")
    with m2:
        metric_card("Annual Dividend Income", clean_money(annual_income), f"{portfolio_yield:.2f}% yield", "green")
    with m3:
        metric_card("Monthly Income", clean_money(monthly_income), f"{clean_money(daily_income)} / day", "green")
    with m4:
        metric_card("Income Goal", f"{clean_money(target_income)}", f"{progress:.1f}% of goal", "green")
    with m5:
        metric_card("Income Gap", clean_money(income_gap), f"{clean_money(income_gap/12)} / month", "red")
    with m6:
        metric_card("Portfolio Needed", clean_money(required_portfolio), f"at {portfolio_yield:.2f}% yield", "green")

    left, mid, right = st.columns([1.05, 1.55, 1.15])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Annual Income Progress</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-progress">{progress:.0f}%</div>', unsafe_allow_html=True)
        st.progress(progress / 100)
        st.markdown(f'<div class="small-muted" style="text-align:center;">{clean_money(annual_income)} of {clean_money(target_income)} annual goal</div>', unsafe_allow_html=True)
        years_to_goal = income_gap / max(annual_income * 0.10, 1)
        st.markdown(f"<br><center><b>{years_to_goal:.1f} years</b><br><span class='small-muted'>indicative at 10% income growth p.a.</span></center>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mid:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Income Forecast</div>', unsafe_allow_html=True)
        years = list(range(datetime.now().year, datetime.now().year + 11))
        forecast = []
        base_income = annual_income
        for i, y in enumerate(years):
            forecast.append({"Year": y, "Projected Income": base_income * ((1.08) ** i), "Goal": target_income})
        fdf = pd.DataFrame(forecast).set_index("Year")
        st.line_chart(fdf)
        st.markdown('<div class="small-muted">Assumes indicative 8% annual growth in dividend income. Educational only.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Portfolio Allocation</div>', unsafe_allow_html=True)
        alloc = df.groupby("Asset Type")["Market Value"].sum()
        st.bar_chart(alloc)
        st.markdown('<div class="small-muted">Good balance reduces reliance on one income source.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title-light">Holdings Snapshot</div>', unsafe_allow_html=True)
    view = df[["Ticker", "Name", "Asset Type", "Units", "Current Price", "Market Value", "Annual Income", "Current Yield %", "Portfolio Allocation %", "Status"]].copy()
    view["Current Price"] = view["Current Price"].map(lambda x: f"${x:,.2f}")
    view["Market Value"] = view["Market Value"].map(lambda x: f"${x:,.0f}")
    view["Annual Income"] = view["Annual Income"].map(lambda x: f"${x:,.0f}")
    view["Current Yield %"] = view["Current Yield %"].map(lambda x: f"{x:.2f}%")
    view["Portfolio Allocation %"] = view["Portfolio Allocation %"].map(lambda x: f"{x:.1f}%")
    st.dataframe(view, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Holdings":
    hero("Holdings Overview", "All your shares and ETFs in one place")

    left, right = st.columns([3.1, 1])
    with left:
        st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-light">Portfolio Table</div>', unsafe_allow_html=True)
        display = df[[
            "Ticker", "Name", "Asset Type", "Sector", "Units", "Average Buy Price",
            "Current Price", "Market Value", "Annual Income", "Yield on Cost %",
            "Current Yield %", "Status"
        ]].copy()
        st.dataframe(display, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel-dark">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-light">Income Summary</div>', unsafe_allow_html=True)
        st.markdown(f"**Annual Income:** {clean_money(annual_income)}")
        st.markdown(f"**Monthly Income:** {clean_money(monthly_income)}")
        st.markdown(f"**Daily Income:** {clean_money(daily_income)}")
        st.markdown(f"**Franking Estimate:** {clean_money(franking)}")
        st.markdown("---")
        st.markdown("### Top Contributors")
        top = df.sort_values("Annual Income", ascending=False).head(3)
        for _, row in top.iterrows():
            st.markdown(f"**{row['Ticker']}** — {clean_money(row['Annual Income'])}")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Income Forecast":
    hero("Goals & Projections", "Model the path to dividend-funded retirement income")

    annual_contribution = st.number_input("Annual new investment", min_value=0, max_value=500000, value=25000, step=5000)
    assumed_yield = st.slider("Assumed long-term portfolio yield", 2.0, 8.0, float(round(portfolio_yield, 2)), 0.1)
    assumed_growth = st.slider("Assumed annual capital growth", 0.0, 10.0, 4.0, 0.25)
    years_out = st.slider("Forecast years", 1, 30, 15)

    rows = []
    value = portfolio_value
    for i in range(1, years_out + 1):
        value = (value + annual_contribution) * (1 + assumed_growth / 100)
        income = value * assumed_yield / 100
        rows.append({"Year": datetime.now().year + i, "Portfolio Value": value, "Projected Income": income, "Goal": target_income})

    proj = pd.DataFrame(rows).set_index("Year")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Projected Annual Income</div>', unsafe_allow_html=True)
    st.line_chart(proj[["Projected Income", "Goal"]])
    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(proj.reset_index(), hide_index=True, use_container_width=True)

elif page == "What to Buy Next":
    hero("What to Buy Next", "Rules-based guidance to support your income goal")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Simple Decision Engine</div>', unsafe_allow_html=True)
    st.write("This is **not financial advice**. It simply checks income yield and concentration.")
    candidates = df.sort_values(["Status", "Current Yield %"], ascending=[True, False])
    st.dataframe(candidates[["Ticker", "Name", "Sector", "Current Yield %", "Portfolio Allocation %", "Annual Income", "Status"]], hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Concentration Watch</div>', unsafe_allow_html=True)
        high = df[df["Portfolio Allocation %"] > 25]
        if len(high):
            st.warning("One or more holdings are above 25% allocation.")
            st.dataframe(high[["Ticker", "Name", "Portfolio Allocation %"]], hide_index=True)
        else:
            st.success("No single holding is above 25% in the sample data.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Income Gap</div>', unsafe_allow_html=True)
        st.markdown(f"You still need **{clean_money(income_gap)}** per year to reach your target.")
        st.markdown(f"At the current sample yield of **{portfolio_yield:.2f}%**, that implies an estimated target portfolio of **{clean_money(required_portfolio)}**.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Upload Data":
    hero("Upload Data", "Bring your own holdings into the dashboard")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">CSV Format Required</div>', unsafe_allow_html=True)
    st.write("Your CSV must have these exact column headings:")
    st.code("Ticker,Name,Asset Type,Sector,Units,Average Buy Price,Current Price,Annual Dividend Per Unit,Franking %")
    st.download_button(
        "Download sample CSV",
        data=sample_data().to_csv(index=False),
        file_name="sample_holdings.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    hero("About", "Educational dividend freedom dashboard")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.write("""
This dashboard is designed to help visualise progress toward a dividend-funded retirement income goal.

Version 1 uses dummy data and manual CSV upload. Later versions can add live price feeds, dividend history, ETF distribution data, and a private local-PC workflow.
""")
    st.warning("Educational tool only. This is not financial advice.")
    st.markdown('</div>', unsafe_allow_html=True)
