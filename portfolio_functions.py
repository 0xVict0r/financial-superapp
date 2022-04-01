import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import base_functions

def get_portfolio_hist_perf(tickers, weights):
    data = pd.DataFrame()
    for t in tickers:
        data[t] = pdr.DataReader(t, data_source='yahoo', start = '2000-1-1')['Adj Close']
    cov_matrix = base_functions.log_returns(data).cov()
    vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    mean = base_functions.log_returns(data).mean().sum()
    for t in tickers:
        data[t] = weights[tickers.index(t)] * data[t]
    price_init = data.sum(axis=1)[-1]
    return vol, mean, price_init

def get_performance_ratios(ticker):
    # Get Stock Data
    stock_data = base_functions.import_stock_data(ticker)
    rf_data = base_functions.import_stock_data(['^TNX'])/100
    
    # Get Stock Risk Free Return
    stock_return = ((stock_data.pct_change().values).T[0])[1:]
    rf_stock_return = ((np.average(stock_return)+1)**252-1) - rf_data.values[-1]
    
    # Get STDEVs 
    stock_rf_hist = stock_return[1:] - rf_data.values.T[0][-len(stock_return)+1:]
    stdev_stock_rf = np.std(stock_rf_hist) * np.sqrt(252)
    stdev_stock_rf_neg = np.std(stock_rf_hist[stock_rf_hist < 0]) * np.sqrt(252)
    
    # Get Max Drawdown
    comp_return = (1+stock_data.pct_change()).cumprod()
    peak = comp_return.cummax()
    drawdown = (comp_return - peak)/peak
    max_dd = drawdown.min()[0]
    
    # Get Ratios
    sharpe = (rf_stock_return/stdev_stock_rf)[0]
    sortino = (rf_stock_return/stdev_stock_rf_neg)[0]
    calmar = (rf_stock_return/np.abs(max_dd))[0]
    
    return sharpe, sortino, calmar