import streamlit as st
from config import set_page_config, apply_custom_styling
from database import init_database

set_page_config()
apply_custom_styling()
init_database()

def main():
    """Main entry point for WeCare HMS"""
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    # If user not logged in, show login page
    if not st.session_state.user:
        st.switch_page("pages/01_Login.py")
    else:
        # Route based on user role
        if st.session_state.user.get('role') == 'admin':
            st.switch_page("pages/05_Admin_Dashboard.py")
        else:
            st.switch_page("pages/04_User_Dashboard.py")

if __name__ == "__main__":
    main()
