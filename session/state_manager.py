# session/state_manager.py
import uuid
import streamlit as st

def init_session_state():
    st.session_state.setdefault("session_id", str(uuid.uuid4()))
    st.session_state.setdefault("role_id", "user")
    st.session_state.setdefault("extra_context", "")
    st.session_state.setdefault("history", [])  # [{role: 'user'|'assistant', content: str}]
    st.session_state.setdefault("is_waiting_response", False)

def add_message(role: str, content: str):
    st.session_state["history"].append({"role": role, "content": content})

def get_history():
    return st.session_state.get("history", [])

def clear_history():
    st.session_state["history"] = []