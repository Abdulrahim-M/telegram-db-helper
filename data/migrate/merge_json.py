import json

# Load JSON
with open("data/output1.json", "r", encoding="utf-8") as f:
    data1 = {x["index_id"]: x for x in json.load(f)}

with open("data/output2.json", "r", encoding="utf-8") as f:
    data2 = {x["index_id"]: x for x in json.load(f)}

merged = {}

# Get all index_ids from both files
all_ids = set(data1.keys()) | set(data2.keys())

for idx in all_ids:
    row1 = data1.get(idx, {})
    row2 = data2.get(idx, {})

    merged[idx] = {}

    # For each field in either file
    fields = set(row1.keys()) | set(row2.keys())

    for f in fields:
        v1 = row1.get(f)
        v2 = row2.get(f)

        # Prefer the non-null value
        merged[idx][f] = v1 if v1 not in [None, "", "null"] else v2

# Save output
with open("data/merged.json", "w", encoding="utf-8") as f:
    json.dump(list(merged.values()), f, ensure_ascii=False, indent=4)
