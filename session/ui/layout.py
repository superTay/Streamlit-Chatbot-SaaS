# ui/layout.py
import streamlit as st

def configure_page():
    st.set_page_config(page_title="SaaS Assistant", page_icon="🤖", layout="wide")

def render_sidebar():
    with st.sidebar:
        st.markdown("## Navigation")
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_💬_Chat.py", label="💬 Chat")
        st.page_link("pages/2_📊_Analytics.py", label="📊 Analytics")
        st.page_link("pages/3_📚_Knowledge_Base.py", label="📚 Knowledge Base")
        st.page_link("pages/4_⚙️_Settings.py", label="⚙️ Settings")

def inject_theme_css():
    try:
        with open("assets/theme.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass