from email.mime import base
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import base_functions

def get_performance_ratios(tickers):
    # Get Stock Data
    stock_data = base_functions.import_stock_data(tickers)
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