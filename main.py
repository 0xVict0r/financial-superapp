import run_functions
import yfinance as yf
import streamlit as st

yf.pdr_override()

st.title("Financial App")

years = st.slider(
    "Choose the number of years you want to calculate for", 1, 100, 1)
ticker = st.text_input("Input ticker here",
                       placeholder="eg. AAPL")

# Variables
monte_carlo_trials = 10000
# ticker = 'FB'
# tickers = ['AAPL', 'AMZN', 'MSFT', 'FB', 'BTC-USD']
# price_init = 1000

# run_functions.best_portfolio_performance_estimator(
#     tickers, price_init, years, mc_plotting=False, monte_carlo_trials=monte_carlo_trials)
# run_functions.portfolio_performance_estimator(
#     years, mc_plotting=False, monte_carlo_trials=monte_carlo_trials)
run_functions.asset_price_estimator(
    ticker, years, mc_plotting=False, monte_carlo_trials=monte_carlo_trials)
