# import streamlit as st
# import numpy as np
# import yfinance as yf
# import fmpsdk as fm
# import sentiment_analysis.sentiment_functions as sentiment_functions

# st.set_page_config(
#     page_title="Financial SuperApp",
#     page_icon="📈",
# )

# st.title("Stock Valuation Tool")

# st.markdown(
#     """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

# with st.form("value_stock_form"):
#     ticker = st.text_input("Input ticker here",
#                            placeholder="eg. AAPL").upper()
#     run_btn_single = st.form_submit_button("Run")

# if run_btn_single:
#     ticker_info = sentiment_functions.get_social_sentiment_data(ticker)
#     # social_sentiment_arr = sentiment_functions.get_historical_social_sentiment(ticker_info)
#     current_social_sentiment = sentiment_functions.get_current_social_sentiment(
#         ticker_info)
#     st.metric("Current Social Sentiment", current_social_sentiment)
