from urllib.request import urlopen
import certifi
import json
import numpy as np
import pandas as pd
import finnhub
import streamlit as st

api_key = st.secrets["finnhub_api"]
finnhub_client = finnhub.Client(api_key=api_key)

print(finnhub_client.stock_social_sentiment('AAPL'))


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_social_sentiment_data(ticker):
    url_social = (
        f"https://financialmodelingprep.com/api/v4/historical/social-sentiment?symbol={ticker}&page=0&apikey={api_key}")
    social_sentiment_data = get_jsonparsed_data(url_social)
    return social_sentiment_data


def get_current_social_sentiment(ticker_data):
    day = True
    i = 0
    stockwits_sentiment_list = []
    twitter_sentiment_list = []
    while day:
        stockwits_sentiment_list.append(ticker_data[i]["stocktwitsSentiment"])
        twitter_sentiment_list.append(ticker_data[i]["twitterSentiment"])
        i += 1
        if ticker_data[i]["date"][11:13] == "23":
            day = False
    stockwits_sentiment_array = np.array(
        [i for i in stockwits_sentiment_list if i > 0])
    twitter_sentiment_array = np.array(
        [i for i in twitter_sentiment_list if i > 0])
    total_social_sentiment = np.sqrt(
        np.mean(stockwits_sentiment_array)*np.mean(twitter_sentiment_array))
    return total_social_sentiment


def get_historical_social_sentiment(ticker_data):
    run = True
    i = 0
    stockwits_sentiment_list = []
    twitter_sentiment_list = []
    total_social_sentiment_list = []
    while run:
        stockwits_sentiment_list.append(ticker_data[i]["stocktwitsSentiment"])
        twitter_sentiment_list.append(ticker_data[i]["twitterSentiment"])
        i += 1
        if ticker_data[i]["date"][11:13] == "23" or i == 99:
            stockwits_sentiment_array = np.array(
                [i for i in stockwits_sentiment_list if i > 0])
            twitter_sentiment_array = np.array(
                [i for i in twitter_sentiment_list if i > 0])
            total_social_sentiment = np.sqrt(
                np.mean(stockwits_sentiment_array)*np.mean(twitter_sentiment_array))
            total_social_sentiment_list.append(total_social_sentiment)
            stockwits_sentiment_list = []
            twitter_sentiment_list = []
        if i == 99:
            run = False
    social_sentiment_arr = np.array(total_social_sentiment_list)
    return social_sentiment_arr


if __name__ == "__main__":
    print(get_current_social_sentiment(
        get_social_sentiment_data("AAPL")))
