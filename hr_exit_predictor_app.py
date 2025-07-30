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
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #E3E7F7 !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            border-right: none;
        }

        /* Light theme override */
        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* Selectbox wrapper and dropdown */
        .stSelectbox > div,
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #E3E7F7 !important;
            border-radius: 8px;
        }

        /* Number input (Salary) */
        input[type="number"] {
            background-color: #E3E7F7 !important;
            border-radius: 8px;
            padding: 0.4rem;
        }

        /* 🎯 Slider styling: track and thumb */
        div[data-baseweb="slider"] > div > div > div:nth-child(2) {
            background: #4B0082 !important;
        }
        div[data-baseweb="slider"] > div > div > div:nth-child(3) {
            background: #e6e6e6 !important;
        }
        div[data-baseweb="slider"] [role="slider"] {
            background-color: #4B0082 !important;
        }

        /* 🎯 Button styling */
        div.stButton > button {
            background-color: #4B0082 !important;
            color: white !important;
            border-radius: 8px !important;
            height: 3em;
            width: auto;
            padding: 0.6rem 1.5rem;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #3a006b !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
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
        default_index=1,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#E3E7F7"
            },
            "icon": {"color": "#4B0082", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#D5D9F0",
                "color": "#333333"
            },
            "nav-link-selected": {
                "background-color": "#C2C7EA",
                "color": "#000000"
            },
        },
    )

# ------------------------------------------------
# HOME TAB
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Welcome to the HR Exit Predictor")
    st.write("Use the navigation on the left to explore the app and predict employee exits.")

# ------------------------------------------------
# PREDICT TAB
# ------------------------------------------------
elif selected == "Predictor":
    st.title("🧠 Employee Exit Probability Predictor")
    st.write("Fill in the employee details to predict their likelihood of exiting.")

    # Input fields
    job_title = st.selectbox("Job Title", [
        'Marketing Analyst', 'Product Manager', 'HR Specialist', 'Software Developer',
        'Sales Executive', 'Data Scientist', 'Network Engineer', 'Telecom Technician',
        'IT Support Engineer', 'Customer Support Agent'
    ])

    department = st.selectbox("Department", [
        'Sales & Marketing', 'Project Management', 'Human Resources', 'IT & Software',
        'Data Analytics', 'Network Operations', 'Field Operations', 'Customer Service', 'Billing'
    ])

    age = st.slider("Age", 22, 65, 30)
    gender = st.selectbox("Gender", ['Male', 'Female'])
    marital_status = st.selectbox("Marital Status", ['Single', 'Married'])
    years_of_service = st.slider("Years of Service", 1, 10, 2)
    salary = st.number_input("Salary", min_value=100.0, max_value=1000.0, value=350.0)

    # Prediction logic
    if st.button("Predict Exit Probability"):
        new_data = pd.DataFrame({
            'Job Title': [job_title],
            'Department': [department],
            'Age': [age],
            'Gender': [gender],
            'Marital Status': [marital_status],
            'Years of Service': [years_of_service],
            'Salary': [salary]
        })

        for col in ['Job Title', 'Department', 'Gender', 'Marital Status']:
            new_data[col] = new_data[col].astype('category')

        new_encoded = pd.get_dummies(new_data)

        for col in X_columns:
            if col not in new_encoded.columns:
                new_encoded[col] = 0
        new_encoded = new_encoded[X_columns]

        new_scaled = scaler.transform(new_encoded)
        prob = model.predict_proba(new_scaled)[0][1] * 100
        st.success(f"Predicted Exit Probability: {prob:.2f}%")

# ------------------------------------------------
# VIEW DATA TAB
# ------------------------------------------------
elif selected == "View Data":
    st.title("📁 View Employee Data")
    st.info("Feature coming soon! You can load Existing_Staff and Exited_Staff datasets here.")

# ------------------------------------------------
# ABOUT TAB
# ------------------------------------------------
elif selected == "About":
    st.title("ℹ About This App")
    st.markdown("""
        This Streamlit app predicts the probability that an employee may exit the organization.

        *Built by:* Jennifer Enyonam  
        *Tools:* Python, Streamlit, Scikit-learn  
        *Goal:* Help HR improve employee retention through data-driven prediction.
    """)
