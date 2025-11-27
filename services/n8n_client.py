# services/n8n_client.py
from __future__ import annotations
import os, json, requests

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://primary-production-b8a0.up.railway.app/webhook/mvp-streamlit-chatbot",
)

class N8NBackendError(RuntimeError): ...

def _extract_answer(data: dict) -> str:
    for k in ("answer", "output", "text", "result"):  # tolerante
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            return v
    body = data.get("body") if isinstance(data, dict) else None
    if isinstance(body, dict):
        for k in ("answer", "output", "text"):
            if body.get(k):
                return str(body[k])
    return ""

def send_message_to_n8n(*, prompt: str, session_id: str, role_id: str|None=None, extra_context: str|None=None, timeout: int = 40) -> str:
    payload = {"action": "send_message", "message": prompt, "session_id": session_id}
    if role_id: payload["role_id"] = role_id
    if extra_context: payload["extra_context"] = extra_context
    try:
        resp = requests.post(N8N_WEBHOOK_URL, json=payload, headers={"Accept":"application/json"}, timeout=timeout)
    except requests.RequestException as e:
        raise N8NBackendError(f"Network error: {e}") from e
    if resp.status_code >= 400:
        raise N8NBackendError(f"HTTP {resp.status_code}: {resp.text[:200]}")
    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise N8NBackendError(f"Non-JSON response: {resp.text[:200]}")
    ans = _extract_answer(data)
    if not ans:
        raise N8NBackendError(f"Missing 'answer' in response. Keys: {list(data.keys())}")
    return ans