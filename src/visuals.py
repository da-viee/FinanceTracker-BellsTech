import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

def create_pie_chart(parent_frame):
    # 1. Load data
    try:
        df = pd.read_csv("data/expenses.csv")
    except:
        return None

    if df.empty:
        return None

    # 2. Process data with Pandas & NumPy (Requirement Check!)
    # Group by category and sum the amounts
    category_data = df.groupby("Category")["Amount"].sum()
    labels = category_data.index.tolist()
    sizes = category_data.values.tolist()
    
    # Use NumPy to calculate total for a label
    total_spent = np.sum(sizes)

    # 3. Create the Matplotlib Figure
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    fig.set_facecolor('#2b2b2b') # Matches Dark Mode background
    
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
           colors=colors, textprops={'color':"w"})
    ax.set_title(f"Total Spending: {total_spent:.2f}", color="white")

    # 4. Convert Matplotlib figure to a Tkinter widget
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    return canvas.get_tk_widget()