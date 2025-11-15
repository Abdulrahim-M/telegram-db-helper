from datetime import datetime, timezone
import pymysql
from services.db import BaseDB
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class MariaDB(BaseDB):
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
        self.conn.commit()

    def query(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

    def search_item(self, query: str):
        return QueryResult(self.query("""
            SELECT * FROM students
            WHERE name LIKE %s OR index_id LIKE %s OR phone LIKE %s OR unId LIKE %s
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")))

    def all_items(self):
        return QueryResult(self.query("SELECT * FROM students"))

    def update_row(self, data: dict, where: dict):
        set_clause = ", ".join(f"{col}=%s" for col in data.keys())
        where_clause = " AND ".join(f"{col}=%s" for col in where.keys())

        sql = f"UPDATE students SET {set_clause} WHERE {where_clause}"
        params = list(data.values()) + list(where.values())

        self.execute(sql, params)


    async def log_bot_message(self, chat_id, text, msg_type="text"):
        print(chat_id, text, msg_type)
        self.execute("""
            INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (chat_id, 0, "BOT", text, msg_type, datetime.now(timezone.utc).isoformat()))

    def log_user_message(self, chat_id, user_id, username, message_content, msg_type, reply_to, forwarded_from):
        self.execute("""
            INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp, reply_to, forwarded_from)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

class QueryResult:
    def __init__(self, rows):
        self.rows = rows

    def as_list(self):
        return [list(r.values()) for r in self.rows]

    def as_dict(self):
        return self.rows
