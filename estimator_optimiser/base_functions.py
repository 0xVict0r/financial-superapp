import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import estimator_optimiser.portfolio_functions as portfolio_functions
import streamlit as st
import altair as alt


def import_stock_data(ticker, start='2000-1-1'):
    data = pdr.DataReader(ticker, data_source='yahoo',
                          start=start)['Adj Close']
    return data


def lin_returns(data):
    return 1+data.pct_change()


def log_returns(data):
    return np.log(1+data.pct_change())


def get_asset_hist_perf(ticker):
    price = import_stock_data(ticker)
    mean = log_returns(price).mean()
    vol = log_returns(price).std()
    init_price = price[-1]
    return mean, vol, init_price


def drift_calc(vol, mean):
    return (mean-(0.5*vol**2))


def daily_returns(vol, mean, days, iterations):
    drift = drift_calc(vol, mean)
    daily_returns = np.exp(
        drift + vol * np.random.normal(0, 1, (days, iterations)))
    return daily_returns


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
    col2.metric("Hisorical Yearly Return",
                f"{np.round((mean*252)*100, 2)}%")
    col3.metric("Historical Yearly Volatility",
                f"{np.round(vol*np.sqrt(252)*100, 2)}%")
    col4.metric("Historical Sharpe Ratio",
                f"{np.round(portfolio_functions.get_sharpe_ratio_single([mean, vol]), 3)}")

    return price_df


def plot_all_prices(price_dataframe):
    price_dataframe.plot(legend=False, grid=True,
                         xlim=(0, len(price_dataframe)))
    plt.show()


def get_percentile_prices(price_dataframe):
    last_prices = price_dataframe.iloc[-1]
    prices = last_prices.quantile([0.25, 0.5, 0.75]).values
    return prices


def get_chart(data):
    hover = alt.selection_single(
        fields=["Time (Months)"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Asset Price Estimates")
        .mark_line()
        .encode(
            alt.X("Time (Months):Q", scale=alt.Scale(
                zero=False, nice=False)),
            alt.Y("Price:Q", scale=alt.Scale(zero=False)),
            color='Estimate',
            strokeDash='Estimate'
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Time (Months)",
            y="Price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Time (Months)", title="Time (Months)"),
                alt.Tooltip("Price", title="Price"),
                alt.Tooltip('Estimate', title="Estimate")
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


def plot_percentiles(init_price, percentile_prices, days):
    daily_interests = (percentile_prices/init_price)**(1/days)
    prices = np.ones((3, days+1))
    for j in np.arange(3):
        prices[j][0] *= init_price
        for i in np.arange(days):
            prices[j][i+1] *= prices[j][i] * daily_interests[j]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Bad Scenario',
                f'${np.round(percentile_prices[0], 2)}', f'{np.round((percentile_prices[0]-init_price)/init_price * 100, 2)}%')
    col2.metric('Median Scenario', f'${np.round(percentile_prices[1], 2)}',
                f'{np.round((percentile_prices[1]-init_price)/init_price * 100, 2)}%')
    col3.metric('Good Scenario', f'${np.round(percentile_prices[2], 2)}',
                f'{np.round((percentile_prices[2]-init_price)/init_price * 100, 2)}%')
    col4.metric("Yearly Return",
                f"{np.round(((percentile_prices[1]/init_price)**(252/days)-1)*100, 2)}%")

    df_bad = pd.DataFrame(
        {"Price": prices[0], "Estimate": "Bad", "Time (Months)": np.arange(days+1)/21})

    df_median = pd.DataFrame(
        {"Price": prices[1], "Estimate": "Median", "Time (Months)": np.arange(days+1)/21})

    df_good = pd.DataFrame(
        {"Price": prices[2], "Estimate": "Good", "Time (Months)": np.arange(days+1)/21})

    plotting_df = pd.concat([df_bad, df_median, df_good])

    fig = get_chart(plotting_df)
    st.altair_chart(fig, use_container_width=True)


if __name__ == "__main__":
    mean, vol, init_price = get_asset_hist_perf("AAPL")
    mean_vol = (mean, vol)
    print(portfolio_functions.get_sharpe_ratio_single(mean_vol))
