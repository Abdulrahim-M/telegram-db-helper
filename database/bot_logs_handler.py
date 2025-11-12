from datetime import datetime, timezone
import sqlite3

conn = sqlite3.connect("data/data.db", check_same_thread=False)
cursor = conn.cursor()

async def log_outgoing_message(chat_id, text, msg_type="text"):
    print("logging bot message")
    cursor.execute("""
        INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (chat_id, 0, "BOT", text, msg_type, datetime.now(timezone.utc).isoformat()))
    conn.commit()

