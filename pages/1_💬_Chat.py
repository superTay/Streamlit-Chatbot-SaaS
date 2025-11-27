# pages/1_💬_Chat.py
import streamlit as st
from session.state_manager import init_session_state, add_message, get_history
from ui.layout import inject_theme_css
from services.n8n_client import send_message_to_n8n
from services.stream_utils import stream_text

inject_theme_css()
init_session_state()

st.title("💬 Chat")

with st.sidebar:
    st.subheader("Persona & Tone")
    st.selectbox("Role", ["user","admin"], index=0, key="role_id")
    st.text_area("Extra context / tone", key="extra_context", height=120)

history = get_history()
for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Write your message…")
if prompt:
    add_message("user", prompt)
    with st.chat_message("user"): st.markdown(prompt)
    st.session_state["is_waiting_response"] = True
    try:
        with st.chat_message("assistant"):
            ans = send_message_to_n8n(
                prompt=prompt,
                session_id=st.session_state["session_id"],
                role_id=st.session_state.get("role_id"),
                extra_context=st.session_state.get("extra_context"),
            )
            full = "".join(stream_text(ans))
            st.markdown(full)
        add_message("assistant", ans)
    except Exception as e:
        st.error(f"❌ Error talking to backend: {e}")
    finally:
        st.session_state["is_waiting_response"] = False