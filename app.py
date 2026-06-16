
import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #f6f8fc; }

    .block-container {
        padding-top: 2.4rem;
        padding-left: 1.7rem;
        padding-right: 1.7rem;
        max-width: 1700px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071327 0%, #0b1a33 100%);
    }

    section[data-testid="stSidebar"] * { color: #f8fafc !important; }

    .logo-box { display:flex; gap:12px; align-items:center; margin-bottom:22px; }

    .logo-icon {
        width:40px; height:40px; border-radius:13px;
        background:linear-gradient(135deg,#2563eb,#22c55e);
        display:flex; align-items:center; justify-content:center;
        font-weight:900; font-size:22px; color:white;
    }

    .logo-title { font-size:22px; font-weight:900; line-height:1; }
    .logo-sub { font-size:13px; color:#cbd5e1 !important; margin-top:3px; }

    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #edf4ff 100%);
        border:1px solid #dbe4f0;
        border-radius:22px;
        padding:26px 30px;
        box-shadow:0 8px 22px rgba(15,23,42,0.055);
        margin-bottom:22px;
    }

    .hero-title { font-size:34px; font-weight:900; color:#0f172a; letter-spacing:-0.6px; margin-bottom:4px; }
    .hero-subtitle { color:#475569; font-size:15px; }

    .metric-card {
        background:#ffffff; border:1px solid #dbe4f0; border-radius:18px;
        padding:18px; box-shadow:0 8px 22px rgba(15,23,42,0.055); min-height:110px;
    }

    .metric-label { color:#64748b; font-size:12px; font-weight:800; margin-bottom:6px; }
    .metric-value { color:#0f172a; font-size:25px; font-weight:900; line-height:1.1; }
    .metric-sub-green { color:#16a34a; font-size:12px; font-weight:900; margin-top:5px; }
    .metric-sub-red { color:#dc2626; font-size:12px; font-weight:900; margin-top:5px; }

    .panel {
        background:#ffffff; border:1px solid #dbe4f0; border-radius:18px;
        padding:20px; box-shadow:0 8px 22px rgba(15,23,42,0.05); margin-bottom:18px;
    }

    .panel-title { color:#0f172a; font-size:18px; font-weight:900; margin-bottom:10px; }
    .panel-sub { color:#64748b; font-size:13px; margin-bottom:10px; }

    .info-box {
        background:#ffffff; border:1px solid #dbe4f0; border-left:5px solid #2563eb;
        border-radius:16px; padding:16px; box-shadow:0 8px 22px rgba(15,23,42,0.04);
        margin:18px 0; color:#0f172a;
    }

    .home-card {
        background:#ffffff; border:1px solid #dbe4f0; border-radius:20px;
        padding:22px; min-height:210px; box-shadow:0 8px 22px rgba(15,23,42,0.055);
    }

    .home-icon { font-size:34px; margin-bottom:12px; }
    .home-title { font-size:22px; font-weight:900; color:#0f172a; margin-bottom:8px; }
    .home-text { font-size:14px; color:#475569; line-height:1.5; }

    .progress-bar { height:12px; background:#e5e7eb; border-radius:999px; overflow:hidden; margin:12px 0 8px 0; }
    .progress-fill { height:12px; background:linear-gradient(90deg,#22c55e,#2563eb); border-radius:999px; }

    div[data-testid="stDataFrame"] {
        border-radius:14px; overflow:hidden; border:1px solid #e2e8f0;
    }

    @media (max-width: 768px) {
        .block-container { padding-left:0.8rem; padding-right:0.8rem; padding-top:1.2rem; }
        .hero-title { font-size:28px; }
        .metric-value { font-size:22px; }
    }
    </style>
    """, unsafe_allow_html=True)
