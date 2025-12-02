import streamlit as st
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info
from database import get_appointments

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title(f"👋 Welcome, {st.session_state.user['full_name']}!")

# Sidebar
with st.sidebar:
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.success("Logged out successfully!")
        st.switch_page("pages/01_Login.py")

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📋 Total Visits", "5", "+2 this month")

with col2:
    st.metric("📅 Appointments", "2", "Upcoming")

with col3:
    st.metric("⭐ Health Score", "85%", "+5%")

st.markdown("---")
st.markdown("### 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏥 Free Diagnosis Clinic", use_container_width=True):
        st.switch_page("pages/08_Free_Diagnosis.py")

with col2:
    if st.button("🎪 Waiting Room", use_container_width=True):
        st.switch_page("pages/09_Waiting_Room.py")

with col3:
    if st.button("📋 Patient History", use_container_width=True):
        st.switch_page("pages/06_Patient_History.py")

st.markdown("---")
st.markdown("### 📅 Your Appointments")

appointments = get_appointments(st.session_state.user['user_id'])

if appointments:
    for apt in appointments[:5]:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📅 **{apt[2]}** at **{apt[3]}**")
                st.caption(f"Status: {apt[4]}")
            with col2:
                if apt[4] == 'pending':
                    st.warning("Pending")
                else:
                    st.success("Completed")
else:
    st.info("No appointments scheduled yet")

st.markdown("---")
st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
