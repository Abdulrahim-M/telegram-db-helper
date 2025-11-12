import sqlite3
from config import DB_PATH

def connect_db():
    return sqlite3.connect(DB_PATH)

def search_item(query: str):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT name, index_id, unId, email, phone, address
            FROM students
            WHERE name LIKE ? OR index_id LIKE ? OR phone LIKE ? OR unId LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        return c.fetchall()

def all_items():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT name, index_id, unId, email, phone, address FROM students")
        return [list(r) for r in c.fetchall()]