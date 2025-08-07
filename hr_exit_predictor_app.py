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
            background: #af4c0f !important;
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
            background-color: #af4c0f !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* ✅ FIX: Remove white borders or outlines */
        .nav-link:focus,
        .nav-link:focus-visible,
        .nav-link:active {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
        }
        .nav-link {
            border: none !important;
            box-shadow: none !important;
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
                "color": "#ffffff"
            },
        },
    )

# ------------------------------------------------
# HOME TAB
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Welcome to the HR Exit Predictor")
    st.markdown("""
    This application helps HR professionals identify employees who are likely to leave the organization using historical data and machine learning.

    ---
    ### 🔍 What You Can Do:
    - **Predict Exit Risk:** Use the *Predictor* tab to estimate exit probabilities.
    - **Explore the Data:** Use the *View Data* tab to explore employee datasets.
    - **Learn More:** Visit the *About* section for details on the app.

    ---
    ### 📊 How It Works:
    We use a **Random Forest + SMOTE** model trained on HR data. Inputs are encoded and scaled before prediction.

    ---
    ### 📎 Disclaimer:
    This is a decision-support tool for educational use.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=300, caption="HR Analytics for Smarter Decisions")

# ------------------------------------------------
# PREDICTOR TAB
# ------------------------------------------------
elif selected == "Predictor":
    st.title("🧠 Employee Exit Probability Predictor")
    st.write("Fill in the employee details to predict their likelihood of exiting.")

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

        st.markdown("### 💡 HR Recommendation")
        if prob < 30:
            st.info("🟢 **Low Risk:** Likely to stay. Continue monitoring and supporting.")
        elif 30 <= prob <= 70:
            st.warning("🟡 **Moderate Risk:** Engage the employee with mentorship, training, or workload reviews.")
        else:
            st.error("🔴 **High Risk:** Act now. Consider conversation, incentives, or role reassignment.")

# ------------------------------------------------
# VIEW DATA TAB
# ------------------------------------------------
elif selected == "View Data":
    st.title("📁 View Employee Records")

    try:
        df = pd.read_csv("Employee Records.csv")

        st.markdown(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

        with st.expander("📄 Preview DataFrame"):
            st.dataframe(df.style.set_properties(**{'background-color': '#F0F4FF'}, subset=df.columns))

        with st.expander("🧾 Data Summary"):
            st.write(df.describe(include='all').T)

        st.markdown("### 🎛️ Filter Data")
        selected_dept = st.multiselect("Filter by Department", options=df['Department'].dropna().unique())
        selected_gender = st.multiselect("Filter by Gender", options=df['Gender'].dropna().unique())

        filtered_df = df.copy()
        if selected_dept:
            filtered_df = filtered_df[filtered_df['Department'].isin(selected_dept)]
        if selected_gender:
            filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]

        st.markdown(f"**Filtered Rows:** {filtered_df.shape[0]}")
        st.dataframe(filtered_df.reset_index(drop=True))

        st.markdown("### 📊 Insights")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Gender Distribution**")
            st.bar_chart(filtered_df['Gender'].value_counts())

        with col2:
            st.markdown("**Department Breakdown**")
            st.bar_chart(filtered_df['Department'].value_counts())

    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.info("Ensure 'Employee Records.csv' is available in the working directory.")

# ------------------------------------------------
# ABOUT TAB
# ------------------------------------------------
elif selected == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    Welcome to the **HR Exit Predictor** – a data-powered app that empowers HR professionals to predict and manage staff attrition risks.

    ---
    ### 🎯 Purpose
    Predict the likelihood of employee exits to enable early HR interventions and retention strategies.

    ---
    ### 🛠️ Built With
    - **Python** – Programming  
    - **Pandas & NumPy** – Data processing  
    - **Scikit-learn** – ML model  
    - **Streamlit** – Web interface  
    - **Joblib** – Model storage

    ---
    ### 👩🏽‍💻 Developer
    **Jennifer Enyonam**  
    Electrical & Electronics Engineer | Data Enthusiast | Women in STEM Advocate

    ---
    ### 💌 Feedback & Contact
    - LinkedIn: [Jennifer Enyonam](https://www.linkedin.com)  
    - Email: ankujenyonam5@gmail.com

    ---
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/9074/9074702.png", width=300, caption="Powered by Data. Guided by Purpose.")
