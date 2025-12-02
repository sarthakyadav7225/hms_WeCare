import streamlit as st
from config import set_page_config, apply_custom_styling
from database import verify_password, get_user_by_email

set_page_config()
apply_custom_styling()

st.title("🏥 WeCare HMS - Login")
st.markdown("### Welcome to Healthcare Management System")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("---")
    
    email = st.text_input("📧 Email Address", placeholder="user@example.com")
    password = st.text_input("🔐 Password", type="password", placeholder="Enter your password")
    
    col_login, col_signup = st.columns(2)
    
    with col_login:
        if st.button("🔓 Login", use_container_width=True):
            if email and password:
                if verify_password(email, password):
                    user = get_user_by_email(email)
                    st.session_state.user = user
                    st.success("✅ Login successful!")
                    st.balloons()
                    if user['role'] == 'admin':
                        st.switch_page("pages/05_Admin_Dashboard.py")
                    else:
                        st.switch_page("pages/04_User_Dashboard.py")
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.warning("⚠️ Please enter email and password")
    
    with col_signup:
        if st.button("📝 Create Account", use_container_width=True):
            st.switch_page("pages/02_Signup.py")
    
    st.markdown("---")
    
    with st.expander("🆘 Forgot Password?"):
        st.markdown("Click the button below to reset your password")
        if st.button("🔑 Reset Password", use_container_width=True):
            st.switch_page("pages/03_Forgot_Password.py")
    
    st.markdown("---")
    st.markdown("### 📝 Demo Accounts")
    
    col_admin, col_user = st.columns(2)
    
    with col_admin:
        st.markdown("**Admin Account:**")
        st.code("Email: admin@wecare.com\nPassword: admin123", language="text")
    
    with col_user:
        st.markdown("**User Account:**")
        st.code("Email: user@wecare.com\nPassword: user123", language="text")
    
    st.markdown("---")
    st.markdown("**Version:** 1.0.0 | **Created:** December 2024")
