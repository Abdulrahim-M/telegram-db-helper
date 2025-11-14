from datetime import datetime, timezone
from config import DB_PATH
import sqlite3

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

async def log_outgoing_message(chat_id, text, msg_type="text"):
    cursor.execute("""
        INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (chat_id, 0, "BOT", text, msg_type, datetime.now(timezone.utc).isoformat()))
    conn.commit()
