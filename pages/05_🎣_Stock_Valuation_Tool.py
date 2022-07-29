import streamlit as st
import numpy as np
import yfinance as yf
import fmpsdk as fm
import stock_valuation.valuation_functions as valuation_functions
import os

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

st.title("Stock Valuation Tool")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("value_stock_form"):
    ticker = st.text_input("Input ticker here",
                           placeholder="eg. AAPL").upper()
    run_btn_single = st.form_submit_button("Run")

if run_btn_single:
    api_key = os.environ.get("fmp_api")
    ticker_data = yf.Ticker(ticker).info
    current_price = fm.quote_short(api_key, ticker)[0]["price"]
    analyst_price = ticker_data["targetMedianPrice"]
    valuation, error = valuation_functions.get_valuation(ticker, True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Stock Price", f"${np.round(current_price, 2)}")
    col2.metric("Current Valuation", f"${np.round(valuation, 2)}",
                f"{np.round((valuation-current_price)/current_price * 100, 2)}%")
    try:
        col3.metric("Current Analyst Target", f"${np.round(analyst_price, 2)}",
                    f"{np.round((analyst_price-current_price)/current_price * 100, 2)}%")
    except TypeError:
        col3.metric("Current Analyst Target", "N/A")
    col4.metric("Historical Error", f"{np.round(error, 2)}%")
