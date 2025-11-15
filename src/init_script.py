import sqlite3
import json
import os

def create_config():
    bot_token = input('Enter your telegram bot token: ')

    default_data = {
        "DB_PATH": "data/data.db",
        "BOT_TOKEN": bot_token,
        "DB_HOST": "",
        "DB_USER": "",
        "DB_PASSWORD": "",
        "DB_NAME": "",
        "USED_DB": ""
    }

    with open("src/config.json", "w") as f:
        json.dump(default_data, f, indent=4)

    print("Config file created: config.json")

    laod_database()


def laod_database():
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
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
