import streamlit as st

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="WeCare HMS 🏥",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "WeCare - Healthcare Management System v1.0.0"
        }
    )

def apply_custom_styling():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        :root {
            --primary-color: #3b82f6;
            --success-color: #10b981;
            --danger-color: #ef4444;
            --warning-color: #f59e0b;
            --info-color: #06b6d4;
        }
        
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        body {
            background-color: #f8fafc;
            color: #1e293b;
        }
        
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #2563eb;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .success-box {
            background-color: #ecfdf5;
            border-left: 4px solid var(--success-color);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .error-box {
            background-color: #fef2f2;
            border-left: 4px solid var(--danger-color);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .info-box {
            background-color: #f0f9ff;
            border-left: 4px solid var(--info-color);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin: 16px 0;
        }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    """Display application header"""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🏥 WeCare HMS")
        st.markdown("**Complete Healthcare Management System**")
    with col2:
        st.markdown("### Version 1.0.0")

def show_sidebar_user_info(user):
    """Display user info in sidebar"""
    if user:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"**👤 User:** {user.get('full_name', 'User')}")
            st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
            st.markdown(f"**🔑 Role:** {user.get('role', 'user').upper()}")
            st.markdown("---")
