import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

# Load your saved model, scaler, and feature columns
model = joblib.load('logreg_model.pkl')
scaler = joblib.load('scaler.pkl')
X_columns = joblib.load('X_columns.pkl')

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

# Predict button
if st.button("Predict Exit Probability"):
    # Create DataFrame from input
    new_data = pd.DataFrame({
        'Job Title': [job_title],
        'Department': [department],
        'Age': [age],
        'Gender': [gender],
        'Marital Status': [marital_status],
        'Years of Service': [years_of_service],
        'Salary': [salary]
    })

    # Preprocess
    for col in ['Job Title', 'Department', 'Gender', 'Marital Status']:
        new_data[col] = new_data[col].astype('category')

    new_encoded = pd.get_dummies(new_data)

    for col in X_columns:
        if col not in new_encoded.columns:
            new_encoded[col] = 0
    new_encoded = new_encoded[X_columns]

    new_scaled = scaler.transform(new_encoded)

    # Predict
    prob = model.predict_proba(new_scaled)[0][1] * 100
    st.success(f"Predicted Exit Probability: {prob:.2f}%")
