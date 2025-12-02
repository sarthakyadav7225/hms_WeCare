import streamlit as st
from config import set_page_config, apply_custom_styling
from database import create_user, get_user_by_email

set_page_config()
apply_custom_styling()

st.title("🏥 WeCare HMS - Sign Up")
st.markdown("### Create Your Account")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("---")
    
    full_name = st.text_input("👤 Full Name", placeholder="John Doe")
    email = st.text_input("📧 Email Address", placeholder="user@example.com")
    phone = st.text_input("📱 Phone Number (Optional)", placeholder="+91-9876543210")
    password = st.text_input("🔐 Password", type="password", placeholder="At least 6 characters")
    confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Re-enter password")
    
    agree = st.checkbox("I agree to the Terms and Conditions")
    
    col_signup, col_back = st.columns(2)
    
    with col_signup:
        if st.button("📝 Create Account", use_container_width=True):
            # Validation
            if not all([full_name, email, password, confirm_password]):
                st.error("❌ Please fill all required fields")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not agree:
                st.error("❌ Please agree to Terms and Conditions")
            elif get_user_by_email(email):
                st.error("❌ Email already registered")
            else:
                success, message = create_user(email, password, full_name, role='user', phone=phone)
                if success:
                    st.success("✅ Account created successfully!")
                    st.balloons()
                    st.info("👉 Redirecting to login page...")
                    if st.button("🔓 Go to Login"):
                        st.switch_page("pages/01_Login.py")
                else:
                    st.error(f"❌ Error: {message}")
    
    with col_back:
        if st.button("⬅️ Back to Login", use_container_width=True):
            st.switch_page("pages/01_Login.py")
    
    st.markdown("---")
    st.markdown("**Already have an account?** [Login here](/?page=login)")
