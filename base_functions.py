import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import portfolio_functions
import streamlit as st
import altair as alt
import plotly.express as px

pd.options.plotting.backend = "plotly"

# Get Historic Stock Prices


def import_stock_data(ticker, start='2000-1-1'):
    data = pdr.DataReader(ticker, data_source='yahoo',
                          start=start)['Adj Close']
    return data


def get_weights_and_tickers():
    data = np.genfromtxt('./data/portfolio.csv',
                         delimiter=',', dtype=str, skip_header=1)
    tickers = data[:, 0]
    init_value = np.sum(data[:, 1].astype(float))
    weights = data[:, 1].astype(float)/init_value
    return tickers, weights, init_value

# Calculate Linear Returns


def lin_returns(data):
    return 1+data.pct_change()

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
    daily_returns = np.exp(
        drift + vol * np.random.normal(0, 1, (days, iterations)))
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
    st.write(name+':')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Value", f"${np.round(init_price, 2)}")
    col2.metric("Yearly Return",
                f"{np.round(((price_df.iloc[-1].median()/init_price)**(252/days)-1)*100, 2)}%")
    col3.metric("Yearly Volatility", f"{np.round(vol*np.sqrt(252)*100, 2)}%")
    col4.metric("Sharpe Ratio",
                f"{np.round(portfolio_functions.get_sharpe_ratio_single([mean, vol]), 3)}")

    return price_df


def plot_all_prices(price_dataframe):
    price_dataframe.plot(legend=False, grid=True,
                         xlim=(0, len(price_dataframe)))
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

    col1, col2, col3 = st.columns(3)
    col1.metric('Bad Scenario',
                f'${np.round(percentile_prices[0], 2)}', f'{np.round((percentile_prices[0]-init_price)/init_price * 100, 2)}%')
    col2.metric('Median Scenario', f'${np.round(percentile_prices[1], 2)}',
                f'{np.round((percentile_prices[1]-init_price)/init_price * 100, 2)}%')
    col3.metric('Good Scenario', f'${np.round(percentile_prices[2], 2)}',
                f'{np.round((percentile_prices[2]-init_price)/init_price * 100, 2)}%')

    df = pd.DataFrame(
        {"Bad": prices[0], "Median": prices[1], "Good": prices[2]}, index=np.arange(days+1)/21)

    fig = df.plot(labels=dict(
        index="Time [Months]", value="Price [$]", variable="Scenario"))
    fig.update_yaxes(tickprefix="$")
    st.plotly_chart(fig, use_container_width=True)
