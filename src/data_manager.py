import pandas as pd
import os

class FinanceData:
    def __init__(self):
        self.file_path = "data/expenses.csv"
        # Create the file if it doesn't exist
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
            df.to_csv(self.file_path, index=False)

    def add_expense(self, date, category, amount, description):
        # Load existing data
        df = pd.read_csv(self.file_path)
        # Add new row
        new_row = {"Date": date, "Category": category, "Amount": amount, "Description": description}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        # Save back to CSV
        df.to_csv(self.file_path, index=False)
        return "Expense Added Successfully!"

    def get_summary(self):
        df = pd.read_csv(self.file_path)
        # Use Pandas to group spending by category
        summary = df.groupby("Category")["Amount"].sum()
        return summary