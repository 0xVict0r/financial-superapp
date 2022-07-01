import streamlit as st
import yfinance as yf

yf.pdr_override()

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

st.markdown(
    """
    # The Financial SuperApp

    _This financial superapp contains tools both to help an investor with the building of his portfolio and for simpler and more elementary applications. The tools provided by this app are shortly described below._

    * Single Asset Estimator: Given an asset's ticker (eg. AAPL for Apple Inc.), the tool will determine the most probable asset price at the end of the specified period.
    * Portfolio Estimator: Given a multitude of tickers and their value inside one's portfolio, the tool will estimate the most probable value of that portfolio at the end of the specified time. This uses the same method as the single stock estimator tool.
    * Portfolio Optimiser: Given a ticker list, the tool will find the best possible combinantion according to the Sharpe Optimisation theory. It will then compute the estimated price at the end of the speicified period given an initial investment.
    """
)
