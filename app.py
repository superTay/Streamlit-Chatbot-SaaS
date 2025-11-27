# app.py
import os, streamlit as st
from config.settings import APP_TITLE, APP_ICON
from ui.layout import configure_page, render_sidebar, inject_theme_css
from session.state_manager import init_session_state
from services.n8n_client import send_message_to_n8n

configure_page()
inject_theme_css()
init_session_state()
render_sidebar()

st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("Home • Usa la barra lateral para navegar (Chat, Analytics, KB, Settings)")

col1, col2 = st.columns([1,1])
with col1:
    if st.button("🔌 Test backend", use_container_width=True):
        try:
            ans = send_message_to_n8n(prompt="ping", session_id=st.session_state["session_id"])
            st.success(f"Backend OK → {ans[:120]}…")
        except Exception as e:
            st.error(f"Backend FAIL: {e}")

with col2:
    if st.button("🧹 Clear session", use_container_width=True):
        for k in ("history", "is_waiting_response"):
            if k in st.session_state: del st.session_state[k]
        st.toast("Session cleared")