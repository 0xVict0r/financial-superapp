import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import streamlit as st

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

st.title("Asset Price Estimator using Prophet")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("Main"):
    ticker = st.text_input("Enter the Stock you would like to predict")
    period = st.slider("Enter how long you want the prediction to be (yr)", min_value=1, max_value=5)
    form_bttn = st.form_submit_button("Run Simulation")

if form_bttn:
    data = yf.download(ticker, period='10y')

    df_train = data["Adj Close"].reset_index().rename(
        columns={"Date": "ds", "Adj Close": "y"})

    model = Prophet()
    model.fit(df_train)
    future = model.make_future_dataframe(periods=period*262)
    forecast = model.predict(future)

    fig = plot_plotly(model, forecast)
    st.plotly_chart(fig)
