import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import portfolio_functions

# Get Historic Stock Prices
def import_stock_data(ticker, start = '2000-1-1'):
    data = pdr.DataReader(ticker, data_source='yahoo', start = start)['Adj Close']
    return data

# Calculate Linear Returns
def lin_returns(data):
    return (1+data.pct_change())

# Calculate Log Returns
def log_returns(data):
    return np.log(1+data.pct_change())

def get_asset_hist_perf(ticker):
    price = import_stock_data(ticker)
    mean = log_returns(price).mean()
    vol = log_returns(price).std()
    init_price = price[-1]
    return mean, vol, init_price

# Get Drift of the Asset
def drift_calc(vol, mean):
    return (mean-(0.5*vol**2))
    
# Calculate Daily Returns
def daily_returns(vol, mean, days, iterations):
    drift = drift_calc(vol, mean)
    daily_returns = np.exp(drift + vol * np.random.normal(0, 1, (days, iterations)))
    return daily_returns

# Monte Carlo
def simulate_mc(init_price, vol, mean, days, iterations, name):
    # Generate daily returns
    returns = daily_returns(vol, mean, days, iterations)
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
    print('-----------------------------------')
    print(name+':')
    print(f"Years: {(days)/252}")
    print(f"Expected Value: ${round(price_df.iloc[-1].median(),2)}")
    print(f"Return: {round(100*(price_df.iloc[-1].median()-price_list[0,1])/price_df.iloc[-1].median(),2)}%")
    print(f"Volatility: {vol*np.sqrt(252)*100}%")
    print(f"Sharpe Ratio: {portfolio_functions.get_sharpe_ratio([mean, vol])}")
    print('-----------------------------------')
          
    return price_df

def plot_all_prices(price_dataframe):
    price_dataframe.plot(legend = False, grid = True, xlim=(0, len(price_dataframe)))
    plt.show()
    
def get_percentile_prices(price_dataframe):
    last_prices = price_dataframe.iloc[-1]
    prices = last_prices.quantile([.25, .5, .75]).values
    return prices

def plot_percentiles(init_price, percentile_prices, days):
    daily_interests = (percentile_prices/init_price)**(1/days)
    prices = np.ones((3, days+1))
    for j in np.arange(3):
        prices[j][0] *= init_price
        for i in np.arange(days):
            prices[j][i+1] *= prices[j][i] * daily_interests[j]
            
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(np.arange(days+1)/21, prices[0])
    ax.plot(np.arange(days+1)/21, prices[1])
    ax.plot(np.arange(days+1)/21, prices[2])
    ax.grid()
    plt.show()