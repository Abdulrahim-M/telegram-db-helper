# import_data.py
import pandas as pd
import sqlite3

# Load your spreadsheet
# If it's an Excel file:
# df = pd.read_excel("data/data.xlsx")
# If it's a CSV file:
df = pd.read_csv("data/output.csv")

# Create the database
conn = sqlite3.connect("data/data.db")
c = conn.cursor()

# Create table with your schema
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

# Note: renamed second "id" to "id_code" since SQLite can't have two "id" columns.

# Insert data
for _, row in df.iterrows():
    c.execute("""
    INSERT INTO students (name, index_id, unId, email, phone)
    VALUES (?, ?, ?, ?, ?)
    """, (row['name'], row['index'], row['unId'], row['email'], row['phone']))

conn.commit()
conn.close()
print("Data imported successfully.")
