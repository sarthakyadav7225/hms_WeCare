import streamlit as st
from config import set_page_config, apply_custom_styling

set_page_config()
apply_custom_styling()

st.title("🏥 WeCare HMS - Reset Password")
st.markdown("### Recover Your Account")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("---")
    
    st.info("📧 Enter your email address and we'll help you reset your password")
    
    email = st.text_input("📧 Email Address", placeholder="user@example.com")
    
    if st.button("🔑 Reset Password", use_container_width=True):
        if email:
            st.success(f"✅ Password reset link sent to {email}")
            st.markdown("""
            **Next steps:**
            1. Check your email inbox
            2. Click the reset link
            3. Set your new password
            4. Login with new password
            """)
            
            if st.button("🔓 Back to Login"):
                st.switch_page("pages/01_Login.py")
        else:
            st.error("❌ Please enter your email address")
    
    st.markdown("---")
    
    col_login, col_signup = st.columns(2)
    
    with col_login:
        if st.button("🔓 Back to Login", use_container_width=True):
            st.switch_page("pages/01_Login.py")
    
    with col_signup:
        if st.button("📝 Create Account", use_container_width=True):
            st.switch_page("pages/02_Signup.py")
