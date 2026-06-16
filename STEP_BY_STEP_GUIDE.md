
import streamlit as st
from utils.styling import apply_global_style

st.set_page_config(
    page_title="Family Wealth Platform",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_style()

st.sidebar.markdown("""
<div class="logo-box">
  <div class="logo-icon">↗</div>
  <div>
    <div class="logo-title">Family Wealth</div>
    <div class="logo-sub">Private Planning Platform</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">Family Wealth Platform</div>
    <div class="hero-subtitle">Three private planning dashboards for different life stages.</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="home-card">
        <div class="home-icon">📈</div>
        <div class="home-title">Wealth Builder</div>
        <div class="home-text">For Mum & Dad: shares, ETFs, dividends, income target and financial freedom planning.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="home-card">
        <div class="home-icon">🏡</div>
        <div class="home-title">Home Builder</div>
        <div class="home-text">For a first-home buyer: deposit progress, purchase costs, mortgage estimate and cost-of-living readiness.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="home-card">
        <div class="home-icon">🚗</div>
        <div class="home-title">Future Builder</div>
        <div class="home-text">For younger kids: car savings, investing early and long-term compounding to age 55.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<b>Privacy note:</b> this demo uses dummy data only. For real personal financial data, run locally on your own PC first or deploy privately with access controls.
</div>
""", unsafe_allow_html=True)

st.markdown("### How to use")
st.write("""
Use the page menu on the left to open each dashboard. Each page currently uses its own dummy CSV from the `data/` folder.
Later, each family member can have their own private CSV or database table.
""")
