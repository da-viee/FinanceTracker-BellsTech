import customtkinter as ctk
from src.database import FinanceDB
from src.visuals import create_pie_chart
from src.history_table import HistoryTable
from src.predictor import predict_next_month
from src.report_gen import export_to_pdf
from datetime import datetime
from tkinter import messagebox

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize Database
        self.db = FinanceDB()

        # Window Configuration
        self.title("Bells Tech Finance Tracker Pro")
        self.geometry("1100x650")

        # Layout Configuration (The Root Window uses Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # We use .pack() for EVERYTHING inside the sidebar to stay consistent
        self.logo = ctk.CTkLabel(self.sidebar, text="FINANCE PRO", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=30, padx=20)

        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.btn_dash.pack(pady=10, padx=20)

        self.btn_add = ctk.CTkButton(self.sidebar, text="Add Expense", command=self.show_add_expense)
        self.btn_add.pack(pady=10, padx=20)

        self.btn_hist = ctk.CTkButton(self.sidebar, text="History", command=self.show_history)
        self.btn_hist.pack(pady=10, padx=20)

        self.btn_pred = ctk.CTkButton(self.sidebar, text="AI Predictor", fg_color="#6c5ce7", command=self.show_prediction)
        self.btn_pred.pack(pady=10, padx=20)

        self.btn_set = ctk.CTkButton(self.sidebar, text="Budget & Reports", command=self.show_budget)
        self.btn_set.pack(pady=10, padx=20)

        self.label_version = ctk.CTkLabel(self.sidebar, text="v1.0.0 - ICT323", text_color="gray")
        self.label_version.pack(side="bottom", pady=20)

        # --- MAIN VIEW ---
        self.main_view = ctk.CTkFrame(self, corner_radius=15)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.show_dashboard()

    def clear_view(self):
        """Cleans the main view before loading a new page"""
        for widget in self.main_view.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_view()
        ctk.CTkLabel(self.main_view, text="Financial Analytics", font=("Arial", 26, "bold")).pack(pady=20)
        
        chart = create_pie_chart(self.main_view)
        if chart:
            chart.pack(fill="both", expand=True, padx=20, pady=20)
        else:
            ctk.CTkLabel(self.main_view, text="Welcome! Start by adding your first expense.").pack(pady=100)

    def show_add_expense(self):
        self.clear_view()
        ctk.CTkLabel(self.main_view, text="New Transaction", font=("Arial", 24)).pack(pady=20)

        # Entry Fields
        self.entry_amount = ctk.CTkEntry(self.main_view, placeholder_text="Amount (e.g., 5000)", width=300)
        self.entry_amount.pack(pady=10)

        self.category_opt = ctk.CTkOptionMenu(self.main_view, width=300,
                                             values=["Food", "Rent", "Transport", "Shopping", "Health", "Utilities", "Education", "Gifts", "Entertainment"])
        self.category_opt.pack(pady=10)

        self.entry_desc = ctk.CTkEntry(self.main_view, placeholder_text="Description (e.g., Dinner)", width=300)
        self.entry_desc.pack(pady=10)

        ctk.CTkButton(self.main_view, text="Save Transaction", fg_color="green", width=200, height=40,
                      command=self.save_data).pack(pady=30)

    def save_data(self):
        amt = self.entry_amount.get()
        if not amt.replace('.','',1).isdigit():
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return

        success = self.db.add_record(
            datetime.now().strftime("%Y-%m-%d"),
            self.category_opt.get(),
            amt,
            self.entry_desc.get()
        )
        if success:
            messagebox.showinfo("Success", "Expense Recorded!")
            self.show_dashboard()

    def show_history(self):
        self.clear_view()
        ctk.CTkLabel(self.main_view, text="Recent Transactions", font=("Arial", 24)).pack(pady=20)
        table = HistoryTable(self.main_view)
        table.pack(fill="both", expand=True, padx=20, pady=20)

    def show_prediction(self):
        self.clear_view()
        ctk.CTkLabel(self.main_view, text="AI Spending Prediction", font=("Arial", 24)).pack(pady=20)
        
        pred, accuracy = predict_next_month()
        
        card = ctk.CTkFrame(self.main_view, fg_color="#2d3436")
        card.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(card, text=f"Predicted Daily Spend: N{pred}", font=("Arial", 20)).pack(pady=15)
        ctk.CTkLabel(card, text=f"Statistical Confidence: {accuracy * 100}%", text_color="#00b894").pack(pady=5)
        ctk.CTkLabel(self.main_view, text="Note: Based on Linear Regression of your data trends.", font=("Arial", 10)).pack(pady=20)

    def show_budget(self):
        self.clear_view()
        ctk.CTkLabel(self.main_view, text="Budget & PDF Reports", font=("Arial", 24)).pack(pady=20)
        
        # Budget Section
        curr = self.db.get_budget()
        ctk.CTkLabel(self.main_view, text=f"Current Monthly Limit: N{curr}", font=("Arial", 16)).pack(pady=10)
        
        self.budget_entry = ctk.CTkEntry(self.main_view, placeholder_text="New Limit")
        self.budget_entry.pack(pady=5)
        
        ctk.CTkButton(self.main_view, text="Update Budget", command=self.update_budget_logic).pack(pady=10)
        
        # Report Section
        ctk.CTkLabel(self.main_view, text="---", text_color="gray").pack(pady=20)
        ctk.CTkButton(self.main_view, text="Download PDF Report", fg_color="#d63031", 
                      command=self.run_report).pack(pady=10)

    def update_budget_logic(self):
        val = self.budget_entry.get()
        if val.isdigit():
            self.db.set_budget(val)
            self.show_budget()
            messagebox.showinfo("Success", "Budget Updated!")

    def run_report(self):
        if export_to_pdf():
            messagebox.showinfo("Success", "PDF Saved in docs/Finance_Report.pdf")
        else:
            messagebox.showerror("Error", "Could not generate PDF.")

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()