import streamlit as st
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info
from database import get_all_users, get_all_appointments, get_all_patient_history

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user or st.session_state.user['role'] != 'admin':
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title("👨‍💼 Admin Dashboard")

# Sidebar
with st.sidebar:
    admin_section = st.radio("📊 Navigation", ["Dashboard", "Users", "Appointments", "Patient History", "EDA & Analytics"])
    
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.success("Logged out successfully!")
        st.switch_page("pages/01_Login.py")

# Dashboard
if admin_section == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    users = get_all_users()
    appointments = get_all_appointments()
    
    with col1:
        st.metric("👥 Total Users", len(users) if users else 0)
    with col2:
        st.metric("📅 Appointments", len(appointments) if appointments else 0)
    with col3:
        st.metric("⭐ System Health", "100%")
    with col4:
        st.metric("🔒 Security", "Active")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recent Users**")
        if users:
            for user in users[-5:]:
                st.text(f"• {user[2]} ({user[1]})")
    
    with col2:
        st.markdown("**Recent Appointments**")
        if appointments:
            for apt in appointments[-5:]:
                st.text(f"• {apt[2]} at {apt[3]} - {apt[4]}")

# Users Management
elif admin_section == "Users":
    st.markdown("### 👥 User Management")
    
    users = get_all_users()
    
    if users:
        st.dataframe(
            [[u[0], u[1], u[2], u[3], u[4], u[5]] for u in users],
            columns=["ID", "Email", "Name", "Role", "Phone", "Joined"],
            use_container_width=True
        )
    else:
        st.info("No users found")

# Appointments
elif admin_section == "Appointments":
    st.markdown("### 📅 Appointment Management")
    
    appointments = get_all_appointments()
    
    if appointments:
        st.dataframe(
            [[a[0], a[1], a[2], a[3], a[4], a[5]] for a in appointments],
            columns=["ID", "User ID", "Date", "Time", "Status", "Notes"],
            use_container_width=True
        )
    else:
        st.info("No appointments found")

# Patient History
elif admin_section == "Patient History":
    st.markdown("### 📋 Patient Records")
    
    if st.button("📊 View Patient History", use_container_width=True):
        st.switch_page("pages/06_Patient_History.py")

# EDA & Analytics
elif admin_section == "EDA & Analytics":
    st.markdown("### 📊 Data Analysis & Insights")
    
    if st.button("🔍 Go to EDA & Chatbot", use_container_width=True):
        st.switch_page("pages/07_EDA_Chatbot.py")

st.markdown("---")
st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
