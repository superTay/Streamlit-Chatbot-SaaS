# pages/3_📚_Knowledge_Base.py
import os, requests, streamlit as st
from session.state_manager import init_session_state

init_session_state()
st.title("📚 Knowledge Base")

mode = os.getenv("KB_UPLOAD_MODE", "form").lower()
if mode == "form":
    form_url = os.getenv("KB_FORM_URL", "")
    if form_url:
        st.info("La subida de KB se realiza mediante un formulario externo de n8n.")
        st.link_button("Abrir Formulario de Ingesta", form_url, use_container_width=True)
    else:
        st.warning("Configura KB_FORM_URL en tu .env para usar el modo 'form'.")