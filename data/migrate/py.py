import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

# --- 1. Connect to SQLite ---
sqlite_conn = sqlite3.connect("data.db")

# --- 2. Connect to MariaDB ---
# Format: mysql+mysqlconnector://user:password@host:port/database
mariadb_engine = create_engine(
    "mysql+mysqlconnector://admin:8VZbbc4engICZE@150.230.52.62:3306/telebot"
)

# --- 3. List of tables to migrate ---
tables = ["students", "chat_logs"]

for table in tables:
    # Read SQLite table into DataFrame
    df = pd.read_sql(f"SELECT * FROM {table}", sqlite_conn)

    # Write DataFrame to MariaDB
    # 'replace' will drop table if exists, 'append' adds to existing table
    df.to_sql(table, mariadb_engine, if_exists="replace", index=False)
    print(f"Table '{table}' migrated successfully.")

# --- 4. Recreate indexes for chat_logs if needed ---
# Example: suppose chat_logs had indexes on columns 'user_id' and 'timestamp'
with mariadb_engine.connect() as conn:
    conn.execute(text("CREATE INDEX idx_user ON chat_logs(user_id);"))
    conn.execute(text("CREATE INDEX idx_chat ON chat_logs(chat_id);"))

print("Indexes recreated successfully.")
