
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Wealth Builder",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    padding-top: 1.0rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 1700px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071327 0%, #0b1a33 100%);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

.sidebar-logo {
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:20px;
}

.logo-icon {
    width:36px;
    height:36px;
    border-radius:12px;
    background:linear-gradient(135deg,#2563eb,#22c55e);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:20px;
    font-weight:900;
}

.logo-title {
    font-size:21px;
    font-weight:900;
    line-height:1.05;
}

.logo-sub {
    font-size:13px;
    color:#cbd5e1 !important;
}

.sidebar-card {
    background:rgba(255,255,255,0.065);
    border:1px solid rgba(148,163,184,0.2);
    border-radius:16px;
    padding:15px;
    margin:16px 0;
}

.header-row {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:16px;
}

.page-title {
    font-size:32px;
    font-weight:900;
    color:#0f172a;
    letter-spacing:-0.6px;
    margin-bottom:4px;
}

.page-subtitle {
    font-size:15px;
    color:#475569;
}

.top-actions {
    text-align:right;
    color:#0f172a;
    font-size:13px;
    font-weight:700;
}

.refresh-pill {
    display:inline-block;
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
    color:white;
    padding:12px 17px;
    border-radius:12px;
    font-weight:800;
    margin-left:12px;
    box-shadow:0 8px 18px rgba(37,99,235,0.25);
}

.metric-card {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:17px 17px;
    box-shadow:0 8px 22px rgba(15,23,42,0.055);
    min-height:108px;
}

.metric-inner {
    display:flex;
    gap:13px;
    align-items:center;
}

.metric-icon {
    width:42px;
    height:42px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
    flex-shrink:0;
}

.icon-green { background:#dcfce7; color:#16a34a; }
.icon-purple { background:#ede9fe; color:#7c3aed; }
.icon-blue { background:#dbeafe; color:#2563eb; }
.icon-orange { background:#ffedd5; color:#f97316; }
.icon-red { background:#fee2e2; color:#ef4444; }

.metric-label {
    font-size:12px;
    color:#64748b;
    font-weight:800;
    margin-bottom:4px;
}

.metric-value {
    color:#0f172a;
    font-size:23px;
    line-height:1.15;
    font-weight:900;
}

.metric-sub-green {
    color:#16a34a;
    font-size:12px;
    font-weight:800;
    margin-top:4px;
}

.metric-sub-red {
    color:#dc2626;
    font-size:12px;
    font-weight:800;
    margin-top:4px;
}

.panel {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:21px;
    box-shadow:0 8px 22px rgba(15,23,42,0.05);
    margin-bottom:18px;
}

.panel-title {
    color:#0f172a;
    font-size:18px;
    font-weight:900;
    margin-bottom:14px;
}

.panel-sub {
    color:#64748b;
    font-size:13px;
}

.progress-ring {
    width:220px;
    height:130px;
    border-radius:220px 220px 0 0;
    background:
      radial-gradient(circle at 50% 100%, white 0 52%, transparent 53%),
      conic-gradient(from 270deg, #22c55e 0deg, #22c55e var(--angle), #e5e7eb var(--angle), #e5e7eb 180deg, transparent 180deg);
    margin:14px auto 2px auto;
}

.progress-number {
    text-align:center;
    font-size:36px;
    color:#16a34a;
    font-weight:900;
    margin-top:-16px;
}

.center { text-align:center; }
.green-text { color:#16a34a; font-weight:900; }

.right-card {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:16px;
    padding:16px;
    margin-bottom:14px;
    box-shadow:0 8px 20px rgba(15,23,42,0.04);
}

.right-title {
    color:#0f172a;
    font-size:16px;
    font-weight:900;
    margin-bottom:12px;
}

.summary-row {
    display:flex;
    justify-content:space-between;
    font-size:13px;
    margin-bottom:9px;
    color:#1e293b;
}

.summary-value { font-weight:900; }

.holdings-header {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    margin-bottom:12px;
}

.pill-button {
    display:inline-block;
    border:1px solid #dbe4f0;
    border-radius:10px;
    padding:10px 12px;
    color:#334155;
    background:#ffffff;
    font-size:13px;
    font-weight:700;
}

.add-button {
    display:inline-block;
    border-radius:10px;
    padding:10px 15px;
    color:white;
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
    font-size:13px;
    font-weight:800;
}

.total-row {
    background:#f8fafc;
    border:1px solid #e2e8f0;
    border-radius:12px;
    padding:14px 16px;
    font-size:14px;
    font-weight:900;
    color:#0f172a;
    display:flex;
    justify-content:space-between;
    margin-top:10px;
}

div[data-testid="stDataFrame"] {
    border-radius:14px;
    overflow:hidden;
    border:1px solid #e2e8f0;
}

.mobile-only {
    display:none;
}

.desktop-only {
    display:block;
}

/* iPhone / mobile improvements */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.85rem;
        padding-right: 0.85rem;
        padding-top: 0.5rem;
    }

    .desktop-only {
        display:none !important;
    }

    .mobile-only {
        display:block !important;
    }

    .header-row {
        display:block;
        margin-bottom:10px;
    }

    .page-title {
        font-size:28px;
        line-height:1.05;
        letter-spacing:-0.4px;
        margin-top: 0.4rem;
    }

    .page-subtitle {
        font-size:14px;
        line-height:1.35;
    }

    .top-actions {
        text-align:left;
        margin-top:12px;
        font-size:13px;
    }

    .refresh-pill {
        margin-left:0;
        margin-top:8px;
        padding:10px 14px;
        font-size:13px;
    }

    .metric-card {
        border-radius:18px;
        padding:14px 14px;
        min-height:86px;
        margin-bottom:4px;
    }

    .metric-icon {
        width:38px;
        height:38px;
        font-size:19px;
    }

    .metric-inner {
        gap:11px;
    }

    .metric-label {
        font-size:11px;
    }

    .metric-value {
        font-size:22px;
    }

    .metric-sub-green,
    .metric-sub-red {
        font-size:11px;
    }

    .panel {
        padding:16px;
        border-radius:18px;
        margin-bottom:14px;
    }

    .panel-title {
        font-size:17px;
    }

    .progress-ring {
        width:200px;
        height:118px;
    }

    .progress-number {
        font-size:33px;
    }

    .holdings-header {
        display:block;
    }

    .pill-button,
    .add-button {
        display:none;
    }

    .right-card {
        padding:14px;
        border-radius:16px;
    }

    .summary-row {
        font-size:12px;
    }

    .total-row {
        display:block;
        font-size:12px;
        line-height:1.5;
    }

    div[data-testid="stDataFrame"] {
        font-size:11px;
    }

    section[data-testid="stSidebar"] {
        width: 82vw !important;
    }

    div[data-testid="collapsedControl"] {
        top: 0.6rem;
    }
}
</style>
""", unsafe_allow_html=True)

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
    ], columns=["Symbol","Icon","Name","Asset Type","Sector","Sub Sector","Units","Avg. Price","Current Price","Annual Dividend Per Unit","Franking %"])

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
    df["Status"] = np.where((df["Current Yield"] >= 5) & (df["Allocation"] < 20), "Accumulate", "Hold")
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

uploaded = st.sidebar.file_uploader("Upload holdings CSV", type=["csv"])
df = prepare(pd.read_csv(uploaded) if uploaded else sample_data())

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
  <div style="font-size:14px; font-weight:800; margin-bottom:10px;">Income Goal</div>
  <div style="font-size:19px; font-weight:900;">{money(target_income)} <span style="font-size:13px; font-weight:500;">/ year</span></div>
  <div style="height:10px; background:rgba(255,255,255,0.14); border-radius:999px; margin:14px 0 8px 0;">
    <div style="height:10px; width:{progress}%; background:linear-gradient(90deg,#22c55e,#2563eb); border-radius:999px;"></div>
  </div>
  <div style="font-size:12px; color:#cbd5e1;">{progress:.0f}% complete</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄 Refresh Data", use_container_width=True, type="primary"):
    st.cache_data.clear()

if page == "Dashboard":
    st.markdown(f"""
    <div class="header-row">
      <div>
        <div class="page-title">Dashboard Overview</div>
        <div class="page-subtitle">Your journey to {money(target_income)} per year in dividend income</div>
      </div>
      <div class="top-actions">
        Market closed<br>
        <span style="font-weight:500; color:#64748b;">as of 24 May 2025</span><br>
        <span class="refresh-pill">↻ Refresh Data</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="mobile-only">', unsafe_allow_html=True)
    cA, cB = st.columns(2)
    with cA:
        metric("$", "icon-green", "Portfolio Value", money(portfolio_value), "+1.35% (1D)")
    with cB:
        metric("◔", "icon-purple", "Annual Income", money(annual_income), f"{portfolio_yield:.1f}% yield")
    cC, cD = st.columns(2)
    with cC:
        metric("▣", "icon-blue", "Monthly Income", money(monthly_income), f"{money2(daily_income)} / day")
    with cD:
        metric("◎", "icon-orange", "Goal", money(target_income), f"{progress:.0f}% of goal")
    cE, cF = st.columns(2)
    with cE:
        metric("⌄", "icon-red", "Gap", money(income_gap), f"{money(income_gap/12)} / month", red=True)
    with cF:
        metric("↗", "icon-green", "Needed", f"${needed/1_000_000:.2f}M", f"{portfolio_yield:.1f}% yield")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="desktop-only">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    left, mid, right = st.columns([1.1, 1.55, 1.2])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Annual Dividend Income Progress</div>', unsafe_allow_html=True)
        angle = min(progress, 100) * 1.8
        st.markdown(f'<div class="progress-ring" style="--angle:{angle}deg;"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-number">{progress:.0f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center panel-sub">{money(annual_income)} of {money(target_income)} annual goal</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mid:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Income Forecast</div>', unsafe_allow_html=True)
        years = list(range(2025, 2037))
        rows = []
        for i, y in enumerate(years):
            rows.append({"Year": y, "Projected Income": annual_income * (1.135 ** i), "Current Trend": annual_income * (1.085 ** i), "Goal": target_income})
        st.line_chart(pd.DataFrame(rows).set_index("Year"))
        st.markdown("<div class='panel-sub'>Forecast is dummy data for design testing.</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Portfolio Allocation</div>', unsafe_allow_html=True)
        st.bar_chart(df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False))
        st.markdown("<div class='center green-text'>✓ Well diversified</div>", unsafe_allow_html=True)
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

        display = df[["Icon","Symbol","Name","Asset Type","Units","Avg. Price","Current Price","Market Value","Annual Income","Current Yield","Status"]].copy()
        display["Symbol"] = display["Icon"] + "  " + display["Symbol"]
        display = display.drop(columns=["Icon"])
        display["Avg. Price"] = display["Avg. Price"].map(money2)
        display["Current Price"] = display["Current Price"].map(money2)
        display["Market Value"] = display["Market Value"].map(money)
        display["Annual Income"] = display["Annual Income"].map(money)
        display["Current Yield"] = display["Current Yield"].map(lambda x: f"{x:.2f}%")
        st.dataframe(display, use_container_width=True, hide_index=True, height=360)
        st.markdown(f"""
        <div class="total-row">
          <div>Total / Weighted Average</div>
          <div>{money(portfolio_value)} &nbsp;&nbsp; {money(annual_income)} &nbsp;&nbsp; {portfolio_yield:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with lower_right:
        st.markdown('<div class="right-card">', unsafe_allow_html=True)
        st.markdown('<div class="right-title">Income Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-row"><span>Annual Income</span><span class="summary-value">{money(annual_income)}</span></div>
        <div class="summary-row"><span>Monthly Income</span><span class="summary-value">{money(monthly_income)}</span></div>
        <div class="summary-row"><span>Daily Income</span><span class="summary-value">{money2(daily_income)}</span></div>
        <div class="summary-row"><span>Franking Credits</span><span class="summary-value">{money(franking)}</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="right-card">', unsafe_allow_html=True)
        st.markdown('<div class="right-title">Top Contributors</div>', unsafe_allow_html=True)
        top = df.sort_values("Annual Income", ascending=False).head(3)
        for _, r in top.iterrows():
            pct_income = r["Annual Income"] / annual_income * 100 if annual_income else 0
            st.markdown(f"<div class='summary-row'><span><b>{r['Symbol']}</b></span><span class='summary-value'>{money(r['Annual Income'])} ({pct_income:.1f}%)</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(f"<div class='page-title'>{page}</div><div class='page-subtitle'>This page will be expanded in the next build.</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
