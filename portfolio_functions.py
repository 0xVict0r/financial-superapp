import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import base_functions
import datetime

def get_portfolio_data(tickers):
    print('Retrieving Portoflio Assets Price Data!')
    data = pd.DataFrame()
    start_date = datetime.date(2000, 1, 3)
    
    for t in tickers:
        temp = pdr.DataReader(t, data_source='yahoo', start = start_date)['Adj Close']
        if temp.index[0] > pd.Timestamp(start_date):
            start_date = temp.index[0]
            data = data.loc[start_date:]
            temp = pdr.DataReader(t, data_source='yahoo', start = start_date)['Adj Close']
        data[t] = temp
    return data

def get_portfolio_hist_perf(data, weights):
    # Get the Covariance Matrix and the Portfolio Volatility
    cov_matrix = base_functions.log_returns(data).cov()
    vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Get the Portfolio Mean
    mean = np.dot(base_functions.log_returns(data).mean(), weights)
    return mean, vol

def get_sharpe_ratio(mean_vol):
    # Get Risk Free Rate
    rf = base_functions.import_stock_data('^TNX').iloc[-1]/100
    
    # Get Sharpe Ratio
    sharpe = ((1+mean_vol[0])**252-1-rf)/(mean_vol[1]*np.sqrt(252))
    return sharpe

def get_best_portfolio(data, num_ports=10):
    print('Starting Sharpe Optimization!')
    best_sharpe = 0
    
    for i in range(num_ports):
        print(f'Running Try no. {i+1}')
        # weights 
        weights = np.array(np.random.random(len(data.columns))) 
        weights = weights/np.sum(weights)  
        
        # Sharpe Ratio 
        sharpe_temp = get_sharpe_ratio(get_portfolio_hist_perf(data, weights))
        
        # Check Whether Higher
        if sharpe_temp > best_sharpe:
            best_weights = weights
            best_sharpe = sharpe_temp
        
    return best_sharpe, best_weights

def print_portfolio_weights(tickers, weights):
    print('Portfolio Weights: ')
    for i in range(len(tickers)):
        print(tickers[i] + f': {weights[i]*100}%')
    print('-----------------------------------')