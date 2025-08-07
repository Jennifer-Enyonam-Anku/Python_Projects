import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from streamlit_option_menu import option_menu
import joblib

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="HR Exit Predictor", layout="wide")

# ------------------------------------------------
# CUSTOM STYLING
# ------------------------------------------------
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            border-right: none;
        }
        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }
        .stSelectbox > div,
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #90e0ef !important;
            border-radius: 8px; 
        }
        input[type="number"] {
            background-color: #90e0ef !important;
            border-radius: 8px;
            padding: 0.4rem;
        }
        div[data-baseweb="slider"] > div > div > div:nth-child(2) {
            background: #002c66 !important;
        }
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
            height: 3em;
            width: auto;
            padding: 0.6rem 1.5rem;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #002c66 !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* 🛠️ Remove rounded corners from sidebar nav buttons */
        .nav-link, .nav-link-selected {
            border-radius: 0px !important;
            -webkit-border-radius: 0px !important;
            -moz-border-radius: 0px !important;
        }
        .nav-link:hover, .nav-link-selected:hover {
            border-radius: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# MODEL LOADING
# ------------------------------------------------
model = joblib.load('logreg_model.pkl')
scaler = joblib.load('scaler.pkl')
X_columns = joblib.load('X_columns.pkl')

# ------------------------------------------------
# SIDEBAR MENU
# ------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Predictor", "View Data", "About"],
        icons=["house", "bar-chart", "folder", "info-circle"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#006983"},
            "icon": {"color": "#3edad8", "font-size": "22px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#002c66",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background-color": "#00b4d8",
                "color": "#002c66"
            },
        },
    )

# ------------------------------------------------
# HOME TAB
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Welcome to the HR Exit Predictor")
    st.markdown("""
    This application is designed to help HR professionals identify employees who are likely to leave the organization, using historical data and machine learning.

    ---
    ### 🔍 What You Can Do:
    - Predict Exit Risk: Use the Predictor tab to estimate the probability that an employee will leave based on input features like age, department, salary, etc.
    - Explore the Data: View employee-related datasets.
    - Learn More: Visit the About section for more information on the app's purpose and development.
    
    ---
    ### 📊 How It Works:
    We use a Random Forest +SMOTE model trained on HR data to analyze patterns and predict exit probabilities. Inputs are standardized and encoded before feeding into the model.

    ---
    ### 📎 Disclaimer:
    This tool is for educational and decision-support purposes only. It should not be the sole basis for HR decisions.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=300, caption="HR Analytics for Smarter Decisions")
