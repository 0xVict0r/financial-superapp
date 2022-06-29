import streamlit as st
import run_functions

tickers_dict = st.session_state

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
