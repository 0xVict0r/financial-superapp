import streamlit as st
import numpy as np
import yfinance as yf
import fmpsdk as fm
import stock_valuation.pe_value as pe_value
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
    dcf_price = fm.discounted_cash_flow(api_key, ticker)[0]["dcf"]
    dcf_hist_data = fm.historical_discounted_cash_flow(
        api_key, ticker, "annual", limit=10)
    dcf_hist = pe_value.get_historical_dcf(ticker)
    financial_price, df_stock, df_sector, dates = pe_value.get_pe_pb_value(
        ticker)
    mod_financial, ave_dcf_diff, financial_df = pe_value.plot_hist(
        ticker, df_sector, df_stock, dcf_hist, dates)
    financial_price = financial_price/mod_financial
    analyst_price = ticker_data["targetMedianPrice"]
    dcf_price = dcf_price/ave_dcf_diff
    valuation = np.mean([financial_price, dcf_price])
    error = pe_value.get_error(financial_df)
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
