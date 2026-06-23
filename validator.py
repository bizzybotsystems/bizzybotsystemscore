import streamlit as st
import pandas as pd
import io

# ==========================================
# BIZZYBOT SYSTEMS CORE: COMPLIANCE & CONTENT
# ==========================================

st.set_page_config(page_title="BizzyBot Live Validator", page_icon="⚡")
st.title("⚡ BizzyBot Systems Core")

tab1, tab2 = st.tabs(["⚡ Compliance Validator", "📝 Content Engine"])

# --- TAB 1: COMPLIANCE VALIDATOR (CLIENT FACING) ---
with tab1:
    st.subheader("Automated Compliance Validator")
    uploaded_file = st.file_uploader("Upload your data file here", type=["xlsx", "csv"])

    with st.sidebar:
        st.write("## 🛠️ Builder Tools")
        auto_test = st.button("GENERATE FAKE DATA & TEST")

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
                errors.append("Must be 'Completed'")
            status = "❌ Compliance Failure" if errors else "✅ Compliant"
            results.append({'Patient_ID': patient_id, 'Validation_Status': status, 'Specific_Errors': ", ".join(errors)})
        return pd.DataFrame(results)

    data_source = None
    if uploaded_file:
        try: data_source = pd.read_excel(uploaded_file)
        except: data_source = pd.read_csv(uploaded_file)
    elif auto_test:
        data_source = pd.DataFrame({'Patient_ID': ['P101-1', 'P102-2'], 'Form_Type': ['Intake', 'Consent'], 'Completion_Status': ['Completed', None]})
    
    if data_source is not None:
        validation_df = validate_compliance(data_source)
        
        # DISPLAY PARTIAL RESULTS (FREE)
        st.write("### Audit Summary")
        st.dataframe(validation_df[['Patient_ID', 'Validation_Status']])
        
        # THE "GATE"
        st.warning("🔒 Detailed error reports are locked.")
        if st.button("Unlock Full Report ($10)"):
            st.link_button("Go to Payment", "https://buy.stripe.com/4gM3cv2c0cvudrg6Ic7g404")
            
        # HIDDEN SECTION
        if st.checkbox("I have already purchased access (Admin Override)"):
            st.write("### Full Detailed Audit")
            st.dataframe(validation_df)

# --- TAB 2: CONTENT ENGINE (ADMIN ONLY) ---
with tab2:
    st.header("BizzyBot Content Engine")
    password = st.sidebar.text_input("Admin Password:", type="password")
    
    if password == "BIZZYBOT123": 
        industry = st.text_input("Enter Industry:")
        problem = st.text_input("Describe '3 AM' problem:")
        if st.button("Generate Article"):
            st.markdown(f"### Solving {problem} in {industry}\n\nAt BizzyBotSystems, we automate the path to compliance.")
    else:
        st.warning("⚠️ Restricted Area: Enter password in sidebar to access.")
