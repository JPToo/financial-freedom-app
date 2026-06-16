
import streamlit as st
import pandas as pd
from utils.styling import apply_global_style
from utils.calculations import money, money2, prepare_wealth_data

st.set_page_config(page_title="Wealth Builder", page_icon="📈", layout="wide")
apply_global_style()

st.markdown("""
<div class="hero">
    <div class="hero-title">Wealth Builder</div>
    <div class="hero-subtitle">For Mum & Dad: track shares, ETFs, dividend income and the path to financial freedom.</div>
</div>
""", unsafe_allow_html=True)

df = prepare_wealth_data(pd.read_csv("data/wealth_builder_sample.csv"))

target_income = st.sidebar.number_input("Annual income target", min_value=10000, max_value=500000, value=120000, step=5000)
annual_contribution = st.sidebar.number_input("Annual new investment", min_value=0, max_value=500000, value=30000, step=5000)
assumed_growth = st.sidebar.slider("Forecast annual growth %", 0.0, 12.0, 6.0, 0.5)

portfolio_value = df["Market Value"].sum()
annual_income = df["Annual Income"].sum()
monthly_income = annual_income / 12
portfolio_yield = annual_income / portfolio_value * 100 if portfolio_value else 0
income_gap = max(target_income - annual_income, 0)
required_portfolio = target_income / (portfolio_yield / 100) if portfolio_yield else 0
progress = min(annual_income / target_income * 100, 100)

c1, c2, c3, c4, c5 = st.columns(5)
for col, label, value, sub, red in [
    (c1, "Portfolio Value", money(portfolio_value), "dummy data", False),
    (c2, "Annual Income", money(annual_income), f"{portfolio_yield:.2f}% yield", False),
    (c3, "Monthly Income", money(monthly_income), "dividend equivalent", False),
    (c4, "Income Gap", money(income_gap), f"{100-progress:.0f}% remaining", True),
    (c5, "Portfolio Needed", money(required_portfolio), "at current yield", False),
]:
    with col:
        cls = "metric-sub-red" if red else "metric-sub-green"
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="{cls}">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.1, 1.7])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Progress to Income Goal</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{progress}%;"></div></div>', unsafe_allow_html=True)
    st.write(f"Current income: **{money(annual_income)}** of **{money(target_income)}** target.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    years = list(range(2026, 2046))
    value = portfolio_value
    rows = []
    for year in years:
        value = (value + annual_contribution) * (1 + assumed_growth / 100)
        income = value * portfolio_yield / 100
        rows.append({"Year": year, "Projected Portfolio": value, "Projected Income": income, "Income Target": target_income})
    forecast = pd.DataFrame(rows).set_index("Year")
    st.markdown("### Income Forecast")
    st.line_chart(forecast[["Projected Income", "Income Target"]], height=330)

st.markdown("### Holdings")
display = df[["Ticker", "Name", "Asset Type", "Sector", "Units", "Current Price", "Market Value", "Annual Income", "Current Yield %", "Allocation %"]].copy()
display["Current Price"] = display["Current Price"].map(money2)
display["Market Value"] = display["Market Value"].map(money)
display["Annual Income"] = display["Annual Income"].map(money)
display["Current Yield %"] = display["Current Yield %"].map(lambda x: f"{x:.2f}%")
display["Allocation %"] = display["Allocation %"].map(lambda x: f"{x:.1f}%")
st.dataframe(display, hide_index=True, use_container_width=True)

st.markdown("""
<div class="info-box">
<b>Automation potential:</b> current share/ETF prices can be automated daily using a market data source. Units owned and purchase history should remain manual or come from a broker/Sharesight export.
</div>
""", unsafe_allow_html=True)
