import streamlit as st
import pandas as pd
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info
from database import get_patient_history, get_all_patient_history, add_patient_history

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title("📋 Patient History")

with st.sidebar:
    if st.button("⬅️ Back"):
        if st.session_state.user['role'] == 'admin':
            st.switch_page("pages/05_Admin_Dashboard.py")
        else:
            st.switch_page("pages/04_User_Dashboard.py")
    
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.switch_page("pages/01_Login.py")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 View Records", "➕ Add Record", "💾 Export Data"])

# View Records
with tab1:
    st.markdown("### Your Medical Records")
    
    if st.session_state.user['role'] == 'admin':
        records = get_all_patient_history()
        st.info("📊 Showing all patient records (Admin View)")
    else:
        records = get_patient_history(st.session_state.user['user_id'])
    
    if records:
        df_data = []
        for record in records:
            df_data.append({
                'ID': record[0],
                'Name': record[2],
                'Age': record[3],
                'Gender': record[4],
                'Disease': record[5],
                'Date': record[9],
                'Status': record[13]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No medical records found")

# Add Record
with tab2:
    st.markdown("### Add Medical Record")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Patient Name")
        age = st.number_input("📅 Age", min_value=1, max_value=150)
        gender = st.selectbox("👥 Gender", ["Male", "Female", "Other"])
        disease = st.text_input("🏥 Disease/Condition")
    
    with col2:
        symptoms = st.text_area("🔍 Symptoms")
        severity = st.selectbox("⚠️ Severity", ["Mild", "Moderate", "Severe"])
        height = st.number_input("📏 Height (cm)", min_value=50, max_value=250)
        weight = st.number_input("⚖️ Weight (kg)", min_value=10, max_value=200)
    
    col3, col4 = st.columns(2)
    
    with col3:
        smoking = st.selectbox("🚬 Smoking Status", ["Never", "Former", "Current"])
        exercise = st.selectbox("🏃 Exercise Level", ["Sedentary", "Light", "Moderate", "Vigorous"])
    
    with col4:
        treatment = st.text_input("💊 Treatment Given")
        medicine = st.text_input("💉 Medicine Prescribed")
    
    col5, col6 = st.columns(2)
    
    with col5:
        cost = st.number_input("💰 Treatment Cost", min_value=0.0)
        insurance = st.text_input("🛡️ Insurance Used")
    
    with col6:
        follow_up = st.date_input("📅 Follow-up Date")
    
    if st.button("💾 Save Record", use_container_width=True):
        bmi = weight / ((height/100) ** 2)
        
        patient_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'disease_name': disease,
            'symptoms': symptoms,
            'severity_level': severity,
            'height_cm': height,
            'weight_kg': weight,
            'BMI': round(bmi, 2),
            'smoking_status': smoking,
            'exercise_level': exercise,
            'treatment_given': treatment,
            'medicine_prescribed': medicine,
            'treatment_cost': cost,
            'insurance_used': insurance,
            'follow_up_date': str(follow_up)
        }
        
        success, message = add_patient_history(st.session_state.user['user_id'], patient_data)
        
        if success:
            st.success("✅ Record saved successfully!")
            st.balloons()
        else:
            st.error(f"❌ Error: {message}")

# Export Data
with tab3:
    st.markdown("### Export Records")
    
    if st.session_state.user['role'] == 'admin':
        records = get_all_patient_history()
    else:
        records = get_patient_history(st.session_state.user['user_id'])
    
    if records:
        df_data = []
        for record in records:
            df_data.append({
                'Patient ID': record[0],
                'Name': record[2],
                'Age': record[3],
                'Gender': record[4],
                'Disease': record[5],
                'Symptoms': record[6],
                'Severity': record[7],
                'Height': record[15],
                'Weight': record[16],
                'BMI': record[17],
                'Treatment': record[20],
                'Medicine': record[21],
                'Cost': record[22],
                'Date': record[9]
            })
        
        df = pd.DataFrame(df_data)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="patient_records.csv",
            mime="text/csv"
        )
        
        st.info("✅ Data ready to export in CSV format")
    else:
        st.info("No records to export")

st.markdown("---")
st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
