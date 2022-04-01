import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import seaborn as sns

# Get Historic Stock Prices
def import_stock_data(tickers, start = '2000-1-1'):
    data = pd.DataFrame()
    for t in tickers:
        data[t] = wb.DataReader(t, data_source='yahoo', start = start)['Adj Close']
    return data

# Calculate Log Returns
def log_returns(data):
    return (np.log(1+data.pct_change()))

# Get Drift of the Stock
def drift_calc(data):
    return (log_returns(data).mean()-(0.5*log_returns(data).var()))
    
# Calculate Daily Returns
def daily_returns(data, days, iterations):
    drift = drift_calc(data).values
    stdv = log_returns(data).std().values
    dr = np.exp(drift + stdv * np.random.normal(0, 1, (days, iterations)))
    return dr

# Monte Carlo
def simulate_mc(data, days, iterations):
    # Generate daily returns
    returns = daily_returns(data, days, iterations)
    # Create empty matrix
    price_list = np.zeros_like(returns)
    # Put the last actual price in the first row of matrix. 
    price_list[0] = data.iloc[-1]
    # Calculates the price everyday
    for t in range(1, days):
        price_list[t] = price_list[t-1]*returns[t]
    
    # Make the results a pandas dataframe
    price_df = pd.DataFrame(price_list)
          
    # Printing information about stock
    print(data.columns[0])
    print(f"Days: {days-1}")
    print(f"Expected Value: ${round(price_df.iloc[-1].mean(),2)}")
    print(f"Return: {round(100*(price_df.iloc[-1].mean()-price_list[0,1])/price_df.iloc[-1].mean(),2)}%")
          
    return price_df

def plot_all_prices(price_dataframe):
    # price_dataframe = price_dataframe.cumsum()
    price_dataframe.plot(legend = False, grid = True, xlim=(0, 365))
    plt.show()