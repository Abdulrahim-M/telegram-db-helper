import re
import json

# Input and output files
input_file = 'data/data.txt'
output_file = 'data/output1.json'

# Pattern to match each entry
pattern = re.compile(
    r"\d+\.\s*الاسم كامل رباعي:\s*(.*?)\s*"
    r"رقم الجلوس:\s*(.*?)\s*"
    r"الرقم الجامعي:\s*(.*?)\s*"
    r"الايميل \(Active\):\s*(.*?)\s*"
    r"رقم الهاتف المستخدم:\s*(.*?)\s*(?=\d+\.|$)",
    re.DOTALL
)

# Read the text file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all matches
entries = pattern.findall(content)

# Build list of dictionaries
data = []
for i, entry in enumerate(entries, start=1):
    data.append({
        "id": i,              # auto-generated ID
        "name": entry[0].strip(),
        "index_id": entry[1].strip(),
        "unId": entry[2].strip(),
        "email": entry[3].strip(),
        "phone": entry[4].strip(),
        "address": None
    })

# Write JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"JSON file saved as {output_file}")
