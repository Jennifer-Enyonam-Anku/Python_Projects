import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from streamlit_option_menu import option_menu
import joblib

# ================================================
# CRITICAL STYLING FIXES - MUST COME FIRST
# ================================================
st.markdown("""
<style>
    /* NUCLEAR OPTION FOR SIDEBAR WHITE CORNERS */
    [data-testid="stSidebar"] {
        background-color: #006983 !important;
    }

    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] > div:first-child > div > div,
    .st-emotion-cache-1vq4p4l {
        background-color: #006983 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .st-emotion-cache-1wbqy5l {
        gap: 0 !important;
    }

    .stSelectbox > div,
    .stSelectbox div[data-baseweb="select"] > div,
    input[type="number"] {
        background-color: #90e0ef !important;
        border-radius: 8px !important;
        padding: 0.4rem !important;
    }

    div[data-baseweb="slider"] > div > div > div:nth-child(2),
    div[data-baseweb="slider"] > div > div > div:nth-child(3) {
        background: #002c66 !important;
    }

    div[data-baseweb="slider"] [role="slider"] {
        background-color: #002c66 !important;
    }

    div.stButton > button {
        background-color: #002c66 !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3em !important;
        width: auto !important;
        padding: 0.6rem 1.5rem !important;
        border: none !important;
    }

    div.stButton > button:hover {
        background-color: #af4c0f !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ================================================
# PAGE CONFIGURATION
# ================================================
st.set_page_config(page_title="HR Exit Predictor", layout="wide")

# ================================================
# MODEL LOADING
# ================================================
model = joblib.load('logreg_model.pkl')
scaler = joblib.load('scaler.pkl')
X_columns = joblib.load('X_columns.pkl')

# ================================================
# SIDEBAR MENU - WITH WHITE CORNERS FIXED
# ================================================
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Predictor", "View Data", "About"],
        icons=["house", "bar-chart", "folder", "info-circle"],
        default_index=0,
        styles={
            "container": {
                "padding": "0 !important",
                "margin": "0 !important",
                "background-color": "#006983 !important",
                "border": "none !important"
            },
            "icon": {
                "color": "#3edad8 !important", 
                "font-size": "22px !important"
            },
            "nav-link": {
                "font-size": "20px !important",
                "text-align": "left !important",
                "margin": "0 !important",
                "--hover-color": "#002c66 !important",
                "color": "#ffffff !important",
                "border-radius": "0 !important",
                "padding": "10px 15px !important",
                "border": "none !important"
            },
            "nav-link-selected": {
                "background-color": "#00b4d8 !important",
                "color": "#ffffff !important",
                "border-radius": "0 !important",
                "border": "none !important"
            },
        }
    )
