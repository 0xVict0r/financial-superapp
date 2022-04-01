from curses import start_color
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

# Get Historic Stock Prices
def import_stock_data(ticker, start = '2000-1-1'):
    data = pdr.DataReader(ticker, data_source='yahoo', start = start)['Adj Close']
    return data

# Calculate Linear Returns
def lin_returns(data):
    return (1+data.pct_change())

# Calculate Log Returns
def log_returns(data):
    return (np.log(1+data.pct_change()))

def get_asset_hist_perf(ticker):
    price = import_stock_data(ticker)
    mean = log_returns(price).mean()
    stdev = log_returns(price).std()
    init_price = price[-1]
    return mean, stdev, init_price

# Get Drift of the Asset
def drift_calc(stdev, mean):
    return (mean-(0.5*stdev**2))
    
# Calculate Daily Returns
def daily_returns(stdev, mean, days, iterations):
    drift = drift_calc(stdev, mean)
    daily_returns = np.exp(drift + stdev * np.random.normal(0, 1, (days, iterations)))
    return daily_returns

# Monte Carlo
def simulate_mc(init_price, stdev, mean, days, iterations, name):
    # Generate daily returns
    returns = daily_returns(stdev, mean, days, iterations)
    # Create empty matrix
    price_list = np.zeros_like(returns)
    # Put the last actual price in the first row of matrix. 
    price_list[0] = init_price
    # Calculates the price everyday
    for t in range(1, days):
        price_list[t] = price_list[t-1]*returns[t]
    
    # Make the results a pandas dataframe
    price_df = pd.DataFrame(price_list)
          
    # Printing information about stock
    print(name)
    print(f"Years: {(days-1)/252}")
    print(f"Expected Value: ${round(price_df.iloc[-1].mean(),2)}")
    print(f"Return: {round(100*(price_df.iloc[-1].mean()-price_list[0,1])/price_df.iloc[-1].mean(),2)}%")
          
    return price_df

def plot_all_prices(price_dataframe):
    price_dataframe.plot(legend = False, grid = True, xlim=(0, len(price_dataframe)))
    plt.show()