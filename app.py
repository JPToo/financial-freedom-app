
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Family Wealth Platform", page_icon="🏡", layout="wide")

st.markdown("""
<style>
.stApp {background:#f6f8fc;}
.block-container {padding-top:2rem; max-width:1600px;}
section[data-testid="stSidebar"] {background:#071327;}
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {color:#f8fafc !important;}
section[data-testid="stSidebar"] input {color:#111827 !important;}
.hero {background:white; border:1px solid #dbe4f0; border-radius:22px; padding:26px 30px; box-shadow:0 8px 22px rgba(15,23,42,.06); margin-bottom:22px;}
.hero-title {font-size:34px; font-weight:900; color:#0f172a;}
.hero-subtitle {font-size:15px; color:#475569;}
.metric-card {background:white; border:1px solid #dbe4f0; border-radius:18px; padding:18px; box-shadow:0 8px 22px rgba(15,23,42,.055); min-height:110px;}
.metric-label {color:#64748b; font-size:12px; font-weight:800;}
.metric-value {color:#0f172a; font-size:25px; font-weight:900;}
.metric-sub-green {color:#16a34a; font-size:12px; font-weight:900;}
.metric-sub-red {color:#dc2626; font-size:12px; font-weight:900;}
.panel {background:white; border:1px solid #dbe4f0; border-radius:18px; padding:20px; box-shadow:0 8px 22px rgba(15,23,42,.05); margin-bottom:18px;}
.panel-title {font-size:18px; font-weight:900; color:#0f172a;}
.home-card {background:white; border:1px solid #dbe4f0; border-radius:20px; padding:24px; min-height:210px; box-shadow:0 8px 22px rgba(15,23,42,.055);}
.home-icon {font-size:36px; margin-bottom:12px;}
.home-title {font-size:22px; font-weight:900; color:#0f172a;}
.home-text {font-size:14px; color:#475569; line-height:1.5;}
.info-box {background:white; border:1px solid #dbe4f0; border-left:5px solid #2563eb; border-radius:16px; padding:16px; margin:18px 0;}
.progress-bar {height:12px; background:#e5e7eb; border-radius:999px; overflow:hidden; margin:12px 0;}
.progress-fill {height:12px; background:linear-gradient(90deg,#22c55e,#2563eb);}
</style>
""", unsafe_allow_html=True)

def money(x): return f"${x:,.0f}"
def money2(x): return f"${x:,.2f}"

def metric(label, value, sub="", red=False):
    cls = "metric-sub-red" if red else "metric-sub-green"
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="{cls}">{sub}</div></div>', unsafe_allow_html=True)

