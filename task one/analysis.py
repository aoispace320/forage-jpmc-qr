import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# data load
df = pd.read_csv("Nat_Gas.csv")
df['Dates'] = pd.to_datetime(df['Dates'])
df = df.sort_values('Dates').reset_index(drop=True)

# time index (t=0,1,2,...)
df['t'] = np.arange(len(df))

# sin,cos feature
df['sin'] = np.sin(2 * np.pi * df['t'] / 12)
df['cos'] = np.cos(2 * np.pi * df['t'] / 12)

# feature matrix
X = df[['t', 'sin', 'cos']].values
y = df['Prices'].values

# model
model = LinearRegression()
model.fit(X, y)

print(f"Intercept (β0): {model.intercept_:.4f}")
print(f"Trend (β1): {model.coef_[0]:.4f}")
print(f"Sin (β2): {model.coef_[1]:.4f}")
print(f"Cos (β3): {model.coef_[2]:.4f}")

# future 12 mo
t_future = np.arange(len(df), len(df) + 12)
sin_future = np.sin(2 * np.pi * t_future / 12)
cos_future = np.cos(2 * np.pi * t_future / 12)
X_future = np.column_stack([t_future, sin_future, cos_future])

# prediction
y_pred_train = model.predict(X)
y_pred_future = model.predict(X_future)

# make future dates
future_dates = pd.date_range(start='2024-10-31', periods=12, freq='ME')

# vis
plt.figure(figsize=(13, 5))
plt.plot(df['Dates'], y, marker='o', label='Actual', linewidth=1.5)
plt.plot(df['Dates'], y_pred_train, label='Model Fit', linewidth=1.5)
plt.plot(future_dates, y_pred_future, linestyle='--', label='Forecast', linewidth=1.5)
plt.axvline(x=df['Dates'].iloc[-1], color='gray', linestyle=':', label='Forecast Start')
plt.title('Natural Gas Price: Fit & Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

def get_price(date_str):
    date = pd.to_datetime(date_str)
    base_date = df['Dates'].iloc[0]
    t = (date.year - base_date.year) * 12 + (date.month - base_date.month)
    
    sin_val = np.sin(2 * np.pi * t / 12)
    cos_val = np.cos(2 * np.pi * t / 12)
    
    price = model.predict([[t, sin_val, cos_val]])[0]
    return round(price, 2)

# test
print(get_price("2024-06-15"))   # past
print(get_price("2025-03-31"))   # future