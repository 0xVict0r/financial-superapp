import streamlit as st
import yfinance as yf

yf.pdr_override()

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈"
)

st.markdown(
    """
    # The Financial SuperApp

    _This financial superapp contains tools both to help an investor with the building of his portfolio and for simpler and more elementary applications. The tools provided by this app are shortly described below._

    ### _Single Asset Estimator_
    Given an asset's ticker (eg. AAPL for Apple Inc.), the tool will determine the most probable asset price at the end of the specified period. This is done using historical stock data (10 years) and a Monte Carlo estimation method.
    ### _Portfolio Estimator_
    Given a multitude of tickers and their value inside one's portfolio, the tool will estimate the most probable value of that portfolio at the end of the specified time. This uses the same method as the single stock estimator tool. The estimation is performed using the same methods as the single asset estimator (Monte Carlo and historical data).
    ### _Portfolio Optimiser_ 
    Given a ticker list, the tool will find the best possible combinantion according to the Sortino Optimisation theory. It will then compute the estimated price at the end of the speicified period given an initial investment (using a Monte Carlo method).
    ### _Compound Interest Calculator_
    A simple tool to visualise the power of compound interest. You can enter an initial capital, an interest rate, a compoundign rate and a investment length to determine how much money you'll end up with. The interest rate is also modifiable with time in case the investment has a decreasing/increasing interest rate.
    ### _Stock Valuation Tool_
    Given a stock symbol (no ETF, no FX, no Crypto), the tool will determine the fair value of the asset. It is calculated using a combination of financial ratios and DCF models as well as both relative and absolute methods. The median analyst price target is also given to have a comparison with institutionals. A graph showing the history of the valuation model and a figure of its error are also shown to assess the model's accuracy for the chosen stock.
    ### _Stock Sentiment Tool_
    This tool gets the market's sentiment of a given stock ticker in the US market (as it is the most popular and the only one yielding viable results). It uses data from Twitter, StockTwits and Wall Street news to generate a sentiment score between 0% and 100% (using natural language processing). A 4 day history is also given in order to understand the trend of the metric.
    """
)
