
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Wealth Builder",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - Streamlit design closer to the mockup
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
}

.block-container {
    padding-top: 1.25rem;
    padding-left: 1.8rem;
    padding-right: 1.8rem;
    max-width: 1720px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071327 0%, #0b1a33 100%);
    width: 285px !important;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

div[data-testid="stSidebarUserContent"] {
    padding: 1.2rem 1rem;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 22px;
}

.logo-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #22c55e);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 22px;
    font-weight: 900;
}

.logo-title {
    font-size: 22px;
    font-weight: 900;
    line-height: 1.05;
}

.logo-sub {
    font-size: 13px;
    color: #cbd5e1 !important;
    margin-top: 2px;
}

.sidebar-card {
    background: rgba(255,255,255,0.065);
    border: 1px solid rgba(148,163,184,0.20);
    border-radius: 16px;
    padding: 15px;
    margin-top: 18px;
    margin-bottom: 14px;
}

.sidebar-card-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 11px;
}

.sidebar-muted {
    font-size: 12px;
    color: #cbd5e1 !important;
}

button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    border-radius: 12px !important;
}

.header-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 18px;
}

.page-title {
    font-size: 32px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: -0.6px;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 15px;
    color: #475569;
}

.top-actions {
    text-align: right;
    color: #0f172a;
    font-size: 13px;
    font-weight: 700;
}

.refresh-pill {
    display: inline-block;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 13px 18px;
    border-radius: 12px;
    font-weight: 800;
    margin-left: 12px;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.25);
}

.metric-card {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 18px;
    padding: 18px 18px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.055);
    min-height: 110px;
}

.metric-inner {
    display: flex;
    gap: 14px;
    align-items: center;
}

