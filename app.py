
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f6f8fc; }

.block-container {
    padding-top: 3.2rem;
    padding-left: 1.7rem;
    padding-right: 1.7rem;
    max-width: 1720px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071327 0%, #0b1a33 100%);
}

section[data-testid="stSidebar"] * { color: #f8fafc !important; }

.logo-box {
    display:flex;
    gap:12px;
    align-items:center;
    margin-bottom:22px;
}

.logo-icon {
    width:40px;
    height:40px;
    border-radius:13px;
    background:linear-gradient(135deg,#2563eb,#22c55e);
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:900;
    font-size:22px;
    color:white;
}

.logo-title { font-size:22px; font-weight:900; line-height:1; }
.logo-sub { font-size:13px; color:#cbd5e1 !important; margin-top:3px; }

.side-card {
    background:rgba(255,255,255,0.07);
    border:1px solid rgba(148,163,184,0.25);
    border-radius:16px;
    padding:15px;
    margin:16px 0;
}

.header {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:20px;
}

.title {
    font-size:34px;
    font-weight:900;
    color:#0f172a;
    letter-spacing:-0.6px;
    line-height:1.2;
    margin-top:8px;
    margin-bottom:4px;
}

.subtitle { font-size:15px; color:#475569; }

.top-right {
    text-align:right;
    font-size:13px;
    color:#0f172a;
    font-weight:800;
}

.refresh {
    display:inline-block;
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
    color:white;
    padding:12px 18px;
    border-radius:12px;
    font-weight:900;
    margin-left:12px;
    box-shadow:0 8px 18px rgba(37,99,235,0.25);
}

.card {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:18px;
    box-shadow:0 8px 22px rgba(15,23,42,0.055);
}

.kpi { min-height:112px; }
.kpi-inner { display:flex; align-items:center; gap:14px; }

.kpi-icon {
    width:44px;
    height:44px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
    flex-shrink:0;
}

.green-bg { background:#dcfce7; color:#16a34a; }
.purple-bg { background:#ede9fe; color:#7c3aed; }
.blue-bg { background:#dbeafe; color:#2563eb; }
.orange-bg { background:#ffedd5; color:#f97316; }
.red-bg { background:#fee2e2; color:#ef4444; }

.kpi-label { color:#64748b; font-size:12px; font-weight:800; margin-bottom:4px; }
.kpi-value { color:#0f172a; font-size:23px; font-weight:900; line-height:1.1; }
.kpi-sub-green { color:#16a34a; font-size:12px; font-weight:900; margin-top:5px; }
.kpi-sub-red { color:#dc2626; font-size:12px; font-weight:900; margin-top:5px; }

.panel {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:22px;
    box-shadow:0 8px 22px rgba(15,23,42,0.05);
    margin-bottom:18px;
}

.panel-title { color:#0f172a; font-size:18px; font-weight:900; margin-bottom:14px; }
.panel-sub { color:#64748b; font-size:13px; }

.progress-ring {
    width:230px;
    height:135px;
    border-radius:230px 230px 0 0;
    background:
      radial-gradient(circle at 50% 100%, white 0 52%, transparent 53%),
      conic-gradient(from 270deg, #22c55e 0deg, #22c55e var(--angle), #e5e7eb var(--angle), #e5e7eb 180deg, transparent 180deg);
    margin:16px auto 2px auto;
}

.progress-number {
    text-align:center;
    color:#16a34a;
    font-size:38px;
    font-weight:900;
    margin-top:-18px;
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

.right-title { color:#0f172a; font-size:16px; font-weight:900; margin-bottom:12px; }

.summary-row {
    display:flex;
    justify-content:space-between;
    gap:10px;
    font-size:13px;
    margin-bottom:9px;
    color:#1e293b;
}

.summary-value { font-weight:900; }

.holdings-header {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:12px;
    margin-bottom:12px;
}

.total-row {
    background:#f8fafc;
    border:1px solid #e2e8f0;
    border-radius:12px;
    padding:14px 16px;
    display:flex;
    justify-content:space-between;
    color:#0f172a;
    font-weight:900;
    margin-top:10px;
}

.insight-strip {
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    gap:12px;
    margin:12px 0 14px 0;
}

.insight {
    background:#f8fafc;
    border:1px solid #e2e8f0;
    border-radius:14px;
    padding:12px 14px;
}

.insight-label {
    color:#64748b;
    font-size:12px;
    font-weight:800;
    margin-bottom:4px;
}

.insight-value {
    color:#0f172a;
    font-size:18px;
    font-weight:900;
}

div[data-testid="stDataFrame"] {
    border-radius:14px;
    overflow:hidden;
    border:1px solid #e2e8f0;
}

.iphone-wrap { max-width: 430px; margin: 0 auto; }
.iphone-title { font-size: 28px; font-weight: 900; color: #0f172a; line-height:1.05; margin-bottom:8px; }
.iphone-sub { color:#475569; font-size:14px; line-height:1.35; margin-bottom:14px; }

.iphone-card {
    background:#ffffff;
    border:1px solid #dbe4f0;
    border-radius:20px;
    padding:16px;
    box-shadow:0 8px 22px rgba(15,23,42,0.055);
    margin-bottom:12px;
}

.iphone-kpi { display:flex; align-items:center; gap:13px; }

.iphone-icon {
    width:42px;
    height:42px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:21px;
    flex-shrink:0;
}

.iphone-label { color:#64748b; font-size:12px; font-weight:800; margin-bottom:3px; }
.iphone-value { color:#0f172a; font-size:25px; font-weight:900; line-height:1.1; }
.iphone-subtext-green { color:#16a34a; font-size:12px; font-weight:900; margin-top:4px; }
.iphone-subtext-red { color:#dc2626; font-size:12px; font-weight:900; margin-top:4px; }

.iphone-progress { height:10px; background:#e5e7eb; border-radius:999px; margin:12px 0 8px 0; }
.iphone-progress-fill { height:10px; background:linear-gradient(90deg,#22c55e,#2563eb); border-radius:999px; }

.iphone-holding {
    display:flex;
    justify-content:space-between;
    gap:12px;
    padding:12px 0;
    border-bottom:1px solid #e2e8f0;
}

.iphone-holding:last-child { border-bottom:none; }
.iphone-symbol { font-weight:900; color:#0f172a; }
.iphone-small { color:#64748b; font-size:12px; }

@media (max-width: 768px) {
    .block-container {
        padding-left:0.7rem;
        padding-right:0.7rem;
        padding-top:1.2rem;
    }
    .title { font-size:28px; }
    .insight-strip { grid-template-columns: repeat(2, 1fr); }
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

def kpi(icon, bg, label, value, sub, red=False):
    sub_class = "kpi-sub-red" if red else "kpi-sub-green"
    st.markdown(f"""
    <div class="card kpi">
      <div class="kpi-inner">
        <div class="kpi-icon {bg}">{icon}</div>
        <div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="{sub_class}">{sub}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def iphone_kpi(icon, bg, label, value, sub, red=False):
    sub_class = "iphone-subtext-red" if red else "iphone-subtext-green"
    st.markdown(f"""
    <div class="iphone-card">
      <div class="iphone-kpi">
        <div class="iphone-icon {bg}">{icon}</div>
        <div>
          <div class="iphone-label">{label}</div>
          <div class="iphone-value">{value}</div>
          <div class="{sub_class}">{sub}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="logo-box">
  <div class="logo-icon">↗</div>
  <div>
    <div class="logo-title">Wealth Builder</div>
    <div class="logo-sub">Dividend Freedom</div>
  </div>
</div>
""", unsafe_allow_html=True)

display_mode = st.sidebar.radio("Display Mode", ["Desktop Dashboard", "iPhone Dashboard"], index=0)
page = st.sidebar.radio("Navigation", ["Dashboard", "Holdings", "Income Forecast", "What to Buy Next", "Upload Data"], index=0)

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
<div class="side-card">
  <div style="font-size:14px; font-weight:900; margin-bottom:10px;">Income Goal</div>
  <div style="font-size:19px; font-weight:900;">{money(target_income)} <span style="font-size:13px; font-weight:500;">/ year</span></div>
  <div style="height:10px; background:rgba(255,255,255,0.14); border-radius:999px; margin:14px 0 8px 0;">
    <div style="height:10px; width:{progress}%; background:linear-gradient(90deg,#22c55e,#2563eb); border-radius:999px;"></div>
  </div>
  <div style="font-size:12px; color:#cbd5e1;">{progress:.0f}% complete</div>
</div>
""", unsafe_allow_html=True)

# iPhone
if display_mode == "iPhone Dashboard":
    st.markdown('<div class="iphone-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="iphone-title">Wealth Builder</div>
    <div class="iphone-sub">Dividend Freedom<br>Journey to {money(target_income)} per year</div>
    """, unsafe_allow_html=True)

    iphone_kpi("$", "green-bg", "Portfolio Value", money(portfolio_value), "+1.35% (1D)")
    iphone_kpi("◔", "purple-bg", "Annual Dividend Income", money(annual_income), f"{portfolio_yield:.1f}% yield")
    iphone_kpi("▣", "blue-bg", "Monthly Income", money(monthly_income), f"{money2(daily_income)} / day")
    iphone_kpi("◎", "orange-bg", "Income Goal", f"{money(target_income)} / year", f"{progress:.0f}% of goal")
    iphone_kpi("⌄", "red-bg", "Income Gap", f"{money(income_gap)} / year", f"{money(income_gap/12)} / month", red=True)
    iphone_kpi("↗", "green-bg", "Portfolio Needed", f"${needed/1_000_000:.2f}M", f"at {portfolio_yield:.1f}% yield")

    st.markdown(f"""
    <div class="iphone-card">
      <div class="right-title">Progress to Goal</div>
      <div class="iphone-progress"><div class="iphone-progress-fill" style="width:{progress}%;"></div></div>
      <div class="iphone-small">{money(annual_income)} of {money(target_income)} annual goal</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="iphone-card">', unsafe_allow_html=True)
    st.markdown('<div class="right-title">Top Income Contributors</div>', unsafe_allow_html=True)
    top = df.sort_values("Annual Income", ascending=False).head(5)
    for _, r in top.iterrows():
        st.markdown(f"""
        <div class="iphone-holding">
          <div>
            <div class="iphone-symbol">{r['Icon']} {r['Symbol']}</div>
            <div class="iphone-small">{r['Name']}</div>
          </div>
          <div style="text-align:right;">
            <div class="iphone-symbol">{money(r['Annual Income'])}</div>
            <div class="iphone-small">{r['Current Yield']:.1f}% yield</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Desktop
else:
    if page == "Dashboard":
        st.markdown(f"""
        <div class="header">
          <div>
            <div class="title">Dashboard Overview</div>
            <div class="subtitle">Your journey to {money(target_income)} per year in dividend income</div>
          </div>
          <div class="top-right">
            Market closed<br>
            <span style="font-weight:500; color:#64748b;">as of 24 May 2025</span>
            <span class="refresh">↻ Refresh Data</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(6)
        with cols[0]: kpi("$", "green-bg", "Portfolio Value", money(portfolio_value), "+1.35% (1D)")
        with cols[1]: kpi("◔", "purple-bg", "Annual Dividend Income", money(annual_income), "+3.12% (1M)")
        with cols[2]: kpi("▣", "blue-bg", "Monthly Income", money(monthly_income), "+3.12% (1M)")
        with cols[3]: kpi("◎", "orange-bg", "Income Goal", f"{money(target_income)} <span style='font-size:14px;'>/ year</span>", f"{progress:.0f}% of goal")
        with cols[4]: kpi("⌄", "red-bg", "Income Gap", f"{money(income_gap)} <span style='font-size:14px;'>/ year</span>", f"{money(income_gap/12)} / month", red=True)
        with cols[5]: kpi("↗", "green-bg", "Est. Portfolio Needed", f"${needed/1_000_000:.2f}M", f"at {portfolio_yield:.1f}% yield")

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
                rows.append({"Year": y, "Projected Income": annual_income * (1.135 ** i), "Current Trend": annual_income * (1.085 ** i), "Goal": target_income})
            st.line_chart(pd.DataFrame(rows).set_index("Year"))
            st.markdown("<div class='panel-sub'>Assumes average annual investment of $18,000 and current average yield</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Portfolio Allocation</div>', unsafe_allow_html=True)
            st.bar_chart(df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False))
            st.markdown("<div class='center green-text'>✓ Well diversified</div><div class='center panel-sub'>Good balance across asset classes</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        lower_left, lower_right = st.columns([3.2, 0.9])
        with lower_left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)

            asset_options = ["All Assets"] + sorted(df["Asset Type"].dropna().unique().tolist())
            sector_options = ["All Sectors"] + sorted(df["Sector"].dropna().unique().tolist())

            st.markdown('<div class="holdings-header"><div><div class="panel-title" style="margin-bottom:2px;">Holdings Overview</div><div class="panel-sub">Filter the table to see income, yield and exposure by asset class or sector</div></div></div>', unsafe_allow_html=True)

            f1, f2, f3, f4 = st.columns([1, 1, 1.5, 0.9])
            selected_asset = f1.selectbox("Asset filter", asset_options, label_visibility="collapsed")
            selected_sector = f2.selectbox("Sector filter", sector_options, label_visibility="collapsed")
            search_text = f3.text_input("Search holdings", placeholder="🔍 Search holdings...", label_visibility="collapsed")
            f4.button("+ Add Holding", use_container_width=True, type="primary")

            filtered_df = df.copy()
            if selected_asset != "All Assets":
                filtered_df = filtered_df[filtered_df["Asset Type"] == selected_asset]
            if selected_sector != "All Sectors":
                filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
            if search_text:
                mask = (
                    filtered_df["Symbol"].str.contains(search_text, case=False, na=False)
                    | filtered_df["Name"].str.contains(search_text, case=False, na=False)
                    | filtered_df["Sector"].str.contains(search_text, case=False, na=False)
                )
                filtered_df = filtered_df[mask]

            filtered_value = filtered_df["Market Value"].sum()
            filtered_income = filtered_df["Annual Income"].sum()
            filtered_yield = filtered_income / filtered_value * 100 if filtered_value else 0
            filtered_franking = filtered_df["Franking Credits"].sum()

            st.markdown(f"""
            <div class="insight-strip">
              <div class="insight"><div class="insight-label">Filtered Value</div><div class="insight-value">{money(filtered_value)}</div></div>
              <div class="insight"><div class="insight-label">Filtered Income</div><div class="insight-value">{money(filtered_income)}</div></div>
              <div class="insight"><div class="insight-label">Filtered Yield</div><div class="insight-value">{filtered_yield:.2f}%</div></div>
              <div class="insight"><div class="insight-label">Franking Estimate</div><div class="insight-value">{money(filtered_franking)}</div></div>
            </div>
            """, unsafe_allow_html=True)

            display = filtered_df[["Icon","Symbol","Name","Units","Avg. Price","Current Price","Market Value","Annual Income","Yield on Cost","Current Yield"]].copy()
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
              <div>{int(filtered_df['Units'].sum()):,} units &nbsp;&nbsp;&nbsp; {money(filtered_value)} &nbsp;&nbsp;&nbsp; {money(filtered_income)} &nbsp;&nbsp;&nbsp; {filtered_yield:.2f}%</div>
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
            st.markdown('<div class="right-title">Top Income Contributors</div>', unsafe_allow_html=True)
            top = df.sort_values("Annual Income", ascending=False).head(3)
            for _, r in top.iterrows():
                pct_income = r["Annual Income"] / annual_income * 100 if annual_income else 0
                st.markdown(f"<div class='summary-row'><span><b>{r['Symbol']}</b></span><span class='summary-value'>{money(r['Annual Income'])} ({pct_income:.1f}%)</span></div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown(f"<div class='title'>{page}</div><div class='subtitle'>This page will be expanded in the next build.</div>", unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
