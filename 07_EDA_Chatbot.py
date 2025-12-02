import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info
from database import get_all_patient_history

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user or st.session_state.user['role'] != 'admin':
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title("📊 EDA & Chatbot Analytics")

with st.sidebar:
    if st.button("⬅️ Back"):
        st.switch_page("pages/05_Admin_Dashboard.py")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.switch_page("pages/01_Login.py")

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 EDA Analysis", "💬 Data Chatbot", "📤 Upload Data"])

# EDA Analysis
with tab1:
    st.markdown("### Exploratory Data Analysis")
    
    patient_records = get_all_patient_history()
    
    if patient_records:
        df_data = []
        for record in patient_records:
            df_data.append({
                'Patient ID': record[0],
                'Name': record[2],
                'Age': record[3],
                'Gender': record[4],
                'Disease': record[5],
                'Severity': record[7],
                'BMI': record[17] if record[17] else 0,
                'Treatment Cost': record[22] if record[22] else 0,
                'Date': record[9]
            })
        
        df = pd.DataFrame(df_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Patients", len(df))
        with col2:
            st.metric("💰 Total Cost", f"${df['Treatment Cost'].sum():,.0f}")
        with col3:
            st.metric("📊 Avg Age", f"{df['Age'].mean():.1f} years")
        with col4:
            st.metric("📈 Avg BMI", f"{df['BMI'].mean():.1f}")
        
        st.markdown("---")
        st.markdown("### Data Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Age Distribution**")
            fig_age = px.histogram(df, x='Age', nbins=10, title='Patient Age Distribution')
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            st.markdown("**Gender Distribution**")
            gender_count = df['Gender'].value_counts()
            fig_gender = px.pie(values=gender_count.values, names=gender_count.index, title='Gender Distribution')
            st.plotly_chart(fig_gender, use_container_width=True)
        
        st.markdown("---")
        st.markdown("**Disease Distribution**")
        disease_count = df['Disease'].value_counts().head(10)
        fig_disease = px.bar(x=disease_count.values, y=disease_count.index, orientation='h', title='Top 10 Diseases')
        st.plotly_chart(fig_disease, use_container_width=True)
        
        st.markdown("---")
        st.markdown("**Treatment Cost Analysis**")
        fig_cost = px.scatter(df, x='Age', y='Treatment Cost', color='Severity', title='Treatment Cost vs Age')
        st.plotly_chart(fig_cost, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Data Summary")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data available for analysis")

# Chatbot
with tab2:
    st.markdown("### Data Chatbot")
    
    st.info("💬 Ask questions about patient data")
    
    patient_records = get_all_patient_history()
    
    if patient_records:
        df_data = []
        for record in patient_records:
            df_data.append({
                'Age': record[3],
                'Gender': record[4],
                'Disease': record[5],
                'BMI': record[17] if record[17] else 0,
                'Cost': record[22] if record[22] else 0
            })
        
        df = pd.DataFrame(df_data)
        
        query = st.text_input("🤖 Ask a question:", placeholder="e.g., How many patients have disease X?")
        
        if st.button("💬 Get Answer"):
            if query.lower().find("total") > -1 or query.lower().find("how many") > -1:
                st.success(f"✅ Total patients: **{len(df)}**")
            elif query.lower().find("average age") > -1:
                st.success(f"✅ Average age: **{df['Age'].mean():.1f}** years")
            elif query.lower().find("disease") > -1:
                st.success(f"✅ Top diseases: {df['Disease'].value_counts().head(5).to_dict()}")
            elif query.lower().find("cost") > -1:
                st.success(f"✅ Total treatment cost: **${df['Cost'].sum():,.0f}**")
                st.success(f"✅ Average cost: **${df['Cost'].mean():,.0f}**")
            elif query.lower().find("gender") > -1:
                st.success(f"✅ Gender distribution: {df['Gender'].value_counts().to_dict()}")
            elif query.lower().find("bmi") > -1:
                st.success(f"✅ Average BMI: **{df['BMI'].mean():.1f}**")
            else:
                st.info("💡 Try asking: 'How many patients?', 'What is average age?', 'Show diseases', etc.")
        
        with st.expander("💡 Sample Questions"):
            st.markdown("""
            - How many patients are in the database?
            - What is the average age of patients?
            - What are the most common diseases?
            - What is the average treatment cost?
            - Show gender distribution
            - What is the average BMI?
            """)
    else:
        st.info("No data available for chatbot")

# Upload Data
with tab3:
    st.markdown("### Upload Patient Data")
    
    uploaded_file = st.file_uploader("📤 Upload CSV or Excel file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ File uploaded successfully")
            st.dataframe(df, use_container_width=True)
            
            st.info("📊 Data preview - Ready to analyze")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
