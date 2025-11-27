# pages/2_📊_Analytics.py
import streamlit as st
from session.state_manager import init_session_state
from services.metrics_client import get_metrics_cached

init_session_state()
st.title("📊 Analytics")

with st.form("filters"):
    c1, c2, c3 = st.columns([2,2,1])
    with c1:
        date_from = st.date_input("From", value=None)
    with c2:
        date_to   = st.date_input("To", value=None)
    with c3:
        submitted = st.form_submit_button("Fetch")

if st.button("🔁 Refresh metrics"):
    get_metrics_cached.clear()  # invalida caché
    st.toast("Metrics cache cleared")

if submitted:
    with st.spinner("Loading KPIs…"):
        data = get_metrics_cached(
            st.session_state["session_id"],
            str(date_from) if date_from else None,
            str(date_to) if date_to else None,
        )
    kpis = data.get("kpis", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Msgs", kpis.get("messages", 0))
    c2.metric("Tokens in", kpis.get("input_tokens", 0))
    c3.metric("Tokens out", kpis.get("output_tokens", 0))
    c4.metric("RAG %", f"{kpis.get('retrieval_rate', 0):.0%}")

    st.subheader("Recent messages")
    for row in data.get("last_messages", []):
        st.write(f"**{row['role']}**: {row['content']}")