import sqlite3

def laod_database():
    conn = sqlite3.connect("data/data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        index_id TEXT,
        unId TEXT,
        email TEXT,
        phone TEXT,
        address TEXT 
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        user_id INTEGER,
        username TEXT,
        message TEXT,
        type TEXT DEFAULT 'text',
        timestamp TEXT,
        reply_to INTEGER,
        forwarded_from INTEGER
    )
    """)

    c.execute("CREATE INDEX IF NOT EXISTS idx_user ON chat_logs(user_id)")

    c.execute("CREATE INDEX IF NOT EXISTS idx_chat ON chat_logs(chat_id)")

    conn.commit()
    conn.close()
