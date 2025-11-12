import csv
import re

# Input and output files
input_file = 'data/data.txt'
output_file = 'data/output.csv'

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

# Write CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Header
    writer.writerow(['name', 'index', 'unId', 'email', 'phone'])
    # Data
    for entry in entries:
        writer.writerow(entry)

print(f"CSV file saved as {output_file}")
