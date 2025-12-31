import pandas as pd
import numpy as np
from scipy import stats
import datetime

def predict_next_month():
    try:
        df = pd.read_csv("data/expenses.csv")
        if df.empty or len(df) < 3: # Need at least 3 points to predict
            return 0, 0

        # Convert date to numbers for SciPy
        df['Date'] = pd.to_datetime(df['Date'])
        # Create a numeric column for dates
        df['Date_Ordinal'] = df['Date'].apply(lambda x: x.toordinal())
        
        # Group daily spending
        daily_spent = df.groupby('Date_Ordinal')['Amount'].sum().reset_index()
        
        x = daily_spent['Date_Ordinal']
        y = daily_spent['Amount']

        # SciPy Linear Regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Predict for 30 days in the future
        future_day = x.max() + 30
        prediction = intercept + slope * future_day
        
        return round(max(0, prediction), 2), round(abs(r_value), 2)
    except Exception as e:
        print(f"Prediction error: {e}")
        return 0, 0