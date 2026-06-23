import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="BizzyBot Systems Core", page_icon="⚡")

st.title("⚡ BizzyBot Systems Core")
st.subheader("Automated Compliance Validator")

# Pro-Tip: Define your required schema so it never fails on bad column names
REQUIRED_COLUMNS = ['Patient_ID', 'Form_Type', 'Completion_Status', 'Submission_Date']

uploaded_file = st.file_uploader("Upload your file (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # 1. Futuristic Logic: Detect file type automatically
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

        st.success("File uploaded successfully!")

        # 2. Schema Validation (The "BizzyBot" standard)
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
        else:
            # 3. Intelligent Audit
            st.write("### Audit Results")
            
            # Identify "Messy" Rows
            null_count = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()
            
            # Show summary stats to make the client feel they got "value"
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows Processed", len(df))
            col2.metric("Missing Values", null_count)
            col3.metric("Duplicates", duplicates)

            # Display errors for the client
            if null_count > 0 or duplicates > 0:
                st.warning("⚠️ Data quality issues detected. Please review the flagged rows below.")
                st.dataframe(df[df.isnull().any(axis=1) | df.duplicated()])
            else:
                st.balloons()
                st.success("✅ Perfect compliance! Your data is ready.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
