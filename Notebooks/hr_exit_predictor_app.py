import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from streamlit_option_menu import option_menu

# ---------- FOLDER & FILE PATHS ----------
PROJECT = "PREDICTING EMPLOYEE ATTRITION"
MODELS_DIR = os.path.join("Models", PROJECT)
DATASETS_DIR = os.path.join("Datasets", PROJECT)

MODEL_PATH = os.path.join(MODELS_DIR, "rf_fe_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler_rf_fe.pkl")
XCOLS_PATH = os.path.join(MODELS_DIR, "model_features_rf_fe.pkl")
DATA_PATH = os.path.join(DATASETS_DIR, "Employee Records.csv")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="HR Exit Predictor", layout="wide")

# ---------- STYLES ----------
st.markdown("""
<style>
[data-testid="stSidebar"]{background:#006983!important;}
[data-testid="stSidebar"]>div:first-child{border-right:none;}
html,body,[data-testid="stAppViewContainer"]>.main{background:white!important;color:black!important;}
.stSelectbox>div,.stSelectbox div[data-baseweb="select"]>div{background:#90e0ef!important;border-radius:8px;}
input[type="number"]{background:#90e0ef!important;border-radius:8px;padding:.4rem;}
div[data-baseweb="slider"] [role="slider"],
div[data-baseweb="slider"]>div>div>div:nth-child(2),
div[data-baseweb="slider"]>div>div>div:nth-child(3){background:#002c66!important;}
div.stButton>button{background:#002c66!important;color:#fff!important;border-radius:8px!important;height:3em;padding:.6rem 1.5rem;border:none;}
div.stButton>button:hover{background:#002c66!important;}
.block-container{padding-top:2rem;padding-bottom:2rem;}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD ARTIFACTS ----------
@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    xcols = joblib.load(XCOLS_PATH)
    return model, scaler, xcols

try:
    model, scaler, X_columns = load_artifacts()
except Exception as e:
    st.error(f"Failed to load model artifacts. Check paths/files:\n{e}")
    st.stop()

# ---------- SIDEBAR ----------
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
            "nav-link": {"font-size": "20px","text-align": "left","margin": "0px","--hover-color":"#002c66","color":"#ffffff"},
            "nav-link-selected": {"background-color":"#00b4d8","color":"#002c66"},
        },
    )

# ---------- HOME ----------
if selected == "Home":
    st.title("🏠 Welcome to the HR Exit Predictor")
    st.markdown("""
This application helps HR professionals identify employees at risk of exit using historical data and machine learning.

---
### 🔍 What You Can Do
- Predict Exit Risk using employee details  
- Explore HR data  
- Learn how the tool works

---
### 📊 Powered By
**Random Forest** (trained on engineered features; standardized and one-hot encoded).

---
### 📎 Disclaimer
This tool supports decision-making, but should be used alongside human judgment.
""")
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=300,
             caption="HR Analytics for Smarter Decisions")

# ---------- PREDICTOR ----------
elif selected == "Predictor":
    st.title("🧠 Employee Exit Probability Predictor")
    st.write("Enter employee details to estimate their risk of leaving.")

    job_title = st.selectbox("Job Title", [
        'Marketing Analyst','Product Manager','HR Specialist','Software Developer',
        'Sales Executive','Data Scientist','Network Engineer','Telecom Technician',
        'IT Support Engineer','Customer Support Agent'
    ])

    department = st.selectbox("Department", [
        'Sales & Marketing','Project Management','Human Resources','IT & Software',
        'Data Analytics','Network Operations','Field Operations','Customer Service','Billing'
    ])

    age = st.slider("Age", 22, 65, 30)
    gender = st.selectbox("Gender", ['Male', 'Female'])
    marital_status = st.selectbox("Marital Status", ['Single', 'Married'])
    years_of_service = st.slider("Years of Service", 1, 10, 2)
    salary = st.number_input("Salary", min_value=100.0, max_value=1000.0, value=350.0)

    if st.button("Predict Exit Probability"):
        input_df = pd.DataFrame({
            'Job Title':[job_title],
            'Department':[department],
            'Age':[age],
            'Gender':[gender],
            'Marital Status':[marital_status],
            'Years of Service':[years_of_service],
            'Salary':[salary]
        })

        # Feature engineering to match training pipeline
        input_df['Age_Group'] = pd.cut(
            input_df['Age'], bins=[20,30,40,50,60,70],
            labels=['20s','30s','40s','50s','60+'], right=False
        )
        input_df['Salary_Band'] = pd.cut(
            input_df['Salary'], bins=[0,200,300,400,500,1000],
            labels=['<200','200-299','300-399','400-499','500+']
        )

        input_df.drop(columns=['Age','Salary'], inplace=True)

        input_encoded = pd.get_dummies(input_df, drop_first=True)

        # Align with training columns
        for col in X_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[X_columns]

        input_scaled = scaler.transform(input_encoded)
        prob = model.predict_proba(input_scaled)[0][1] * 100
        st.success(f"Predicted Exit Probability: {prob:.2f}%")

        st.markdown("### 💡 HR Recommendation")
        if prob < 30:
            st.info("🟢 Low Risk: Likely to stay. Continue regular support.")
        elif 30 <= prob <= 70:
            st.warning("🟡 Moderate Risk: Engage proactively. Offer growth opportunities.")
        else:
            st.error("🔴 High Risk: Act quickly—1:1 conversation and retention incentives.")

# ---------- VIEW DATA ----------
elif selected == "View Data":
    st.title("📁 View Employee Records")
    try:
        df = pd.read_csv(DATA_PATH)
        st.markdown(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        with st.expander("📄 Preview DataFrame"):
            st.dataframe(df)

        with st.expander("🧾 Data Summary"):
            st.write(df.describe(include='all').T)

        st.markdown("### 🎛 Filter Data")
        selected_dept = st.multiselect("Filter by Department", options=df['Department'].dropna().unique())
        selected_gender = st.multiselect("Filter by Gender", options=df['Gender'].dropna().unique())

        filtered_df = df.copy()
        if selected_dept:
            filtered_df = filtered_df[filtered_df['Department'].isin(selected_dept)]
        if selected_gender:
            filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]

        st.markdown(f"Filtered Rows: {filtered_df.shape[0]}")
        st.dataframe(filtered_df.reset_index(drop=True))

        st.markdown("### 📊 Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Gender Distribution")
            st.bar_chart(filtered_df['Gender'].value_counts())
        with col2:
            st.markdown("Department Breakdown")
            st.bar_chart(filtered_df['Department'].value_counts())

    except FileNotFoundError:
        st.error(f"⚠ Data file not found at: {DATA_PATH}")
    except Exception as e:
        st.error(f"⚠ Error loading data: {e}")

# ---------- ABOUT ----------
elif selected == "About":
    st.title("ℹ About This App")
    st.markdown("""
Welcome to the HR Exit Predictor — a data-driven tool to help predict employee attrition and support strategic HR planning.

---
### 🛠 Tech
- Python, Pandas, NumPy  
- Scikit-learn (Random Forest)  
- Streamlit  
- Joblib (artifacts)

---
### 👩🏽‍💻 Developed By
Jennifer Enyonam — Electrical & Electronics Engineer | Data Enthusiast | Women in STEM Advocate

---
### 📫 Contact
- Email: ankujenyonam5@gmail.com  
- LinkedIn: https://www.linkedin.com
""")
    st.image("https://cdn-icons-png.flaticon.com/512/9074/9074702.png", width=300,
             caption="Powered by Data. Guided by Purpose.")
