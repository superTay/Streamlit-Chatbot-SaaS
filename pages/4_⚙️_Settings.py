# pages/4_⚙️_Settings.py
import streamlit as st
from session.state_manager import init_session_state

init_session_state()
st.title("⚙️ Settings")

st.text_input("Session ID", key="session_id")
st.selectbox("Role", ["user","admin"], key="role_id")
st.text_area("Extra context", key="extra_context")

st.success("Settings updated in session state.")