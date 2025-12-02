import streamlit as st
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title("🏥 Free Diagnosis Clinic")
st.markdown("### AI-Powered Symptom Analysis (Demo)")

with st.sidebar:
    if st.button("⬅️ Back"):
        st.switch_page("pages/04_User_Dashboard.py")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.switch_page("pages/01_Login.py")

# Disease database
DISEASES_DB = {
    'fever': ['Cold', 'Flu', 'Typhoid', 'Malaria', 'COVID-19'],
    'cough': ['Cold', 'Flu', 'Bronchitis', 'Asthma', 'COVID-19'],
    'headache': ['Migraine', 'Tension Headache', 'Cold', 'Flu'],
    'body pain': ['Flu', 'COVID-19', 'Muscle Strain', 'Arthritis'],
    'runny nose': ['Cold', 'Allergy', 'Flu', 'Sinusitis'],
    'sore throat': ['Cold', 'Flu', 'Strep Throat', 'Pharyngitis'],
    'fatigue': ['Anemia', 'Thyroid', 'Depression', 'Chronic Fatigue'],
    'shortness of breath': ['Asthma', 'Pneumonia', 'Anxiety', 'Heart Disease'],
    'nausea': ['Food Poisoning', 'Gastritis', 'Pregnancy', 'Migraine'],
    'dizziness': ['Vertigo', 'Low Blood Pressure', 'Anemia', 'Dehydration']
}

RECOMMENDATIONS_DB = {
    'Cold': ['Rest', 'Hydration', 'Vitamin C', 'Gargle with salt water'],
    'Flu': ['Rest', 'Fluids', 'Pain reliever', 'Consult doctor if severe'],
    'Migraine': ['Rest in dark room', 'Pain medication', 'Avoid triggers', 'Hydration'],
    'Fever': ['Paracetamol', 'Cold compress', 'Hydration', 'Monitor temperature'],
    'Asthma': ['Inhaler', 'Avoid triggers', 'Exercise regularly', 'Consult specialist'],
    'COVID-19': ['Self-isolate', 'Get tested', 'Monitor symptoms', 'Seek medical help if worsens'],
    'Bronchitis': ['Rest', 'Cough syrup', 'Humidifier', 'See doctor if persistent'],
    'Sore Throat': ['Throat lozenges', 'Warm water gargle', 'Honey tea', 'Avoid smoking'],
}

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔍 Describe Your Symptoms")
    
    symptoms_text = st.text_area(
        "Enter your symptoms (e.g., 'I have fever and cough for 2 days')",
        height=100,
        placeholder="Describe what you're experiencing..."
    )
    
    severity = st.selectbox("⚠️ Severity Level", ["Mild", "Moderate", "Severe", "Very Severe"])
    
    duration = st.text_input("⏱️ Duration", placeholder="e.g., 2 days, 1 week")
    
    st.markdown("---")

with col2:
    st.markdown("### 👤 Patient Info")
    
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    medical_history = st.text_area("Medical History (Optional)", height=80, placeholder="Allergies, chronic diseases, etc.")

# Analyze symptoms
if st.button("🔍 Analyze Symptoms", use_container_width=True):
    if not symptoms_text:
        st.error("❌ Please describe your symptoms")
    else:
        symptoms_lower = symptoms_text.lower()
        
        matched_diseases = set()
        for symptom, diseases in DISEASES_DB.items():
            if symptom in symptoms_lower:
                matched_diseases.update(diseases)
        
        if matched_diseases:
            matched_diseases = list(matched_diseases)[:5]
            
            st.success("✅ Analysis Complete")
            
            st.markdown("---")
            st.markdown("### 📋 Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Confidence", "75%")
            with col2:
                st.metric("⚠️ Severity", severity)
            with col3:
                st.metric("⏱️ Duration", duration if duration else "Not specified")
            
            st.markdown("---")
            st.markdown("### 🏥 Possible Conditions")
            
            for i, disease in enumerate(matched_diseases, 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{i}. {disease}**")
                        
                        if disease in RECOMMENDATIONS_DB:
                            recommendations = RECOMMENDATIONS_DB[disease]
                            st.markdown("**Recommendations:**")
                            for rec in recommendations:
                                st.markdown(f"• {rec}")
                    
                    with col2:
                        if severity in ["Very Severe", "Severe"]:
                            st.error("🚨 Seek immediate medical attention")
                        else:
                            st.info("ℹ️ Consult doctor if symptoms persist")
            
            st.markdown("---")
            st.warning("""
            ⚠️ **Important Disclaimer:**
            - This is a demo AI tool for educational purposes only
            - Not a substitute for professional medical diagnosis
            - Always consult with a licensed healthcare provider
            - If symptoms are severe, seek immediate medical attention
            """)
        else:
            st.info("💡 No specific diseases matched. Please provide more detailed symptoms.")

st.markdown("---")
st.info("""
**Common Symptoms Database:**
- Fever, Cold, Flu
- Cough, Bronchitis, Asthma  
- Headache, Migraine
- Body pain, Arthritis
- Sore throat, Pharyngitis
- Nausea, Food poisoning
- Dizziness, Vertigo
""")

st.markdown("---")
st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
