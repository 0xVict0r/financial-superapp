import yfinance as yf
import pandas as pd
import numpy as np
import social_sentiment_functions as functions
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt


def add_price(ticker, df):
    df_price = yf.download(
        ticker, start=df.index.values[0], end=df.index.values[-1])["Close"]

    df_price.index = df_price.index.strftime("%Y-%m-%d")

    final_df = pd.concat([df, df_price], axis=1, join="inner")

    return final_df


def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) +
                   ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def get_transact_points(df):
    df["buying_points"] = np.NaN
    df["selling_points"] = np.NaN
    df = df.reset_index()
    for i in np.arange(len(df)-10):
        if (np.sign(df.at[i+9, "gradient_sentiment"]) == -1) and (np.sign(df.at[i+10, "gradient_sentiment"]) == 1) and (df.at[i+10, "stock_ma_gradient"] <= 0):
            df.at[i+10, "buying_points"] = df.at[i+10, "Close"]

        if (np.sign(df.at[i+9, "gradient_sentiment"]) == 1) and (np.sign(df.at[i+10, "gradient_sentiment"]) == -1) and (df.at[i+10, "stock_ma_gradient"] >= 0):
            df.at[i+10, "selling_points"] = df.at[i+10, "Close"]

    return df


if __name__ == "__main__":
    ticker = "DIS"

    df = functions.get_news_df(ticker, 12*30)
    df = functions.clean_text(df)
    df = functions.get_sentiment_df(df)
    df = functions.aggregate_news_sentiment(df)
    df = add_price(ticker, df)

    df["stock_ma"] = df["Close"].rolling(14).mean()
    df["stock_ma_gradient"] = np.gradient(df["stock_ma"].values)
    df["smooth_sentiment"] = gaussian_filter1d(
        df["news_sentiment"], 10)
    gradient_sentiment = np.gradient(df["smooth_sentiment"].values)
    df["gradient_sentiment"] = gradient_sentiment / np.max(gradient_sentiment)
    df = df.dropna(axis=0)
    df = get_transact_points(df)

    df = df.rename(
        columns={"smooth_sentiment": "Sentiment", "Close": "Close Price"}).set_index("index")
    fig, ax = plt.subplots(figsize=(15, 8))
    df.plot(ax=ax, y=["Close Price", "Sentiment", "stock_ma"], secondary_y=[
            "Sentiment"], mark_right=False, xlabel="Date", ylabel="Price", title=f"Stock Price vs. Sentiment for ${ticker}")
    ax.scatter(x=df.index, y=df['buying_points'], color="lime", zorder=100)
    ax.scatter(x=df.index, y=df['selling_points'], color="red", zorder=100)
    print(df['Close Price'].corr(df['Sentiment']))
    plt.show()
