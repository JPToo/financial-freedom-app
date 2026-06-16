
import streamlit as st
import pandas as pd
from utils.styling import apply_global_style
from utils.calculations import money, future_value_lump_sum, future_value_monthly_contribution

st.set_page_config(page_title="Future Builder", page_icon="🚗", layout="wide")
apply_global_style()

st.markdown("""
<div class="hero">
    <div class="hero-title">Future Builder</div>
    <div class="hero-subtitle">For younger kids: car savings, first investments and the long-term power of compounding.</div>
</div>
""", unsafe_allow_html=True)

profile = pd.read_csv("data/future_builder_sample.csv").iloc[0]

st.sidebar.markdown("### Future Builder Assumptions")
current_age = st.sidebar.number_input("Current age", min_value=5, max_value=40, value=int(profile["Current Age"]), step=1)
current_investment = st.sidebar.number_input("Current savings/investment", min_value=0, max_value=500000, value=int(profile["Current Investment"]), step=1000)
monthly_contribution = st.sidebar.number_input("Monthly contribution", min_value=0, max_value=10000, value=int(profile["Monthly Contribution"]), step=50)
annual_return = st.sidebar.slider("Assumed annual return %", 0.0, 12.0, float(profile["Assumed Annual Return %"]), 0.5)
car_goal = st.sidebar.number_input("Car savings goal", min_value=1000, max_value=200000, value=int(profile["Car Goal"]), step=1000)
forecast_age = st.sidebar.number_input("Long-term forecast age", min_value=current_age+1, max_value=80, value=55, step=1)

years_to_car = max((car_goal - current_investment) / (monthly_contribution * 12), 0) if monthly_contribution else 999
value_at_18 = future_value_lump_sum(current_investment, annual_return, max(18-current_age, 0)) + future_value_monthly_contribution(monthly_contribution, annual_return, max(18-current_age, 0))
value_at_21 = future_value_lump_sum(current_investment, annual_return, max(21-current_age, 0)) + future_value_monthly_contribution(monthly_contribution, annual_return, max(21-current_age, 0))
value_at_30 = future_value_lump_sum(current_investment, annual_return, max(30-current_age, 0)) + future_value_monthly_contribution(monthly_contribution, annual_return, max(30-current_age, 0))
value_at_target = future_value_lump_sum(current_investment, annual_return, forecast_age-current_age) + future_value_monthly_contribution(monthly_contribution, annual_return, forecast_age-current_age)

cols = st.columns(5)
metrics = [
    ("Current Balance", money(current_investment), "starting point"),
    ("Monthly Contribution", money(monthly_contribution), "habit builder"),
    ("Car Goal", money(car_goal), f"{years_to_car:.1f} years"),
    ("Value at Age 30", money(value_at_30), "investment path"),
    (f"Value at Age {forecast_age}", money(value_at_target), f"{annual_return:.1f}% return"),
]
for col, (label, value, sub) in zip(cols, metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-sub-green">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

years = list(range(current_age, forecast_age + 1))
rows = []
for age in years:
    years_elapsed = age - current_age
    investment_value = future_value_lump_sum(current_investment, annual_return, years_elapsed) + future_value_monthly_contribution(monthly_contribution, annual_return, years_elapsed)
    savings_only = current_investment + monthly_contribution * 12 * years_elapsed
    rows.append({"Age": age, "Invested Growth": investment_value, "Savings Only": savings_only, "Car Goal": car_goal})
forecast = pd.DataFrame(rows).set_index("Age")

left, right = st.columns([1.8, 1])

with left:
    st.markdown("### Savings vs Investing Forecast")
    st.line_chart(forecast, height=360)

with right:
    st.markdown('<div class="panel"><div class="panel-title">Milestones</div>', unsafe_allow_html=True)
    st.write(f"At age **18**: {money(value_at_18)}")
    st.write(f"At age **21**: {money(value_at_21)}")
    st.write(f"At age **30**: {money(value_at_30)}")
    st.write(f"At age **{forecast_age}**: {money(value_at_target)}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Forecast Table")
table = forecast.reset_index()
for col in ["Invested Growth", "Savings Only", "Car Goal"]:
    table[col] = table[col].map(money)
st.dataframe(table, hide_index=True, use_container_width=True)

st.markdown("""
<div class="info-box">
<b>Automation potential:</b> forecasts are fully automated once age, balance, contribution and return assumptions are entered. If linked to live ETF prices later, the investment balance could update automatically.
</div>
""", unsafe_allow_html=True)
