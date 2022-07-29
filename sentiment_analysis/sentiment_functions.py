from urllib.request import urlopen
import certifi
import json
import numpy as np
import pandas as pd
import streamlit as st
import ssl
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

api_key = st.secrets["fmp_api"]
context = ssl.create_default_context(cafile=certifi.where())


def get_jsonparsed_data(url):
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return json.loads(data)


def clean(raw):
    result = re.sub("<[a][^>]*>(.+?)</[a]>", 'Link.', raw)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    return result


def get_news_df(ticker):
    url_news = (
        f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=1000&apikey={api_key}")
    social_sentiment_data = get_jsonparsed_data(url_news)
    df = pd.DataFrame(columns=['date', 'bare_text'])
    for i in range(len(social_sentiment_data)):
        df.at[i, 'date'] = social_sentiment_data[i]["publishedDate"][:10]
        df.at[i, 'bare_text'] = social_sentiment_data[i]["title"]
    return df


def clean_text(df):
    df["clean_text"] = np.array(
        [clean(df.at[i, "bare_text"]) for i in range(len(df))])
    return df


def get_sentiment_sentence(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']


def get_sentiment_df(df):
    df["news_sentiment"] = np.array(
        [get_sentiment_sentence(df.at[i, 'clean_text']) for i in range(len(df))])
    return df


def aggregate_news_sentiment(df):
    df = df.groupby('date')["date", "news_sentiment"].mean()
    df = df.sort_values(by="date", ascending=False)
    return df


if __name__ == "__main__":
    df = get_news_df("AAPL")
    df = clean_text(df)
    df = get_sentiment_df(df)
    print(aggregate_news_sentiment(df))
