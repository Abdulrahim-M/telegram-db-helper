from datetime import datetime, timezone
import sqlite3
from services.db import BaseDB
from config import DB_PATH

class SQLiteDB(BaseDB):
    def __init__(self, db_file=DB_PATH):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row

    def execute(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        self.conn.commit()

    def query(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        return [dict(row) for row in cur.fetchall()]

    def search_item(self, query: str):
        c = self.conn.cursor()
        c.execute("""
            SELECT name, index_id, unId, email, phone, address
            FROM students
            WHERE name LIKE ? OR index_id LIKE ? OR phone LIKE ? OR unId LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        return QueryResult(c.fetchall())

    def all_items(self):
        c = self.conn.cursor()
        c.execute("SELECT name, index_id, unId, email, phone, address FROM students")
        return QueryResult(c.fetchall())

    async def log_bot_message(self, chat_id, text, msg_type="text"):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (chat_id, 0, "BOT", text, msg_type, datetime.now(timezone.utc).isoformat()))
        self.conn.commit()

    def log_user_message(self, chat_id, user_id, username, message_content, msg_type, reply_to, forwarded_from):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp, reply_to, forwarded_from)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chat_id,
                user_id,
                username,
                message_content,
                msg_type,
                datetime.now(timezone.utc).isoformat(),
                reply_to,
                forwarded_from,
            ))
        self.conn.commit()

class QueryResult:
    def __init__(self, rows):
        self.rows = rows

    def as_list(self):
        return self.rows

    def as_dict(self):
        keys = ["name", "index_id", "unId", "email", "phone", "address"]
        return [dict(zip(keys, row)) for row in self.rows]
