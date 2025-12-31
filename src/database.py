import pandas as pd
import os

class FinanceDB:
    def __init__(self):
        self.file_path = "data/expenses.csv"
        self.budget_path = "data/budget.txt"
        
        # Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Create the expense file if it doesn't exist
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
            df.to_csv(self.file_path, index=False)

    def add_record(self, date, category, amount, description):
        try:
            df = pd.read_csv(self.file_path)
            new_data = {
                "Date": date, 
                "Category": category, 
                "Amount": float(amount), 
                "Description": description
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def get_all_data(self):
        try:
            return pd.read_csv(self.file_path)
        except:
            return pd.DataFrame()

    def set_budget(self, amount):
        try:
            with open(self.budget_path, "w") as f:
                f.write(str(amount))
            return True
        except:
            return False

    def get_budget(self):
        try:
            with open(self.budget_path, "r") as f:
                return float(f.read())
        except:
            return 0.0