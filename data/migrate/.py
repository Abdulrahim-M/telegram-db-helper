import json
import pandas as pd
from sqlalchemy import create_engine, text

# --- DB CONNECTION ---
engine = create_engine("mysql+mysqlconnector://admin:8VZbbc4engICZE@150.230.52.62:3306/telebot")

# --- READ JSON ---
with open("merged.json", "r", encoding="utf-8") as f:
    df_json = pd.DataFrame(json.load(f))

# Rename key if needed (your JSON uses "index", so convert it)
df_json = df_json.rename(columns={"index": "index_id"})

# Ensure missing columns exist
for col in ["name", "unId", "email", "phone", "address"]:
    if col not in df_json.columns:
        df_json[col] = None

# --- FETCH EXISTING ROWS FROM DB ---
with engine.connect() as conn:
    df_db = pd.read_sql("SELECT * FROM students", conn)

print(df_db["index_id"].dtype)
print(df_json["index_id"].dtype)

df_db["index_id"] = df_db["index_id"].astype(str)
df_json["index_id"] = df_json["index_id"].astype(str)

# --- MERGE DB + JSON ON index_id ---
merged = df_db.merge(df_json, on="index_id", how="left", suffixes=('_db', '_json'))


# --- FUNCTION TO FILL MISSING DB VALUES FROM JSON ---
def fill_missing(row, col):
    db_val = row[f"{col}_db"]
    json_val = row[f"{col}_json"]

    if pd.isna(db_val) or db_val == "" or db_val is None:
        return json_val  # take JSON value
    return db_val        # keep DB value


# --- APPLY MERGING LOGIC ---
final = pd.DataFrame()
final["index_id"] = merged["index_id"]

cols = ["name", "unId", "email", "phone", "address"]

for col in cols:
    final[col] = merged.apply(lambda row: fill_missing(row, col), axis=1)

# Replace NaN → None
final = final.where(pd.notnull(final), None)

# --- SQL UPDATE TEMPLATE ---
update_sql = """
UPDATE students
SET name = :name,
    unId = :unId,
    email = :email,
    phone = :phone,
    address = :address
WHERE index_id = :index_id
"""

# --- APPLY UPDATES ---
with engine.begin() as conn:
    for _, row in final.iterrows():
        conn.execute(text(update_sql), row.to_dict())

print("Database updated successfully from JSON.")
