import streamlit as st
import plotly.graph_objects as go
import sentiment_analysis.sentiment_functions as sentiment_functions
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

st.title("Stock Social Sentiment")

st.markdown("""
This tool gets the market's sentiment of a given stock ticker in the US market (as it is the most popular and the only one yielding viable results). It uses data from Twitter, StockTwits and Wall Street news to generate a sentiment score between 0% and 100% (using natural language processing). A 4 day history is also given in order to understand the trend of the metric.
""")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("value_stock_form"):
    ticker = st.text_input("Input ticker here",
                           placeholder="eg. AAPL").upper()
    run_btn_single = st.form_submit_button("Run")

if run_btn_single:

    df_news = sentiment_functions.get_news_df(ticker, 30)
    df_news = sentiment_functions.clean_text(df_news)
    df_news = sentiment_functions.get_sentiment_df(df_news)
    df_news = sentiment_functions.aggregate_news_sentiment(df_news)

    social_df = sentiment_functions.get_social_sentiment(ticker, 30)

    df = pd.concat([df_news, social_df], axis=1, join="inner")
    df["total_sentiment"] = df[['social_sentiment',
                                'news_sentiment']].mean(axis=1)

    ma = df["total_sentiment"].rolling(5).mean().dropna()

    d_minus_4 = np.round(sentiment_functions.domain_converter(ma[-5]), 1)
    d_minus_3 = np.round(sentiment_functions.domain_converter(ma[-4]), 1)
    d_minus_2 = np.round(sentiment_functions.domain_converter(ma[-3]), 1)
    yesterday = np.round(sentiment_functions.domain_converter(ma[-2]), 1)
    today = np.round(sentiment_functions.domain_converter(ma[-1]), 1)

    if today <= 20:
        color = "darkred"
    elif 20 < today <= 40:
        color = "red"
    elif 40 < today <= 60:
        color = "orange"
    elif 60 < today <= 80:
        color = "green"
    else:
        color = "darkgreen"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        number={'suffix': "%"},
        domain={'x': [0, 1], 'y': [0, 1]},
        value=today,
        delta={'reference': yesterday},
        gauge={'axis': {'range': [0, 100],
                        "ticksuffix": "%"}, "bar": {"color": color}},
        title={'text': "Stock Sentiment Today"}))

    space, col1, col2, col3, col4 = st.columns([0.25, 1, 1, 1, 1])
    col1.metric("Yesterday", f"{yesterday}%")
    col2.metric("2 days ago", f"{d_minus_2}%")
    col3.metric("3 days ago", f"{d_minus_3}%")
    col4.metric("4 days ago", f"{d_minus_4}%")

    st.plotly_chart(fig)
