import streamlit as st
import numpy as np
import yfinance as yf
import fmpsdk as fm
import stock_valuation.pe_value as pe_value

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
    api_key = st.secrets["fmp_api"]
    ticker_data = yf.Ticker(ticker).info
    current_price = fm.quote_short(api_key, ticker)[0]["price"]
    dcf_price = fm.discounted_cash_flow(api_key, ticker)[0]["dcf"]
    financial_price = pe_value.get_pe_pb_value(ticker)
    analyst_price = ticker_data["targetMedianPrice"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Stock Price", f"${np.round(current_price, 2)}")
    col2.metric("DCF Value", f"${np.round(dcf_price, 2)}",
                f"{np.round((dcf_price-current_price)/current_price * 100, 2)}%")
    col3.metric("Financial Value", f"${np.round(financial_price, 2)}",
                f"{np.round((financial_price-current_price)/current_price * 100, 2)}%")
    col4.metric("Analyst Value", f"${np.round(analyst_price, 2)}",
                f"{np.round((analyst_price-current_price)/current_price * 100, 2)}%")
