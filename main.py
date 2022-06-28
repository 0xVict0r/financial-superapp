import run_functions
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

yf.pdr_override()


def clear_state():
    tickers_dict.clear()


asset_estimation_option = st.sidebar.selectbox(
    "Estimation Tools", ("Single Asset", "Portfolio", "Portfolio Optimiser"), on_change=clear_state)
tickers_dict = st.session_state

if asset_estimation_option == "Single Asset":
    st.title("Single Asset Price Estimation")
    with st.form("my_form"):
        years = st.slider(
            "Choose the number of years you want to calculate for", 1, 100, 1)
        ticker = st.text_input("Input ticker here",
                               placeholder="eg. AAPL")
        run_btn_single = st.form_submit_button("Run")

    if run_btn_single:
        run_functions.asset_price_estimator(
            ticker, years, mc_plotting=False, monte_carlo_trials=100000)

elif asset_estimation_option == "Portfolio":
    st.title("Portfolio Value Estimation")
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)

    with st.form("init_form"):
        col1, col2 = st.columns(2)
        ticker = col1.text_input("Input ticker here", placeholder="eg. AAPL")
        amount = col2.number_input(
            "Input value of ticker in portfolio", min_value=0)
        add_btn = col1.form_submit_button("Add Ticker")
        remove_btn = col2.form_submit_button("Remove Latest Ticker")

        if add_btn:
            tickers_dict[ticker] = amount

        if remove_btn:
            del tickers_dict[ticker]

        for key in tickers_dict:
            if type(tickers_dict[key]) not in [type(0.0), type(0)]:
                del tickers_dict[key]

        df = pd.DataFrame(tickers_dict.items(), columns=[
            'Ticker', 'Value [$]'])
        st.table(df)

    col1, col2 = st.columns(2)
    init_value = df['Value [$]'].sum()
    run_btn_mult = col1.button("Run Simulation")
    reload_btn = col2.button("Reset Data")

    if run_btn_mult:
        tickers = df["Ticker"].values
        weights = df['Value [$]'].values / init_value
        run_functions.portfolio_performance_estimator(tickers, weights, init_value,
                                                      years, mc_plotting=False, monte_carlo_trials=100000)
    elif reload_btn:
        st.experimental_singleton.clear()
        st.experimental_memo.clear()
        tickers_dict.clear()
        st.experimental_rerun()

elif asset_estimation_option == "Portfolio Optimiser":
    st.title("Portfolio Value Estimation")
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)

    with st.form("init_form"):
        ticker = st.text_input("Input ticker here",
                               placeholder="eg. AAPL")
        col1, col2 = st.columns(2)
        add_btn = col1.form_submit_button("Add Ticker")
        remove_btn = col2.form_submit_button("Remove Latest Ticker")

        if add_btn:
            tickers_dict[ticker] = 0.0

        if remove_btn:
            del tickers_dict[ticker]

        for key in tickers_dict:
            if type(tickers_dict[key]) not in [type(0.0), type(0)]:
                del tickers_dict[key]

        df_opt = pd.DataFrame(tickers_dict.items(), columns=[
            'Ticker', 'Allocation [%]'])
        cont = st.empty()
        cont.table(df_opt)

    init_value = st.number_input(
        "Input funds to allocate", min_value=0, value=1000)
    col1, col2 = st.columns(2)
    run_btn_mult = col1.button("Run Simulation")
    reload_btn = col2.button("Reset Data")

    if run_btn_mult:
        tickers = df_opt["Ticker"].values
        final_weights = run_functions.best_portfolio_performance_estimator(
            tickers, init_value, years, mc_plotting=False, monte_carlo_trials=100000)
        df_opt['Allocation [%]'] = np.round(final_weights*100, 2)
        cont.empty()
        cont.table(df_opt)

    elif reload_btn:
        st.experimental_singleton.clear()
        st.experimental_memo.clear()
        tickers_dict.clear()
        st.experimental_rerun()
