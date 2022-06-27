import run_functions
import yfinance as yf
import streamlit as st

yf.pdr_override()

asset_estimation_option = st.sidebar.selectbox(
    "Which Estimator?", ("Single Asset", "Portfolio"))

if asset_estimation_option == "Single Asset":
    st.title("Single Asset Price Estimation")
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)
    ticker = st.text_input("Input ticker here",
                           placeholder="eg. AAPL")
    if len(ticker) != 0:
        run_functions.asset_price_estimator(
            ticker, years, mc_plotting=False, monte_carlo_trials=10000)

elif asset_estimation_option == "Portfolio":
    st.title("Portfolio Value Estimation")
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)


# Variables
# tickers = ['AAPL', 'AMZN', 'MSFT', 'FB', 'BTC-USD']
# price_init = 1000

# run_functions.best_portfolio_performance_estimator(
#     tickers, price_init, years, mc_plotting=False, monte_carlo_trials=10000)
# run_functions.portfolio_performance_estimator(
#     years, mc_plotting=False, monte_carlo_trials=10000)
