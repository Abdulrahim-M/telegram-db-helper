import arabic_reshaper
from bidi.algorithm import get_display
import io
import csv
import pandas as pd
from fpdf import FPDF
from database.db import all_items

def export_xlsx():
    output = io.BytesIO()
    df = pd.DataFrame(all_items(), columns=["Name", "ID", "unId", "Email", "Phone", "Address"])
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    return output

def export_csv():
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Name", "ID", "unId", "Email", "Phone", "Address"])
    writer.writerows(all_items())
    buffer.seek(0)
    return io.BytesIO(buffer.getvalue().encode('utf-8'))  # Telegram wants bytes

def export_txt():
    buffer = io.StringIO()
    for r in all_items():
        buffer.write(f"Name: {r[0]}\nID: {r[1]}\nunId: {r[2]}\nEmail: {r[3]}\nPhone: {r[4]}\nAddress: {r[5]}\n")
        buffer.write("-" * 40 + "\n")
    buffer.seek(0)
    return io.BytesIO(buffer.getvalue().encode('utf-8'))

def export_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Load Unicode font
    pdf.add_font("DejaVuSans", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVuSans", size=10)

    # Table headers
    headers = ["Name", "Index", "unId", "Email", "Phone", "Address"]
    col_widths = [30, 20, 25, 40, 25, 50]  # adjust widths as needed

    # Draw headers
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, ln=0, align='C')
    pdf.ln()

    # Draw rows
    for row in all_items():
        for i, item in enumerate(row):
            text = str(item)

            # Shape Arabic if needed
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)

            pdf.cell(col_widths[i], 8, bidi_text, border=1, ln=0, align='R')  # align right
        pdf.ln()

    # Output as bytes
    pdf_bytes = pdf.output(dest="S")
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer