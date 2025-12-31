import customtkinter as ctk
import pandas as pd

class HistoryTable(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv("data/expenses.csv").tail(15) # Show last 15
            # Headers
            headers = ["Date", "Category", "Amount"]
            for col, text in enumerate(headers):
                lbl = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(weight="bold"))
                lbl.grid(row=0, column=col, padx=20, pady=5)

            # Rows
            for i, row in df.iterrows():
                ctk.CTkLabel(self, text=row['Date']).grid(row=i+1, column=0, padx=20)
                ctk.CTkLabel(self, text=row['Category']).grid(row=i+1, column=1, padx=20)
                ctk.CTkLabel(self, text=f"N{row['Amount']}").grid(row=i+1, column=2, padx=20)
        except:
            ctk.CTkLabel(self, text="No data found").pack()