def mortgage_payment(principal, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0: return principal / n
    return principal * (r * (1+r)**n) / ((1+r)**n - 1)

def fv_lump(pv, rate, years): return pv * ((1 + rate/100) ** years)
def fv_monthly(pmt, rate, years):
    r = rate/100/12
    n = years*12
    if r == 0: return pmt*n
    return pmt * (((1+r)**n - 1) / r)

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
    df["Allocation %"] = np.where(df["Market Value"].sum()>0, df["Market Value"]/df["Market Value"].sum()*100, 0)
    return df

st.sidebar.markdown("## ↗ Family Wealth")
st.sidebar.caption("Private Planning Platform")
page = st.sidebar.radio("Choose Dashboard", ["Home", "Wealth Builder", "Home Builder", "Future Builder"])

if page == "Home":
    st.markdown('<div class="hero"><div class="hero-title">Family Wealth Platform</div><div class="hero-subtitle">Three planning dashboards for different family life stages.</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="home-card"><div class="home-icon">📈</div><div class="home-title">Wealth Builder</div><div class="home-text">For Mum & Dad: shares, ETFs, dividends, income target and financial freedom planning.</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="home-card"><div class="home-icon">🏡</div><div class="home-title">Home Builder</div><div class="home-text">For a first-home buyer: deposit progress, purchase costs, mortgage estimate and cost-of-living readiness.</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="home-card"><div class="home-icon">🚗</div><div class="home-title">Future Builder</div><div class="home-text">For younger kids: car savings, investing early and long-term compounding to age 55.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><b>Privacy note:</b> this flat demo uses dummy data only. Real family data should stay local or be hosted privately later.</div>', unsafe_allow_html=True)

elif page == "Wealth Builder":
    st.markdown('<div class="hero"><div class="hero-title">Wealth Builder</div><div class="hero-subtitle">Track shares, ETFs, dividend income and financial freedom.</div></div>', unsafe_allow_html=True)
    df = wealth_data()
    target = st.sidebar.number_input("Annual income target", 10000, 500000, 120000, 5000)
    contribution = st.sidebar.number_input("Annual new investment", 0, 500000, 30000, 5000)
    growth = st.sidebar.slider("Forecast annual growth %", 0.0, 12.0, 6.0, 0.5)
    value = df["Market Value"].sum()
    income = df["Annual Income"].sum()
    yld = income/value*100
    gap = max(target-income, 0)
    needed = target/(yld/100)
    progress = min(income/target*100, 100)
    cols = st.columns(5)
    for col, vals in zip(cols, [("Portfolio Value", money(value), "dummy data", False), ("Annual Income", money(income), f"{yld:.2f}% yield", False), ("Monthly Income", money(income/12), "dividend equivalent", False), ("Income Gap", money(gap), f"{100-progress:.0f}% remaining", True), ("Portfolio Needed", money(needed), "at current yield", False)]):
        with col: metric(*vals)
    st.markdown("<br>", unsafe_allow_html=True)
    l, r = st.columns([1.1, 1.7])
    with l:
        st.markdown('<div class="panel"><div class="panel-title">Progress to Income Goal</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{progress}%;"></div></div>', unsafe_allow_html=True)
        st.write(f"Current income: **{money(income)}** of **{money(target)}** target.")
        st.markdown('</div>', unsafe_allow_html=True)
    with r:
        rows=[]; val=value
        for year in range(2026, 2046):
            val = (val+contribution)*(1+growth/100)
            rows.append({"Year":year, "Projected Income":val*yld/100, "Income Target":target})
        st.markdown("### Income Forecast")
        st.line_chart(pd.DataFrame(rows).set_index("Year"), height=330)
    st.markdown("### Holdings")
    d = df[["Ticker","Name","Asset Type","Sector","Units","Current Price","Market Value","Annual Income","Current Yield %","Allocation %"]].copy()
    for c in ["Current Price"]: d[c]=d[c].map(money2)
    for c in ["Market Value","Annual Income"]: d[c]=d[c].map(money)
    for c in ["Current Yield %","Allocation %"]: d[c]=d[c].map(lambda x:f"{x:.2f}%")
    st.dataframe(d, hide_index=True, use_container_width=True)

elif page == "Home Builder":
    st.markdown('<div class="hero"><div class="hero-title">Home Builder</div><div class="hero-subtitle">Deposit progress, purchase costs and life-after-purchase affordability.</div></div>', unsafe_allow_html=True)
    price = st.sidebar.number_input("Target property price", 100000, 2000000, 700000, 25000)
    savings = st.sidebar.number_input("Current savings", 0, 1000000, 45000, 5000)
    monthly = st.sidebar.number_input("Monthly savings", 0, 20000, 1800, 250)
    dep_pct = st.sidebar.slider("Deposit %", 5, 30, 20)
    income_monthly = st.sidebar.number_input("Monthly income after tax", 0, 50000, 6200, 250)
    rate = st.sidebar.slider("Mortgage interest rate %", 2.0, 10.0, 6.25, 0.25)
    years = st.sidebar.slider("Loan years", 15, 35, 30)
    costs = pd.DataFrame([["Council rates",220],["Water rates",90],["Electricity and gas",260],["Internet and phone",120],["Home insurance",160],["Groceries",700],["Fuel and transport",350],["Maintenance allowance",250],["Entertainment and lifestyle",500],["Emergency saving after purchase",300]], columns=["Category","Monthly Cost"])
    deposit = price*dep_pct/100
    total_required = deposit + price*0.045 + 7000 + 12000 + 20000
    progress = min(savings/total_required*100, 100)
    gap = max(total_required-savings, 0)
    months = gap/monthly if monthly else 999
    mort = mortgage_payment(price-deposit, rate, years)
    living = costs["Monthly Cost"].sum()
    surplus = income_monthly - mort - living
    cols=st.columns(5)
    for col, vals in zip(cols, [("Total Cash Required", money(total_required), "deposit + costs + buffer", False), ("Current Savings", money(savings), f"{progress:.0f}% ready", False), ("Savings Gap", money(gap), f"{months:.1f} months", True), ("Mortgage Estimate", money(mort), "per month", False), ("Post-Purchase Surplus", money(surplus), "per month", surplus<800)]):
        with col: metric(*vals)
    st.markdown("<br>", unsafe_allow_html=True)
    l, r = st.columns([1.1, 1.5])
    with l:
        st.markdown('<div class="panel"><div class="panel-title">Deposit & Purchase Readiness</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{progress}%;"></div></div>', unsafe_allow_html=True)
        st.write(f"Saved **{money(savings)}** of estimated **{money(total_required)}** required.")
        st.write(f"Estimated time to readiness: **{months:.1f} months**")
        if surplus > 1000: st.success("Comfortable after purchase based on dummy assumptions.")
        elif surplus > 300: st.warning("Possible, but tight. Review living costs and buffer.")
        else: st.error("High risk. More savings or lower property price may be required.")
        st.markdown('</div>', unsafe_allow_html=True)
    with r:
        rows=[]
        for yr in range(0,8):
            rows.append({"Year":yr, "Projected Savings":savings + monthly*12*yr, "Total Cash Required":total_required})
        st.markdown("### Savings Forecast")
        st.line_chart(pd.DataFrame(rows).set_index("Year"), height=330)
    st.markdown("### Post-Purchase Monthly Cost Estimate")
    st.dataframe(costs, hide_index=True, use_container_width=True)

elif page == "Future Builder":
    st.markdown('<div class="hero"><div class="hero-title">Future Builder</div><div class="hero-subtitle">Car savings, first investments and long-term compounding.</div></div>', unsafe_allow_html=True)
    age = st.sidebar.number_input("Current age", 5, 40, 15, 1)
    current = st.sidebar.number_input("Current savings/investment", 0, 500000, 10000, 1000)
    monthly = st.sidebar.number_input("Monthly contribution", 0, 10000, 150, 50)
    ret = st.sidebar.slider("Assumed annual return %", 0.0, 12.0, 7.0, 0.5)
    car = st.sidebar.number_input("Car savings goal", 1000, 200000, 25000, 1000)
    target_age = st.sidebar.number_input("Long-term forecast age", age+1, 80, 55, 1)
    def val_at(a):
        yrs=max(a-age,0)
        return fv_lump(current, ret, yrs)+fv_monthly(monthly, ret, yrs)
    years_to_car = max((car-current)/(monthly*12),0) if monthly else 999
    cols=st.columns(5)
    for col, vals in zip(cols, [("Current Balance", money(current), "starting point", False), ("Monthly Contribution", money(monthly), "habit builder", False), ("Car Goal", money(car), f"{years_to_car:.1f} years", False), ("Value at Age 30", money(val_at(30)), "investment path", False), (f"Value at Age {target_age}", money(val_at(target_age)), f"{ret:.1f}% return", False)]):
        with col: metric(*vals)
    st.markdown("<br>", unsafe_allow_html=True)
    rows=[]
    for a in range(age, target_age+1):
        invested = val_at(a)
        savings_only = current + monthly*12*(a-age)
        rows.append({"Age":a, "Invested Growth":invested, "Savings Only":savings_only, "Car Goal":car})
    forecast=pd.DataFrame(rows).set_index("Age")
    l,r=st.columns([1.8,1])
    with l:
        st.markdown("### Savings vs Investing Forecast")
        st.line_chart(forecast, height=360)
    with r:
        st.markdown('<div class="panel"><div class="panel-title">Milestones</div>', unsafe_allow_html=True)
        st.write(f"At age **18**: {money(val_at(18))}")
        st.write(f"At age **21**: {money(val_at(21))}")
        st.write(f"At age **30**: {money(val_at(30))}")
        st.write(f"At age **{target_age}**: {money(val_at(target_age))}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### Forecast Table")
    table=forecast.reset_index()
    for c in ["Invested Growth","Savings Only","Car Goal"]: table[c]=table[c].map(money)
    st.dataframe(table, hide_index=True, use_container_width=True)
