from fpdf import FPDF
import pandas as pd
from datetime import datetime

def export_to_pdf():
    try:
        df = pd.read_csv("data/expenses.csv")
        total = df["Amount"].sum()
        
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Bells Tech Finance - Spending Report", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)

        # Table Header
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Date", 1, 0, 'C', True)
        pdf.cell(50, 10, "Category", 1, 0, 'C', True)
        pdf.cell(40, 10, "Amount", 1, 1, 'C', True)

        # Data Rows
        pdf.set_font("Arial", size=12)
        for i, row in df.tail(20).iterrows(): # Last 20 items
            pdf.cell(40, 10, str(row['Date']), 1)
            pdf.cell(50, 10, str(row['Category']), 1)
            pdf.cell(40, 10, f"N{row['Amount']}", 1, 1)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"TOTAL EXPENDITURE: N{total}", ln=True)
        
        pdf.output("docs/Finance_Report.pdf")
        return True
    except Exception as e:
        print(f"PDF Error: {e}")
        return False