
import streamlit as st
import pandas as pd
from utils.styling import apply_global_style
from utils.calculations import money, calculate_mortgage_payment

st.set_page_config(page_title="Home Builder", page_icon="🏡", layout="wide")
apply_global_style()

st.markdown("""
<div class="hero">
    <div class="hero-title">Home Builder</div>
    <div class="hero-subtitle">For a first-home buyer: deposit progress, purchase costs and life-after-purchase affordability.</div>
</div>
""", unsafe_allow_html=True)

goals = pd.read_csv("data/home_builder_sample.csv").iloc[0]
costs = pd.read_csv("data/home_living_costs_sample.csv")

st.sidebar.markdown("### Home Purchase Assumptions")
house_price = st.sidebar.number_input("Target property price", min_value=100000, max_value=2000000, value=int(goals["Target Property Price"]), step=25000)
current_savings = st.sidebar.number_input("Current savings", min_value=0, max_value=1000000, value=int(goals["Current Savings"]), step=5000)
monthly_savings = st.sidebar.number_input("Monthly savings", min_value=0, max_value=20000, value=int(goals["Monthly Savings"]), step=250)
deposit_percent = st.sidebar.slider("Deposit %", 5, 30, int(goals["Deposit %"]))
interest_rate = st.sidebar.slider("Mortgage interest rate %", 2.0, 10.0, float(goals["Interest Rate %"]), 0.25)
loan_years = st.sidebar.slider("Loan years", 15, 35, int(goals["Loan Years"]))

deposit_required = house_price * deposit_percent / 100
stamp_duty_estimate = house_price * 0.045
settlement_costs = 7000
moving_setup = 12000
emergency_buffer = 20000
total_cash_required = deposit_required + stamp_duty_estimate + settlement_costs + moving_setup + emergency_buffer
progress = min(current_savings / total_cash_required * 100, 100) if total_cash_required else 0
gap = max(total_cash_required - current_savings, 0)
months_to_ready = gap / monthly_savings if monthly_savings else 999

loan_amount = house_price - deposit_required
monthly_mortgage = calculate_mortgage_payment(loan_amount, interest_rate, loan_years)
monthly_living_costs = costs["Monthly Cost"].sum()
monthly_after_purchase = monthly_mortgage + monthly_living_costs

income_monthly = goals["Monthly Income After Tax"]
surplus = income_monthly - monthly_after_purchase

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("Total Cash Required", money(total_cash_required), "deposit + costs + buffer", False),
    ("Current Savings", money(current_savings), f"{progress:.0f}% ready", False),
    ("Savings Gap", money(gap), f"{months_to_ready:.1f} months", True),
    ("Mortgage Estimate", money(monthly_mortgage), "per month", False),
    ("Post-Purchase Surplus", money(surplus), "per month", surplus < 800),
]
for col, (label, value, sub, red) in zip([c1,c2,c3,c4,c5], metrics):
    with col:
        cls = "metric-sub-red" if red else "metric-sub-green"
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="{cls}">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.1, 1.5])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Deposit & Purchase Readiness</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{progress}%;"></div></div>', unsafe_allow_html=True)
    st.write(f"Saved **{money(current_savings)}** of estimated **{money(total_cash_required)}** required.")
    st.write(f"Estimated time to readiness: **{months_to_ready:.1f} months**")
    if surplus > 1000:
        st.success("Comfortable after purchase based on dummy assumptions.")
    elif surplus > 300:
        st.warning("Possible, but tight. Review living costs and buffer.")
    else:
        st.error("High risk. More savings or lower property price may be required.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    years = list(range(0, 8))
    rows = []
    savings = current_savings
    for year in years:
        if year > 0:
            savings += monthly_savings * 12
        rows.append({"Year": year, "Projected Savings": savings, "Total Cash Required": total_cash_required})
    forecast = pd.DataFrame(rows).set_index("Year")
    st.markdown("### Savings Forecast")
    st.line_chart(forecast, height=330)

st.markdown("### Post-Purchase Monthly Cost Estimate")
st.dataframe(costs, hide_index=True, use_container_width=True)

st.markdown("""
<div class="info-box">
<b>Automation potential:</b> mortgage repayment calculations, savings forecasts and readiness status can be fully automated. Property price, income, savings and living costs should be manual inputs.
</div>
""", unsafe_allow_html=True)
