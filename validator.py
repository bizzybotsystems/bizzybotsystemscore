import streamlit as st
import pandas as pd

# BizzyBot Core Configuration
st.set_page_config(page_title="BizzyBot | Live Validator", page_icon="⚡")
st.title("⚡ BizzyBot Systems Core")
st.subheader("Automated Compliance Validator")

# File Upload Slot
uploaded_file = st.file_uploader("Upload your file here", type=["xlsx", "csv"])

# Compliance Logic
def validate_compliance(df):
    results = []
    for index, row in df.iterrows():
        errors = []
        patient_id = str(row.get('Patient_ID', ''))
        if not any(char.isdigit() for char in patient_id):
            errors.append("Invalid ID format")
        if pd.isna(row.get('Form_Type')):
            errors.append("Form Type is required")
        if str(row.get('Completion_Status', '')).lower() != 'completed':
            errors.append("Form must be marked 'Completed'")
        
        status = "❌ Compliance Failure" if errors else "✅ Compliant"
        results.append({'Patient_ID': patient_id, 'Status': status, 'Errors': ", ".join(errors)})
    return pd.DataFrame(results)

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file)
        results = validate_compliance(data)
        st.write("### 📜 Automated Compliance Report")
        st.dataframe(results)
    except Exception as e:
        st.error(f"Error processing file: {e}")
