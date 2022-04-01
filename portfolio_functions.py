import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import base_functions

def get_portfolio_hist_perf(tickers, weights):
    # Create Stock Prices Dataframes
    data = pd.DataFrame()
    for t in tickers:
        data[t] = pdr.DataReader(t, data_source='yahoo', start = '2000-1-1')['Adj Close']
        
    # Get the Covariance Matrix and the Portfolio Volatility
    cov_matrix = base_functions.log_returns(data).cov()
    vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Get the Portfolio Mean
    mean = np.dot(base_functions.log_returns(data).mean(), weights)
    price_init = np.dot(data.iloc[-1], weights)
    return vol, mean, price_init

def get_sharpe_ratio(mean, vol):
    # Get Risk Free Rate
    rf = base_functions.import_stock_data('^TNX').iloc[-1]/100
    
    # Get Sharpe Ratio
    sharpe = ((1+mean)**252-1-rf)/(vol*np.sqrt(252))
    return sharpe

def get_best_portfolio(tickers):
    num_ports = 10
    all_weights = np.zeros((num_ports, len(tickers)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for i in range(num_ports): 
        # weights 
        weights = np.array(np.random.random(len(tickers))) 
        weights = weights/np.sum(weights)  
        
        # save the weights
        all_weights[i,:] = weights
        
        # expected return 
        vol_arr[i], ret_arr[i],_ = get_portfolio_hist_perf(tickers, weights)

        # Sharpe Ratio 
        sharpe_arr[i] = get_sharpe_ratio(ret_arr[i], vol_arr[i])
    
    # plot the data
    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.show()

def get_performance_ratios(ticker):
    # Get Risk Free Rate
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