
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Family Wealth Platform", page_icon="🏡", layout="wide")

# ============================================================
# Styling
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {background:#f6f8fc;}

.block-container {
    padding-top:2rem;
    padding-left:1.7rem;
    padding-right:1.7rem;
    max-width:1700px;
}

section[data-testid="stSidebar"] {background:#071327;}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color:#f8fafc !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    color:#111827 !important;
}

.logo-title {font-size:22px; font-weight:900; color:white; margin-bottom:4px;}
.logo-sub {font-size:13px; color:#cbd5e1; margin-bottom:24px;}

.hero {
    background:white;
    border:1px solid #dbe4f0;
    border-radius:22px;
    padding:26px 30px;
    box-shadow:0 8px 22px rgba(15,23,42,.06);
    margin-bottom:22px;
}

.hero-title {font-size:34px; font-weight:900; color:#0f172a; letter-spacing:-0.6px;}
.hero-subtitle {font-size:15px; color:#475569; margin-top:6px;}

.metric-card {
    background:white;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:18px;
    box-shadow:0 8px 22px rgba(15,23,42,.055);
    min-height:112px;
}

.metric-label {color:#64748b; font-size:12px; font-weight:800; margin-bottom:6px;}
.metric-value {color:#0f172a; font-size:25px; font-weight:900; line-height:1.1;}
.metric-sub-green {color:#16a34a; font-size:12px; font-weight:900; margin-top:5px;}
.metric-sub-red {color:#dc2626; font-size:12px; font-weight:900; margin-top:5px;}
.metric-sub-blue {color:#2563eb; font-size:12px; font-weight:900; margin-top:5px;}

.panel {
    background:white;
    border:1px solid #dbe4f0;
    border-radius:18px;
    padding:20px;
    box-shadow:0 8px 22px rgba(15,23,42,.05);
    margin-bottom:18px;
}

.panel-title {font-size:18px; font-weight:900; color:#0f172a; margin-bottom:10px;}
.panel-sub {font-size:13px; color:#64748b; margin-bottom:10px;}

.home-card {
    background:white;
    border:1px solid #dbe4f0;
    border-radius:20px;
    padding:24px;
    min-height:230px;
    box-shadow:0 8px 22px rgba(15,23,42,.055);
}

.home-icon {font-size:36px; margin-bottom:12px;}
.home-title {font-size:22px; font-weight:900; color:#0f172a;}
.home-text {font-size:14px; color:#475569; line-height:1.5; margin-top:8px;}

.info-box {
    background:white;
    border:1px solid #dbe4f0;
    border-left:5px solid #2563eb;
    border-radius:16px;
    padding:16px;
    margin:18px 0;
}

.progress-bar {
    height:12px;
    background:#e5e7eb;
    border-radius:999px;
    overflow:hidden;
    margin:12px 0;
}

.progress-fill {
    height:12px;
    background:linear-gradient(90deg,#22c55e,#2563eb);
    border-radius:999px;
}

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

.center {text-align:center;}
.green-text {color:#16a34a; font-weight:900;}
.red-text {color:#dc2626; font-weight:900;}

div[data-testid="stDataFrame"] {
    border-radius:14px;
    overflow:hidden;
    border:1px solid #e2e8f0;
}

@media (max-width:768px) {
    .block-container {
        padding-left:0.8rem;
        padding-right:0.8rem;
        padding-top:1.2rem;
    }
    .hero-title {font-size:28px;}
    .metric-value {font-size:22px;}
    .home-card {min-height:180px;}
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Helpers
# ============================================================
def money(x):
    return f"${x:,.0f}"

def money2(x):
    return f"${x:,.2f}"

def metric(label, value, sub="", colour="green"):
    cls = {
        "green": "metric-sub-green",
        "red": "metric-sub-red",
        "blue": "metric-sub-blue",
    }.get(colour, "metric-sub-green")
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="{cls}">{sub}</div></div>',
        unsafe_allow_html=True,
    )

def mortgage_payment(principal, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1+r)**n) / ((1+r)**n - 1)

def fv_lump(pv, rate, years):
    return pv * ((1 + rate/100) ** years)

def fv_monthly(pmt, rate, years):
    r = rate/100/12
    n = years*12
    if r == 0:
        return pmt*n
    return pmt * (((1+r)**n - 1) / r)

def months_to_years_text(months):
    if months >= 900:
        return "Not possible"
    years = int(months // 12)
    rem = int(round(months % 12))
    if years == 0:
        return f"{rem} months"
    return f"{years} yrs {rem} mths"

# ============================================================
# Dummy data
# ============================================================
def wealth_data():
    df = pd.DataFrame([
        ["CBA.AX","Commonwealth Bank","Share","Financials",200,88.50,131.48,4.24,100],
        ["BHP.AX","BHP Group","Share","Resources",150,40.20,48.17,2.31,100],
        ["WDS.AX","Woodside Energy","Share","Energy",400,28.10,28.97,1.54,100],
        ["WES.AX","Wesfarmers","Share","Industrials",100,56.30,66.42,2.12,100],
        ["VAS.AX","Vanguard Australian Shares ETF","ETF","Australian ETF",500,88.60,95.21,4.72,75],
        ["VGS.AX","Vanguard International Shares ETF","ETF","International ETF",300,102.30,111.92,4.94,0],
        ["VHY.AX","Vanguard High Yield Australian Shares ETF","ETF","Dividend ETF",400,68.20,71.45,4.45,80],
        ["A200.AX","Betashares Australia 200 ETF","ETF","Australian ETF",250,118.00,132.60,5.20,75],
        ["IVV.AX","iShares S&P 500 ETF","ETF","International ETF",80,43.00,58.90,0.86,0],
        ["CASH","Cash Position","Cash","Cash",1,12000,12000,240,0],
    ], columns=["Ticker","Name","Asset Type","Sector","Units","Average Buy Price","Current Price","Annual Dividend Per Unit","Franking %"])
    df["Market Value"] = df["Units"] * df["Current Price"]
    df["Cost Base"] = df["Units"] * df["Average Buy Price"]
    df["Annual Income"] = df["Units"] * df["Annual Dividend Per Unit"]
    df["Current Yield %"] = np.where(df["Market Value"]>0, df["Annual Income"]/df["Market Value"]*100, 0)
    df["Yield on Cost %"] = np.where(df["Cost Base"]>0, df["Annual Income"]/df["Cost Base"]*100, 0)
    df["Franking Credits"] = df["Annual Income"] * (df["Franking %"] / 100) * (30 / 70)
    df["Allocation %"] = np.where(df["Market Value"].sum()>0, df["Market Value"]/df["Market Value"].sum()*100, 0)
    return df

def home_cost_data():
    return pd.DataFrame([
        ["Council rates",220],
        ["Water rates",90],
        ["Electricity and gas",260],
        ["Internet and phone",120],
        ["Home insurance",160],
        ["Groceries",700],
        ["Fuel and transport",350],
        ["Maintenance allowance",250],
        ["Entertainment and lifestyle",500],
        ["Emergency saving after purchase",300],
    ], columns=["Category","Monthly Cost"])

# ============================================================
# Session state and sidebar
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.markdown('<div class="logo-title">↗ Family Wealth</div><div class="logo-sub">Private Planning Platform</div>', unsafe_allow_html=True)

options = ["Home", "Wealth Builder", "Home Builder", "Future Builder"]
page = st.sidebar.radio(
    "Choose Dashboard",
    options,
    index=options.index(st.session_state.page),
    key="sidebar_page"
)
st.session_state.page = page

# ============================================================
# Home
# ============================================================
if page == "Home":
    st.markdown('<div class="hero"><div class="hero-title">Family Wealth Platform</div><div class="hero-subtitle">Three planning dashboards for different family life stages.</div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="home-card"><div class="home-icon">📈</div><div class="home-title">Wealth Builder</div><div class="home-text">For Mum & Dad: shares, ETFs, dividends, income target and financial freedom planning.</div></div>', unsafe_allow_html=True)
        if st.button("Open Wealth Builder", use_container_width=True):
            st.session_state.page = "Wealth Builder"
            st.rerun()

    with c2:
        st.markdown('<div class="home-card"><div class="home-icon">🏡</div><div class="home-title">Home Builder</div><div class="home-text">For a first-home buyer: deposit progress, purchase costs, mortgage estimate and cost-of-living readiness.</div></div>', unsafe_allow_html=True)
        if st.button("Open Home Builder", use_container_width=True):
            st.session_state.page = "Home Builder"
            st.rerun()

    with c3:
        st.markdown('<div class="home-card"><div class="home-icon">🚗</div><div class="home-title">Future Builder</div><div class="home-text">For younger kids: car savings, investing early and long-term compounding to age 55.</div></div>', unsafe_allow_html=True)
        if st.button("Open Future Builder", use_container_width=True):
            st.session_state.page = "Future Builder"
            st.rerun()

    st.markdown('<div class="info-box"><b>Privacy note:</b> this demo uses dummy data only. Real family data should stay local or be hosted privately later.</div>', unsafe_allow_html=True)

# ============================================================
# Wealth Builder - stronger V11 style
# ============================================================
elif page == "Wealth Builder":
    st.markdown('<div class="hero"><div class="hero-title">Wealth Builder</div><div class="hero-subtitle">For Mum & Dad: financial freedom through income-producing assets.</div></div>', unsafe_allow_html=True)

    df = wealth_data()
    target = st.sidebar.number_input("Annual income target", 10000, 500000, 120000, 5000)
    contribution = st.sidebar.number_input("Annual new investment", 0, 500000, 30000, 5000)
    growth = st.sidebar.slider("Forecast annual growth %", 0.0, 12.0, 6.0, 0.5)

    value = df["Market Value"].sum()
    income = df["Annual Income"].sum()
    yld = income/value*100
    monthly_income = income/12
    daily_income = income/365
    gap = max(target-income, 0)
    needed = target/(yld/100)
    progress = min(income/target*100, 100)
    franking = df["Franking Credits"].sum()

    cols = st.columns(6)
    with cols[0]: metric("Portfolio Value", money(value), "dummy data")
    with cols[1]: metric("Annual Dividend Income", money(income), f"{yld:.2f}% yield")
    with cols[2]: metric("Monthly Income", money(monthly_income), f"{money2(daily_income)} / day")
    with cols[3]: metric("Income Goal", money(target), f"{progress:.0f}% of goal")
    with cols[4]: metric("Income Gap", money(gap), f"{money(gap/12)} / month", "red")
    with cols[5]: metric("Portfolio Needed", money(needed), f"at {yld:.2f}% yield")

    st.markdown("<br>", unsafe_allow_html=True)

    left, mid, right = st.columns([1.1, 1.6, 1.2])

    with left:
        angle = min(progress, 100) * 1.8
        st.markdown('<div class="panel"><div class="panel-title">Annual Dividend Income Progress</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-ring" style="--angle:{angle}deg;"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-number">{progress:.0f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center">{money(income)} of {money(target)} annual goal</div>', unsafe_allow_html=True)
        years_to_goal = gap / max(contribution * yld / 100, 1)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<div class="center">Indicative years to goal<br><span class="green-text" style="font-size:24px;">{years_to_goal:.1f} years</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with mid:
        rows=[]; val=value
        for year in range(2026, 2041):
            val = (val+contribution)*(1+growth/100)
            rows.append({"Year":year, "Projected Income":val*yld/100, "Income Target":target, "Current Trend": income*((1+growth/100)**(year-2026))})
        st.markdown("### Income Forecast")
        st.line_chart(pd.DataFrame(rows).set_index("Year"), height=330)
        st.caption("Dummy forecast only. Later this can use real holdings, live prices and assumptions.")

    with right:
        st.markdown("### Portfolio Allocation")
        st.bar_chart(df.groupby("Sector")["Market Value"].sum().sort_values(ascending=False), height=330)
        st.markdown('<div class="center green-text">✓ Diversification check</div>', unsafe_allow_html=True)

    st.markdown("### Holdings Overview")
    display = df[["Ticker","Name","Units","Average Buy Price","Current Price","Market Value","Annual Income","Yield on Cost %","Current Yield %","Allocation %"]].copy()
    display["Average Buy Price"] = display["Average Buy Price"].map(money2)
    display["Current Price"] = display["Current Price"].map(money2)
    display["Market Value"] = display["Market Value"].map(money)
    display["Annual Income"] = display["Annual Income"].map(money)
    for c in ["Yield on Cost %","Current Yield %","Allocation %"]:
        display[c] = display[c].map(lambda x:f"{x:.2f}%")
    st.dataframe(display, hide_index=True, use_container_width=True, height=340)

    a,b,c,d = st.columns(4)
    with a: metric("Franking Credits", money(franking), "estimate")
    with b: metric("Top Income Source", df.sort_values("Annual Income", ascending=False).iloc[0]["Ticker"], "by annual income", "blue")
    with c: metric("Largest Holding", df.sort_values("Market Value", ascending=False).iloc[0]["Ticker"], "by market value", "blue")
    with d: metric("Holdings Count", str(len(df)), "dummy portfolio", "blue")

# ============================================================
# Home Builder - cleaner forecast focus
# ============================================================
elif page == "Home Builder":
    st.markdown('<div class="hero"><div class="hero-title">Home Builder</div><div class="hero-subtitle">Deposit progress, purchase costs and life-after-purchase affordability.</div></div>', unsafe_allow_html=True)

    st.sidebar.markdown("### Home Purchase Assumptions")
    price = st.sidebar.number_input("Target property price", 100000, 2000000, 700000, 25000)
    savings = st.sidebar.number_input("Current savings", 0, 1000000, 45000, 5000)
    monthly = st.sidebar.number_input("Monthly savings", 0, 20000, 1800, 250)
    dep_pct = st.sidebar.slider("Deposit %", 5, 30, 20)
    include_purchase_costs = st.sidebar.checkbox("Include purchase costs and buffer", True)
    income_monthly = st.sidebar.number_input("Monthly income after tax", 0, 50000, 6200, 250)
    rate = st.sidebar.slider("Mortgage interest rate %", 2.0, 10.0, 6.25, 0.25)
    years = st.sidebar.slider("Loan years", 15, 35, 30)

    costs = home_cost_data()

    deposit_target = price*dep_pct/100
    purchase_costs = price*0.045 + 7000 + 12000 + 20000 if include_purchase_costs else 0
    savings_target = deposit_target + purchase_costs
    progress = min(savings/savings_target*100, 100) if savings_target else 0
    gap = max(savings_target-savings, 0)
    months = gap/monthly if monthly else 999
    years_to_ready = months/12 if months < 900 else 999

    loan_amount = price - deposit_target
    mort = mortgage_payment(loan_amount, rate, years)
    living = costs["Monthly Cost"].sum()
    surplus = income_monthly - mort - living

    cols=st.columns(5)
    with cols[0]: metric("Savings Target", money(savings_target), "deposit + selected costs")
    with cols[1]: metric("Current Savings", money(savings), f"{progress:.0f}% ready")
    with cols[2]: metric("Savings Gap", money(gap), months_to_years_text(months), "red")
    with cols[3]: metric("Mortgage Estimate", money(mort), "per month")
    with cols[4]: metric("Post-Purchase Surplus", money(surplus), "per month", "red" if surplus < 800 else "green")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1.7])
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Readiness Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{progress}%;"></div></div>', unsafe_allow_html=True)
        st.write(f"Saved **{money(savings)}** of target **{money(savings_target)}**.")
        st.write(f"Estimated time to ready: **{months_to_years_text(months)}**.")
        st.write(f"Chart x-axis = **years from today**.")
        if surplus > 1000:
            st.success("Comfortable after purchase based on dummy assumptions.")
        elif surplus > 300:
            st.warning("Possible, but tight. Review costs and buffer.")
        else:
            st.error("High risk. More savings, lower property price or higher income may be required.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        rows=[]
        max_years = max(8, int(np.ceil(years_to_ready))+2 if years_to_ready < 900 else 8)
        for yr in range(0, min(max_years, 25)+1):
            projected = savings + monthly*12*yr
            rows.append({"Years From Today":yr, "Projected Savings":projected, "Savings Target":savings_target, "Deposit Only Target":deposit_target})
        chart_df = pd.DataFrame(rows).set_index("Years From Today")
        st.markdown("### Savings Forecast")
        st.line_chart(chart_df, height=360)
        st.caption("The x-axis shows years from today. The target line is the savings required based on your inputs.")

    st.markdown("### Post-Purchase Monthly Cost Estimate")
    st.dataframe(costs, hide_index=True, use_container_width=True)

# ============================================================
# Future Builder - car goal and investing separated
# ============================================================
elif page == "Future Builder":
    st.markdown('<div class="hero"><div class="hero-title">Future Builder</div><div class="hero-subtitle">Car savings, first investments and long-term compounding.</div></div>', unsafe_allow_html=True)

    mode = st.sidebar.radio("Future Builder Mode", ["Car Goal + Investing", "Long-Term Investing Only"])
    show_car_goal = mode == "Car Goal + Investing"

    st.sidebar.markdown("### Inputs")
    age = st.sidebar.number_input("Current age", 5, 40, 15, 1)
    current_investment = st.sidebar.number_input("Current investment balance", 0, 500000, 10000, 1000)
    monthly_investment = st.sidebar.number_input("Monthly investment contribution", 0, 10000, 150, 50)
    ret = st.sidebar.slider("Assumed annual investment return %", 0.0, 12.0, 7.0, 0.5)
    target_age = st.sidebar.number_input("Long-term forecast age", age+1, 80, 55, 1)

    if show_car_goal:
        st.sidebar.markdown("### Car Goal")
        car_goal = st.sidebar.number_input("Car goal amount", 1000, 200000, 25000, 1000)
        car_savings = st.sidebar.number_input("Current car savings", 0, 200000, 8000, 500)
        monthly_car_saving = st.sidebar.number_input("Monthly car saving", 0, 10000, 250, 50)
        car_gap = max(car_goal-car_savings, 0)
        car_months = car_gap/monthly_car_saving if monthly_car_saving else 999
    else:
        car_goal = 0
        car_savings = 0
        monthly_car_saving = 0
        car_gap = 0
        car_months = 0

    def val_at(a):
        yrs=max(a-age,0)
        return fv_lump(current_investment, ret, yrs)+fv_monthly(monthly_investment, ret, yrs)

    value_30 = val_at(30)
    value_target = val_at(target_age)

    if show_car_goal:
        cols=st.columns(5)
        with cols[0]: metric("Car Goal", money(car_goal), "target amount")
        with cols[1]: metric("Car Savings", money(car_savings), f"{min(car_savings/car_goal*100,100):.0f}% saved")
        with cols[2]: metric("Car Gap", money(car_gap), months_to_years_text(car_months), "red")
        with cols[3]: metric("Investment at Age 30", money(value_30), "separate from car goal")
        with cols[4]: metric(f"Investment at Age {target_age}", money(value_target), f"{ret:.1f}% return")
    else:
        cols=st.columns(4)
        with cols[0]: metric("Current Investment", money(current_investment), "starting balance")
        with cols[1]: metric("Monthly Investment", money(monthly_investment), "habit builder")
        with cols[2]: metric("Investment at Age 30", money(value_30), "forecast")
        with cols[3]: metric(f"Investment at Age {target_age}", money(value_target), f"{ret:.1f}% return")

    st.markdown("<br>", unsafe_allow_html=True)

    if show_car_goal:
        left, right = st.columns([1.1, 1.7])
        with left:
            car_progress = min(car_savings/car_goal*100,100) if car_goal else 0
            st.markdown('<div class="panel"><div class="panel-title">Car Goal Progress</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{car_progress}%;"></div></div>', unsafe_allow_html=True)
            st.write(f"Saved **{money(car_savings)}** of **{money(car_goal)}**.")
            st.write(f"Estimated time to car goal: **{months_to_years_text(car_months)}**.")
            st.write("Once the car is purchased, switch to **Long-Term Investing Only** mode.")
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            max_car_years = max(5, int(np.ceil(car_months/12))+1 if car_months < 900 else 5)
            rows=[]
            for yr in range(0, min(max_car_years, 15)+1):
                rows.append({"Years From Today":yr, "Projected Car Savings":car_savings + monthly_car_saving*12*yr, "Car Goal":car_goal})
            st.markdown("### Car Savings Forecast")
            st.line_chart(pd.DataFrame(rows).set_index("Years From Today"), height=330)
            st.caption("This chart is only for the car goal. Turn it off once the goal is achieved.")

    rows=[]
    for a in range(age, target_age+1):
        yrs = a-age
        invested = val_at(a)
        cash_only = current_investment + monthly_investment*12*yrs
        rows.append({"Age":a, "Investment Growth Path":invested, "Cash Savings Only":cash_only})
    forecast=pd.DataFrame(rows).set_index("Age")

    left, right = st.columns([1.8,1])
    with left:
        st.markdown("### Long-Term Investing Forecast")
        st.line_chart(forecast, height=360)
        st.caption("Cash Savings Only means no investment growth. Investment Growth Path applies the assumed annual return.")
    with right:
        st.markdown('<div class="panel"><div class="panel-title">Investment Milestones</div>', unsafe_allow_html=True)
        st.write(f"At age **18**: {money(val_at(18))}")
        st.write(f"At age **21**: {money(val_at(21))}")
        st.write(f"At age **30**: {money(val_at(30))}")
        st.write(f"At age **{target_age}**: {money(val_at(target_age))}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Forecast Table")
    table=forecast.reset_index()
    for c in ["Investment Growth Path","Cash Savings Only"]:
        table[c]=table[c].map(money)
    st.dataframe(table, hide_index=True, use_container_width=True)
