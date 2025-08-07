import streamlit as st 
import pandas as pd
import numpy as np
import joblib
from streamlit_option_menu import option_menu

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
        div[data-baseweb="slider"] > div > div > div:nth-child(2),
        div[data-baseweb="slider"] > div > div > div:nth-child(3),
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
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# LOAD MODEL ARTIFACTS
# ------------------------------------------------
model = joblib.load("rf_fe_model.pkl")
scaler = joblib.load("scaler_rf_fe.pkl")
X_columns = joblib.load("model_features_rf_fe.pkl")

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
    This application helps HR professionals identify employees at risk of exit using historical data and machine learning.

    ---
    ### 🔍 What You Can Do:
    - Predict Exit Risk using employee details
    - Explore HR data
    - Learn about how the tool works

    ---
    ### 📊 Powered By:
    Random Forest + SMOTE 
    Inputs are standardized and encoded before prediction.

    ---
    ### 📎 Disclaimer:
    This tool supports decision-making, but should be used alongside human judgment.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=300, caption="HR Analytics for Smarter Decisions")

# ------------------------------------------------
# PREDICTOR TAB
# ------------------------------------------------
elif selected == "Predictor":
    st.title("🧠 Employee Exit Probability Predictor")
    st.write("Enter employee details to estimate their risk of leaving.")

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

    if st.button("Predict Exit Probability"):
        input_df = pd.DataFrame({
            'Job Title': [job_title],
            'Department': [department],
            'Age': [age],
            'Gender': [gender],
            'Marital Status': [marital_status],
            'Years of Service': [years_of_service],
            'Salary': [salary]
        })

        # Feature Engineering
        input_df['Age_Group'] = pd.cut(input_df['Age'], bins=[20, 30, 40, 50, 60, 70],
                                       labels=['20s', '30s', '40s', '50s', '60+'], right=False)
        input_df['Salary_Band'] = pd.cut(input_df['Salary'], bins=[0, 200, 300, 400, 500, 1000],
                                         labels=['<200', '200-299', '300-399', '400-499', '500+'])

        # Drop unneeded columns
        input_df.drop(columns=['Age', 'Salary'], inplace=True)

        # One-hot encoding
        input_encoded = pd.get_dummies(input_df, drop_first=True)

        # Ensure all expected columns are present
        for col in X_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[X_columns]

        # Scale numeric features
        input_scaled = scaler.transform(input_encoded)

        # Predict probability
        prob = model.predict_proba(input_scaled)[0][1] * 100
        st.success(f"Predicted Exit Probability: {prob:.2f}%")

        st.markdown("### 💡 HR Recommendation")
        if prob < 30:
            st.info("🟢 Low Risk: Likely to stay. Continue regular support.")
        elif 30 <= prob <= 70:
            st.warning("🟡 Moderate Risk: Engage employee proactively. Offer growth opportunities.")
        else:
            st.error("🔴 High Risk: Take action. Consider personal engagement and incentives.")

# ------------------------------------------------
# VIEW DATA TAB
# ------------------------------------------------
elif selected == "View Data":
    st.title("📁 View Employee Records")
    try:
        df = pd.read_csv("Employee Records.csv")
        st.markdown(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        with st.expander("📄 Preview DataFrame"):
            st.dataframe(df.style.set_properties({'background-color': '#F0F4FF'}, subset=df.columns))

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
            gender_count = filtered_df['Gender'].value_counts()
            st.bar_chart(gender_count)

        with col2:
            st.markdown("Department Breakdown")
            dept_count = filtered_df['Department'].value_counts()
            st.bar_chart(dept_count)

    except Exception as e:
        st.error(f"⚠ Error loading data: {e}")
        st.info("Ensure 'Employee Records.csv' is available in the app folder.")

# ------------------------------------------------
# ABOUT TAB
# ------------------------------------------------
elif selected == "About":
    st.title("ℹ About This App")
    st.markdown("""
    Welcome to the HR Exit Predictor — a data-driven tool built to help HR professionals predict employee attrition and support strategic planning.

    ---
    ### 🎯 Purpose
    Predict which employees are likely to exit soon and guide timely HR interventions.

    ---
    ### 🛠 Technologies Used
    - Python, Pandas, NumPy
    - Scikit-learn (Random Forest + SMOTE)
    - Streamlit for interactive interface
    - Joblib for saving/loading model files

    ---
    ### 👩🏽‍💻 Developed By
    Jennifer Enyonam  
    Electrical & Electronics Engineer | Data Enthusiast | Women in STEM Advocate

    ---
    ### 📫 Contact
    - Email: ankujenyonam5@gmail.com
    - LinkedIn: [Jennifer Enyonam](https://www.linkedin.com)

    ---
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/9074/9074702.png", width=300, caption="Powered by Data. Guided by Purpose.")
