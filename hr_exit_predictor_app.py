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
            background-color: #16abc2 !important;
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
            background-color: ##16abc2 !important;
            border-radius: 8px;
        }
        input[type="number"] {
            background-color: #16abc2 !important;
            border-radius: 8px;
            padding: 0.4rem;
        }
        div[data-baseweb="slider"] > div > div > div:nth-child(2) {
            background: #002c66 !important;
        }
        div[data-baseweb="slider"] > div > div > div:nth-child(3) {
            background: #e6e6e6 !important;
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
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#16abc2"},
            "icon": {"color": "#002c66", "font-size": "20px"},
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
    st.markdown("""
    This application is designed to help HR professionals identify employees who are likely to leave the organization, using historical data and machine learning.

    ---
    ### 🔍 What You Can Do:
    - **Predict Exit Risk:** Use the *Predictor* tab to estimate the probability that an employee will leave based on input features like age, department, salary, etc.
    - **Explore the Data:** View employee-related datasets.
    - **Learn More:** Visit the *About* section for more information on the app's purpose and development.
    
    ---
    ### 📊 How It Works:
    We use a **Random Forest +SMOTE** model trained on HR data to analyze patterns and predict exit probabilities. Inputs are standardized and encoded before feeding into the model.

    ---
    ### 📎 Disclaimer:
    This tool is for educational and decision-support purposes only. It should not be the sole basis for HR decisions.
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
            st.info("🟢 **Low Risk:** The employee is likely to stay. Continue monitoring and provide regular support.")
        elif 30 <= prob <= 70:
            st.warning("🟡 **Moderate Risk:** Engage the employee. Consider offering professional development, mentorship, or workload reviews.")
        else:
            st.error("🔴 **High Risk:** Take immediate action. Consider a one-on-one conversation, career growth incentives, or team reassignment.")

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
            gender_count = filtered_df['Gender'].value_counts()
            st.bar_chart(gender_count)

        with col2:
            st.markdown("**Department Breakdown**")
            dept_count = filtered_df['Department'].value_counts()
            st.bar_chart(dept_count)

    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.info("Please make sure 'Employee Records.csv' is in the same directory or uploaded correctly.")

# ------------------------------------------------
# ABOUT TAB
# ------------------------------------------------
elif selected == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    Welcome to the **HR Exit Predictor** – an intelligent, data-driven application designed to empower HR professionals with the insights they need to make proactive talent decisions.

    ---
    ### 🎯 Purpose
    This tool predicts the likelihood that an employee may exit an organization. The aim is to support HR managers in identifying potential retention risks early and making informed interventions.

    ---
    ### 🛠️ Technologies Used
    - **Python** for scripting  
    - **Pandas** and **NumPy** for data handling  
    - **Scikit-learn** for building the Logistic Regression model  
    - **Streamlit** for crafting an interactive user interface  
    - **Joblib** for saving and loading model artifacts

    ---
    ### 👩🏽‍💻 Developed By
    **Jennifer Enyonam**  
    *Electrical & Electronics Engineer | Data Enthusiast | Women in STEM Advocate*  
    Passionate about using data and technology to drive real-world solutions in HR, energy, and society at large.

    ---
    ### ❤️ Special Notes
    - This is a demonstration tool meant for educational and analytical purposes.
    - Always complement data-driven decisions with human judgment and organizational context.

    ---
    ### 📫 Contact / Feedback
    Feel free to connect or provide feedback to help improve this app!  
    - LinkedIn: [Jennifer Enyonam](https://www.linkedin.com)  
    - Email: ankujenyonam5@gmail.com

    ---
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/9074/9074702.png", width=300, caption="Powered by Data. Guided by Purpose.")
