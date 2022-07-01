import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import estimator_optimiser.base_functions as base_functions
import datetime
import scipy.optimize as sco


def get_portfolio_data(tickers):
    global data

    print('Retrieving Portoflio Assets Price Data!')
    data = pd.DataFrame()
    start_date = datetime.date(2000, 1, 3)

    for t in tickers:
        temp = pdr.DataReader(t, data_source='yahoo',
                              start=start_date)['Adj Close']
        if temp.index[0] > pd.Timestamp(start_date):
            start_date = temp.index[0]
            data = data.loc[start_date:]
            temp = pdr.DataReader(t, data_source='yahoo',
                                  start=start_date)['Adj Close']
        data[t] = temp
    return data


def get_portfolio_hist_perf(data, weights):
    # Get the Covariance Matrix and the Portfolio Volatility
    vol = np.sqrt(np.dot(weights.T, np.dot(
        base_functions.log_returns(data).cov(), weights)))

    # Get the Portfolio Mean
    mean = np.log(
        1+np.dot((np.exp(base_functions.log_returns(data).mean())-1), weights))
    return mean, vol


def get_sharpe_ratio_single(mean_vol):
    return (mean_vol[0]*253)/(mean_vol[1]*np.sqrt(253))


def get_performance_ratio(weights):

    # Get the Covariance Matrix and the Portfolio Volatility
    returns_df = base_functions.log_returns(data)
    filtered_returns_df = returns_df[returns_df < 0]
    cov_matrix = filtered_returns_df.cov()
    vol_filtered = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    # Get the Portfolio Mean
    mean = np.dot(base_functions.log_returns(data).mean(), weights)

    # Get Risk Free Rate
    rf = base_functions.import_stock_data('^TNX').iloc[-1]/100

    # Get Sortino Ratio
    sortino = ((1+mean)**253-1-rf)/(vol_filtered*np.sqrt(253))
    return sortino*-1


def check_sum(weights):
    return np.sum(weights) - 1


def get_best_portfolio():
    print('Starting Optimization!')
    weights_init = np.random.random(len(data.columns))
    cons = ({'type': 'eq', 'fun': check_sum})
    bounds = tuple([(0, 1) for i in range(len(data.columns))])

    result = sco.minimize(get_performance_ratio, weights_init,
                          method='SLSQP', bounds=bounds, constraints=cons)

    return np.asarray(result.x)


def print_portfolio_weights(tickers, weights):
    print('Portfolio Weights: ')
    for i in range(len(tickers)):
        print(tickers[i] + f': {np.round(weights[i]*100, 2)}%')
    print('-----------------------------------')
