import json
import pandas as pd
from sqlalchemy import create_engine, text

# --- SQLITE CONNECTION ---
engine = create_engine("sqlite:///data/data.db")   # change file path as needed

# --- LOAD JSON ---
with open("data/incom.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Ensure all required columns exist
required_cols = ["index_id", "name", "unId", "email", "phone", "address"]
for col in required_cols:
    if col not in df.columns:
        df[col] = None

# Convert index_id to string always (SQLite stores as TEXT automatically)
df["index_id"] = df["index_id"].astype(str).str.strip()

# Make sure df has exact column order (optional but clean)
df = df[required_cols]

# Replace NaN with None (SQLite uses NULL)
df = df.where(pd.notnull(df), None)

# --- REPLACE TABLE CONTENT ---
with engine.begin() as conn:

    # 1. Clear old data
    conn.execute(text("DELETE FROM students"))

    # 2. Insert fresh data
    insert_sql = """
        INSERT INTO students (index_id, name, unId, email, phone, address)
        VALUES (:index_id, :name, :unId, :email, :phone, :address)
    """

    for _, row in df.iterrows():
        conn.execute(text(insert_sql), row.to_dict())

print("SQLite table 'students' has been fully replaced with JSON data.")
