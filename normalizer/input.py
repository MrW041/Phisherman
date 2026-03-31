import time
import uuid
import os
from datetime import datetime

LOG_DIR = "logs"

def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def _log_user_input(user_id, raw_text):
    _ensure_log_dir()

    log_file = os.path.join(LOG_DIR, f"{user_id}.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {raw_text}\n")

def ingest_input(raw_text, user_id, source="unknown"):
    """
    Layer 0: Input Ingestion + Logging
    """

    if not isinstance(raw_text, str):
        raise TypeError("Input must be a string")

    if not user_id:
        raise ValueError("user_id is required")

    # Log BEFORE any processing
    _log_user_input(user_id, raw_text)

    message = {
        "message_id": str(uuid.uuid4()),
        "user_id": user_id,
        "timestamp": time.time(),
        "source": source,
        "raw_text": raw_text,
        "history":[],
        "urls":{}
    }

    return message

ingest_input(
    "Click HERE to verify your account!!! http://.com  ",
    user_id="user_121"
)
