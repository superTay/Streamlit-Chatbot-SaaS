# services/stream_utils.py
from typing import Iterator

def stream_text(text: str, chunk: int = 40) -> Iterator[str]:
    """Divide el texto en trozos para simular streaming en UI."""
    if not text:
        return
    for i in range(0, len(text), chunk):
        yield text[i:i+chunk]