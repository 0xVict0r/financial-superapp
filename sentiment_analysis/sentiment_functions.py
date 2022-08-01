import numpy as np
import pandas as pd
import streamlit as st
import httpx
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime, timedelta


api_key = st.secrets["fmp_api"]


def get_jsonparsed_data(url):
    response = httpx.get(url)
    return response.json()


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


def get_news_df(ticker, duration_days):
    url_news = (
        f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=10000&apikey={api_key}")
    social_sentiment_data = get_jsonparsed_data(url_news)
    df = pd.DataFrame(columns=['date', 'bare_text'])
    i = 0
    while datetime.strptime(social_sentiment_data[i]["publishedDate"][:10], "%Y-%m-%d") >= (datetime.now() - timedelta(days=duration_days)):
        df.at[i, 'date'] = social_sentiment_data[i]["publishedDate"][:10]
        df.at[i, 'bare_text'] = social_sentiment_data[i]["title"]
        i += 1
    return df


def clean_text(df):
    df["clean_text"] = np.array(
        [clean(df.at[i, "bare_text"]) for i in range(len(df))])
    return df


def get_sentiment_sentence(sentence):
    try:
        sid_obj = SentimentIntensityAnalyzer()
    except LookupError:
        nltk.download('vader_lexicon')
        sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']


def get_sentiment_df(df):
    df["news_sentiment"] = np.array(
        [get_sentiment_sentence(df.at[i, 'clean_text']) for i in range(len(df))])
    return df


def aggregate_news_sentiment(df):
    df = df.groupby('date')[["date", "news_sentiment"]].mean()
    df = df.sort_values(by="date", ascending=True)
    return df


def domain_converter(sentiment):
    return (sentiment + 1)/2 * 100


def get_social_sentiment(ticker, days_from_now):
    df = pd.DataFrame(
        columns=['date', 'twitter_sentiment', "stocktwits_sentiment"])
    page = 0
    i = 0
    run = True
    while run:
        social_sentiment_json = get_jsonparsed_data(
            f"https://financialmodelingprep.com/api/v4/historical/social-sentiment?symbol={ticker}&page={page}&apikey={api_key}")
        for datapoint in social_sentiment_json:
            df.at[i, "date"] = datapoint["date"][:10]
            df.at[i, "twitter_sentiment"] = datapoint["twitterSentiment"]
            df.at[i, "stocktwits_sentiment"] = datapoint["stocktwitsSentiment"]

            if datetime.strptime(datapoint["date"][:10], "%Y-%m-%d") < (datetime.now() - timedelta(days=days_from_now)):
                run = False

            i += 1

        page += 1

    df["twitter_sentiment"] = df["twitter_sentiment"].replace(
        0, np.nan)
    df["stocktwits_sentiment"] = df["stocktwits_sentiment"].replace(
        0, np.nan)

    df["social_sentiment"] = ((df[['twitter_sentiment',
                                   'stocktwits_sentiment']].mean(axis=1) * 2) - 1)*2

    df = df.groupby('date')[["date", "social_sentiment"]].mean()

    return df


if __name__ == "__main__":
    ticker = "DIS"

    # df = get_news_df(ticker, 10)
    # df = clean_text(df)
    # df = get_sentiment_df(df)
    # df = aggregate_news_sentiment(df)

    df = get_social_sentiment(ticker, 10)

    print(df)