.metric-icon {
    width: 42px;
    height: 42px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.icon-green { background: #dcfce7; color: #16a34a; }
.icon-purple { background: #ede9fe; color: #7c3aed; }
.icon-blue { background: #dbeafe; color: #2563eb; }
.icon-orange { background: #ffedd5; color: #f97316; }
.icon-red { background: #fee2e2; color: #ef4444; }

.metric-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 800;
    margin-bottom: 4px;
}

.metric-value {
    color: #0f172a;
    font-size: 24px;
    line-height: 1.15;
    font-weight: 900;
}

.metric-sub-green {
    color: #16a34a;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
}

.metric-sub-red {
    color: #dc2626;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
}

.panel {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    margin-bottom: 18px;
}

.panel-title {
    color: #0f172a;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 14px;
}

.panel-sub {
    color: #64748b;
    font-size: 13px;
}

.progress-ring {
    width: 230px;
    height: 135px;
    border-radius: 230px 230px 0 0;
    background:
      radial-gradient(circle at 50% 100%, white 0 52%, transparent 53%),
      conic-gradient(from 270deg, #22c55e 0deg, #22c55e var(--angle), #e5e7eb var(--angle), #e5e7eb 180deg, transparent 180deg);
    margin: 16px auto 2px auto;
    position: relative;
}

.progress-number {
    text-align: center;
    font-size: 38px;
    color: #16a34a;
    font-weight: 900;
    margin-top: -18px;
}

.center {
    text-align: center;
}

.green-text {
    color: #16a34a;
    font-weight: 900;
}

.right-card {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
}

.right-title {
    color: #0f172a;
    font-size: 16px;
    font-weight: 900;
    margin-bottom: 12px;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    margin-bottom: 9px;
    color: #1e293b;
}

.summary-value {
    font-weight: 900;
}

.holdings-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 12px;
}

.pill-button {
    display: inline-block;
    border: 1px solid #dbe4f0;
    border-radius: 10px;
    padding: 10px 12px;
    color: #334155;
    background: #ffffff;
    font-size: 13px;
    font-weight: 700;
}

.add-button {
    display: inline-block;
    border-radius: 10px;
    padding: 10px 15px;
    color: white;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    font-size: 13px;
    font-weight: 800;
}

.total-row {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 14px;
    font-weight: 900;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.dataframe {
    font-size: 13px !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.stRadio > div {
    gap: 0.35rem;
}

.stRadio label {
    background: transparent;
    border-radius: 10px;
    padding: 2px 4px;
}

.footer-date {
    margin-top: 80px;
}

div[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(148,163,184,0.25) !important;
    border-radius: 14px !important;
}

@media (max-width: 900px) {
    .header-row {
        display: block;
    }
    .top-actions {
        text-align: left;
        margin-top: 10px;
    }
    .metric-value {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Data
# ============================================================
@st.cache_data
def sample_data():
    return pd.DataFrame([
        ["CBA.AX","🟡","Commonwealth Bank","Share","Financials","Bank",200,88.50,131.48,4.24,100],
        ["BHP.AX","🟠","BHP Group","Share","Resources","Mining",150,40.20,48.17,2.31,100],
        ["WDS.AX","🔴","Woodside Energy","Share","Energy","Energy",400,28.10,28.97,1.54,100],
        ["WES.AX","🟢","Wesfarmers","Share","Industrials","Retail",100,56.30,66.42,2.12,100],
        ["VAS.AX","🔴","Vanguard Aus Shares ETF","ETF","ETFs","Australian ETF",500,88.60,95.21,4.72,75],
        ["VGS.AX","🔴","Vanguard Intl Shares ETF","ETF","ETFs","International ETF",300,102.30,111.92,4.94,0],
        ["VHY.AX","🔴","Vanguard Aus High Yield ETF","ETF","ETFs","Dividend ETF",400,68.20,71.45,4.45,80],
        ["A200.AX","🔵","Betashares Australia 200 ETF","ETF","ETFs","Australian ETF",250,118.00,132.60,5.20,75],
        ["IVV.AX","🔵","iShares S&P 500 ETF","ETF","International Shares","US ETF",80,43.00,58.90,0.86,0],
        ["NAB.AX","🟡","National Australia Bank","Share","Financials","Bank",180,29.10,37.25,1.72,100],
        ["TCL.AX","🟣","Transurban","Share","Infrastructure","Infrastructure",450,13.10,12.80,0.62,0],
        ["CASH","🔵","Cash Position","Cash","Cash","Cash",1,12000.00,12000.00,240.00,0],
    ], columns=[
        "Symbol","Icon","Name","Asset Type","Sector","Sub Sector","Units",
        "Avg. Price","Current Price","Annual Dividend Per Unit","Franking %"
    ])

def prepare(df):
    df = df.copy()
    for col in ["Units", "Avg. Price", "Current Price", "Annual Dividend Per Unit", "Franking %"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Avg. Price"]
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Yield on Cost"] = np.where(df["Cost Base"] > 0, df["Annual Income"] / df["Cost Base"] * 100, 0)
    df["Current Yield"] = np.where(df["Market Value"] > 0, df["Annual Income"] / df["Market Value"] * 100, 0)
    df["Franking Credits"] = df["Annual Income"] * (df["Franking %"] / 100) * (30/70)
    total = df["Market Value"].sum()
    df["Allocation"] = np.where(total > 0, df["Market Value"] / total * 100, 0)

    def status(row):
        if row["Asset Type"] == "Cash":
            return "Hold"
        if row["Current Yield"] >= 5 and row["Allocation"] < 20:
            return "Accumulate"
        if row["Allocation"] > 25:
            return "Hold"
        return "Hold"

    df["Status"] = df.apply(status, axis=1)
    return df

def money(x):
    return f"${x:,.0f}"

def money2(x):
    return f"${x:,.2f}"

def metric(icon, icon_class, label, value, sub, red=False):
    sub_class = "metric-sub-red" if red else "metric-sub-green"
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-inner">
        <div class="metric-icon {icon_class}">{icon}</div>
        <div>
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="{sub_class}">{sub}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# Sidebar
# ============================================================
st.sidebar.markdown("""
<div class="sidebar-logo">
  <div class="logo-icon">↗</div>
  <div>
    <div class="logo-title">Wealth Builder</div>
    <div class="logo-sub">Dividend Freedom</div>
  </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Portfolio", "Income", "Holdings", "ETFs", "What to Buy Next", "Goals & Projections", "Reports", "Settings"],
    index=0
)

target_income = st.sidebar.number_input("Annual Income Goal", min_value=10000, max_value=500000, value=120000, step=5000)

raw = sample_data()
df = prepare(raw)

portfolio_value = df["Market Value"].sum()
annual_income = df["Annual Income"].sum()
monthly_income = annual_income / 12
daily_income = annual_income / 365
income_gap = max(target_income - annual_income, 0)
portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
progress = min(annual_income / target_income * 100, 100) if target_income else 0
needed = target_income / (portfolio_yield / 100) if portfolio_yield else 0
franking = df["Franking Credits"].sum()

st.sidebar.markdown(f"""
<div class="sidebar-card">
  <div class="sidebar-card-title">Income Goal</div>
  <div style="font-size:19px; font-weight:900;">{money(target_income)} <span style="font-size:13px; font-weight:500;">/ year</span></div>
  <div style="height:10px; background:rgba(255,255,255,0.14); border-radius:999px; margin:14px 0 8px 0;">
    <div style="height:10px; width:{progress}%; background:linear-gradient(90deg,#22c55e,#2563eb); border-radius:999px;"></div>
  </div>
  <div class="sidebar-muted">{progress:.0f}% &nbsp;&nbsp;&nbsp; {money(annual_income)} of {money(target_income)}</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.sidebar.file_uploader("Upload holdings CSV", type=["csv"])
if uploaded:
    df = prepare(pd.read_csv(uploaded))
    portfolio_value = df["Market Value"].sum()
    annual_income = df["Annual Income"].sum()
    monthly_income = annual_income / 12
    daily_income = annual_income / 365
    income_gap = max(target_income - annual_income, 0)
    portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
    progress = min(annual_income / target_income * 100, 100) if target_income else 0
    needed = target_income / (portfolio_yield / 100) if portfolio_yield else 0
    franking = df["Franking Credits"].sum()

st.sidebar.markdown("""
<div class="footer-date">
  <div class="sidebar-muted">Market closed</div>
  <div class="sidebar-muted">as of 24 May 2025</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄 Refresh Data", use_container_width=True, type="primary"):
    st.cache_data.clear()

# ============================================================
# Dashboard
# ============================================================
if page == "Dashboard":
    st.markdown(f"""
    <div class="header-row">
      <div>
        <div class="page-title">Dashboard Overview</div>
        <div class="page-subtitle">Your journey to {money(target_income)} per year in dividend income</div>
      </div>
      <div class="top-actions">
        Market closed<br>
        <span style="font-weight:500; color:#64748b;">as of 24 May 2025</span>
        <span class="refresh-pill">↻ Refresh Data</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(6)
    with cols[0]:
        metric("$", "icon-green", "Portfolio Value", money(portfolio_value), "+1.35% (1D)")
    with cols[1]:
        metric("◔", "icon-purple", "Annual Dividend Income", money(annual_income), "+3.12% (1M)")
    with cols[2]:
        metric("▣", "icon-blue", "Monthly Income", money(monthly_income), "+3.12% (1M)")
    with cols[3]:
        metric("◎", "icon-orange", "Income Goal", f"{money(target_income)} <span style='font-size:14px;'>/ year</span>", f"{progress:.0f}% of goal")
    with cols[4]:
        metric("⌄", "icon-red", "Income Gap", f"{money(income_gap)} <span style='font-size:14px;'>/ year</span>", f"{money(income_gap/12)} / month", red=True)
    with cols[5]:
        metric("↗", "icon-green", "Est. Portfolio Needed", f"${needed/1_000_000:.2f}M", f"at {portfolio_yield:.1f}% yield")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    left, mid, right = st.columns([1.1, 1.55, 1.2])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Annual Dividend Income Progress</div>', unsafe_allow_html=True)
        angle = min(progress, 100) * 1.8
        st.markdown(f'<div class="progress-ring" style="--angle:{angle}deg;"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-number">{progress:.0f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center panel-sub">{money(annual_income)} of {money(target_income)}<br>annual goal</div>', unsafe_allow_html=True)
        years_to_goal = income_gap / max(18000 * portfolio_yield / 100, 1)
        st.markdown("<hr style='border:none; border-top:1px solid #e2e8f0; margin:20px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='center panel-sub'>On track to reach your goal in</div><div class='center green-text' style='font-size:24px;'>{years_to_goal:.1f} years</div><div class='center panel-sub'>with current contributions</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mid:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Income Forecast</div>', unsafe_allow_html=True)
        years = list(range(2025, 2037))
        rows = []
        for i, y in enumerate(years):
            rows.append({
                "Year": y,
                "Projected Income": annual_income * (1.135 ** i),
                "Current Trend": annual_income * (1.085 ** i),
                "Goal": target_income
            })
        fc = pd.DataFrame(rows).set_index("Year")
        st.line_chart(fc)
        st.markdown("<div class='panel-sub'>Assumes average annual investment of $18,000 and current average yield</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Portfolio Allocation</div>', unsafe_allow_html=True)
        allocation = df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False)
        st.bar_chart(allocation)
        st.markdown("<div class='center green-text'>✓ Well diversified</div><div class='center panel-sub'>Good balance across asset classes</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    lower_left, lower_right = st.columns([3.2, 0.9])

    with lower_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("""
        <div class="holdings-header">
          <div>
            <div class="panel-title" style="margin-bottom:2px;">Holdings Overview</div>
            <div class="panel-sub">All your shares and ETFs in one place</div>
          </div>
          <div>
            <span class="pill-button">All Assets ▾</span>
            <span class="pill-button">All Sectors ▾</span>
            <span class="pill-button">🔍 Search holdings...</span>
            <span class="add-button">+ Add Holding</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        display = df[["Icon","Symbol","Name","Asset Type","Units","Avg. Price","Current Price","Market Value","Annual Income","Yield on Cost","Current Yield","Status"]].copy()
        display["Symbol"] = display["Icon"] + "  " + display["Symbol"]
        display = display.drop(columns=["Icon"])
        display["Avg. Price"] = display["Avg. Price"].map(money2)
        display["Current Price"] = display["Current Price"].map(money2)
        display["Market Value"] = display["Market Value"].map(money)
        display["Annual Income"] = display["Annual Income"].map(money)
        display["Yield on Cost"] = display["Yield on Cost"].map(lambda x: f"{x:.2f}%")
        display["Current Yield"] = display["Current Yield"].map(lambda x: f"{x:.2f}%")
        st.dataframe(display, use_container_width=True, hide_index=True, height=390)

        st.markdown(f"""
        <div class="total-row">
          <div>Total / Weighted Average</div>
          <div>{int(df['Units'].sum()):,} units &nbsp;&nbsp;&nbsp; {money(portfolio_value)} &nbsp;&nbsp;&nbsp; {money(annual_income)} &nbsp;&nbsp;&nbsp; {portfolio_yield:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with lower_right:
        st.markdown('<div class="right-card">', unsafe_allow_html=True)
        st.markdown('<div class="right-title">Income Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-row"><span>Annual Dividend Income</span><span class="summary-value">{money(annual_income)}</span></div>
        <div class="summary-row"><span>Monthly Income</span><span class="summary-value">{money(monthly_income)}</span></div>
        <div class="summary-row"><span>Daily Income</span><span class="summary-value">{money2(daily_income)}</span></div>
        <div class="summary-row"><span>Franking Credits (est.)</span><span class="summary-value">{money(franking)}</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="right-card">', unsafe_allow_html=True)
        st.markdown('<div class="right-title">Sector Exposure</div>', unsafe_allow_html=True)
        sector = df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False)
        for k, v in sector.head(6).items():
            p = v / portfolio_value * 100
            st.markdown(f"""
            <div class="summary-row"><span>{k}</span><span class="summary-value">{p:.1f}%</span></div>
            <div style="height:7px; background:#e5e7eb; border-radius:99px; margin-bottom:8px;">
              <div style="height:7px; width:{min(p,100)}%; background:linear-gradient(90deg,#2563eb,#7c3aed); border-radius:99px;"></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="right-card">', unsafe_allow_html=True)
        st.markdown('<div class="right-title">Top Income Contributors</div>', unsafe_allow_html=True)
        top = df.sort_values("Annual Income", ascending=False).head(3)
        for _, r in top.iterrows():
            pct_income = r["Annual Income"] / annual_income * 100 if annual_income else 0
            st.markdown(f"<div class='summary-row'><span><b>{r['Symbol']}</b></span><span class='summary-value'>{money(r['Annual Income'])} ({pct_income:.1f}%)</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="header-row">
      <div>
        <div class="page-title">{page}</div>
        <div class="page-subtitle">This page will be expanded in the next build.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.write("The main dashboard design is now the focus. Once you are happy with the look, we will build out this section properly.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
