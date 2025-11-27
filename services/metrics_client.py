# services/metrics_client.py
from __future__ import annotations
import os, json, requests, streamlit as st

N8N_URL = os.getenv("N8N_WEBHOOK_URL", "https://primary-production-b8a0.up.railway.app/webhook-test/assistant-webhook")

class MetricsError(RuntimeError): ...

def _post(payload: dict, timeout: int=30) -> dict:
    r = requests.post(N8N_URL, json=payload, headers={"Accept":"application/json"}, timeout=timeout)
    if r.status_code >= 400:
        raise MetricsError(f"HTTP {r.status_code}: {r.text[:240]}")
    try:
        return r.json()
    except json.JSONDecodeError:
        raise MetricsError(f"Non-JSON response: {r.text[:240]}")

@st.cache_data(show_spinner=False, ttl=300)
def get_metrics_cached(session_id: str, date_from: str|None=None, date_to: str|None=None) -> dict:
    payload = {"action":"get_metrics", "session_id": session_id}
    if date_from: payload["date_from"] = date_from
    if date_to:   payload["date_to"]   = date_to
    return _post(payload)