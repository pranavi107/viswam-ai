import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Loan Fraud Predictor", layout="centered")

st.title("🔍 Loan Fraud Detection App")

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Define input fields
st.header("📥 Enter Applicant Details")

loan_amount_requested = st.number_input("Loan Amount Requested", value=50000)
loan_tenure_months = st.slider("Loan Tenure (Months)", 6, 60, 24)
interest_rate_offered = st.slider("Interest Rate (%)", 1.0, 30.0, 12.0)
monthly_income = st.number_input("Monthly Income", value=30000)
existing_emis_monthly = st.number_input("Existing EMIs Monthly", value=5000)
debt_to_income_ratio = st.number_input("Debt to Income Ratio", value=0.3)
applicant_age = st.slider("Applicant Age", 18, 70, 35)
number_of_dependents = st.slider("Number of Dependents", 0, 5, 1)

avg_txn_amt = st.number_input("Average Transaction Amount", value=10000)
total_txn_amt = st.number_input("Total Transaction Amount", value=50000)
max_txn_amt = st.number_input("Max Transaction Amount", value=20000)
min_txn_amt = st.number_input("Min Transaction Amount", value=500)
txn_count = st.number_input("Transaction Count", value=10)
intl_txn_ratio = st.slider("International Transaction Ratio", 0.0, 1.0, 0.1)

loan_type = st.selectbox("Loan Type", ["Business Loan", "Car Loan", "Education Loan", "Personal Loan"])
employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed"])
property_ownership_status = st.selectbox("Property Ownership Status", ["Rented", "Owned", "Mortgaged"])
gender = st.selectbox("Gender", ["Male", "Female"])
purpose_of_loan = st.selectbox("Purpose of Loan", ["Business", "Education", "Personal", "Vehicle"])

# Encode inputs
loan_to_income_ratio = loan_amount_requested / (monthly_income + 1)
emi_to_income_ratio = existing_emis_monthly / (monthly_income + 1)
interest_burden = (interest_rate_offered * loan_amount_requested) / (monthly_income + 1)
high_intl_txn = 1 if intl_txn_ratio > 0.4 else 0
age_group = (
    "Young" if applicant_age <= 30 else
    "Mid-Age" if applicant_age <= 45 else
    "Senior" if applicant_age <= 60 else
    "Elder"
)

# Create a DataFrame for the model
input_dict = {
    'loan_amount_requested': loan_amount_requested,
    'loan_tenure_months': loan_tenure_months,
    'interest_rate_offered': interest_rate_offered,
    'monthly_income': monthly_income,
    'existing_emis_monthly': existing_emis_monthly,
    'debt_to_income_ratio': debt_to_income_ratio,
    'applicant_age': applicant_age,
    'number_of_dependents': number_of_dependents,
    'avg_txn_amt': avg_txn_amt,
    'total_txn_amt': total_txn_amt,
    'max_txn_amt': max_txn_amt,
    'min_txn_amt': min_txn_amt,
    'txn_count': txn_count,
    'intl_txn_ratio': intl_txn_ratio,
    'loan_to_income_ratio': loan_to_income_ratio,
    'emi_to_income_ratio': emi_to_income_ratio,
    'interest_burden': interest_burden,
    'high_intl_txn': high_intl_txn,

    # One-hot encoded fields (you must match training format)
    f'loan_type_{loan_type}': 1,
    f'purpose_of_loan_{purpose_of_loan}': 1,
    f'employment_status_{employment_status}': 1,
    f'property_ownership_status_{property_ownership_status}': 1,
    f'gender_{gender}': 1,
    f'age_group_{age_group}': 1,
}

# Load feature columns used during training
with open("feature_columns.pkl", "rb") as f:
    feature_cols = pickle.load(f)

# Fill missing features with 0
full_input = {col: input_dict.get(col, 0) for col in feature_cols}
input_df = pd.DataFrame([full_input])

# Predict
if st.button("🔎 Predict Fraud"):
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]
    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ High Fraud Risk Detected! Probability: {prob:.2f}")
    else:
        st.success(f"✅ Loan Looks Legitimate. Probability of Fraud: {prob:.2f}")
