from tracemalloc import start
import fmpsdk as fm
from urllib.request import urlopen
import certifi
import json
import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import altair as alt
import os

api_key = os.environ.get("fmp_api")


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_peers(ticker):
    url_peers = (
        f"https://financialmodelingprep.com/api/v4/stock_peers?symbol={ticker}&apikey={api_key}")
    peers = get_jsonparsed_data(url_peers)[0]["peersList"]
    # ticker_info = fm.company_profile(apikey=api_key, symbol=ticker)[0]
    # mc = ticker_info["mktCap"]
    # industry = ticker_info["industry"]
    # sector = ticker_info["sector"]
    # try:
    #     peers_info = fm.stock_screener(apikey=api_key, industry=industry, sector=sector,
    #                                    market_cap_lower_than=int(np.floor(100*mc)), market_cap_more_than=int(np.floor(0.01*mc)), limit=10000)
    # except:
    #     peers_info = fm.stock_screener(apikey=api_key, sector=sector,
    #                                    market_cap_lower_than=int(np.floor(100*mc)), market_cap_more_than=int(np.floor(0.01*mc)), limit=10000)
    # peers = []
    # for i in range(len(peers_info)):
    #     peers.append(peers_info[i]['symbol'])
    return peers


def tolerant_median(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens), len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l), idx] = l
    return np.median(np.array(arr), axis=-1)


def get_stock_pb_pe(ticker):
    url_hist = (
        f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?limit=10&apikey={api_key}")
    ratios_data_hist = get_jsonparsed_data(url_hist)
    ticker_yf_info = yf.Ticker(ticker).info
    pe = ticker_yf_info["forwardPE"]
    pb = ticker_yf_info["priceToBook"]
    peg = ticker_yf_info["pegRatio"]
    pfcf = ticker_yf_info["marketCap"]/ticker_yf_info["freeCashflow"]
    ps = ticker_yf_info["priceToSalesTrailing12Months"]
    pe_array_hist = []
    pb_array_hist = []
    peg_array_hist = []
    pfcf_array_hist = []
    ps_array_hist = []
    dates_hist = []
    for j in range(len(ratios_data_hist)):
        pe_array_hist.append(ratios_data_hist[j]["priceEarningsRatio"])
        pb_array_hist.append(ratios_data_hist[j]["priceToBookRatio"])
        peg_array_hist.append(
            ratios_data_hist[j]["priceEarningsToGrowthRatio"])
        pfcf_array_hist.append(
            ratios_data_hist[j]["priceToFreeCashFlowsRatio"])
        ps_array_hist.append(ratios_data_hist[j]["priceSalesRatio"])
        dates_hist.append(ratios_data_hist[j]["date"])
    pe_hist = np.array(pe_array_hist)
    pb_hist = np.array(pb_array_hist)
    peg_hist = np.array(peg_array_hist)
    pfcf_hist = np.array(pfcf_array_hist)
    ps_hist = np.array(ps_array_hist)
    dates = np.array(dates_hist)
    df_hist = pd.DataFrame({'pe': pe_hist, 'pb': pb_hist,
                           'peg': peg_hist, 'pfcf': pfcf_hist, 'ps': ps_hist})
    return np.array([pe, pb, peg, pfcf, ps]), df_hist, dates


def get_sector_industry_pe_pb(ticker):
    peers = get_peers(ticker)
    pe_array = []
    pb_array = []
    peg_array = []
    pfcf_array = []
    ps_array = []
    pe_array_hist = []
    pb_array_hist = []
    peg_array_hist = []
    pfcf_array_hist = []
    ps_array_hist = []
    for i in range(len(peers)):
        pe_array_temp = []
        pb_array_temp = []
        peg_array_temp = []
        pfcf_array_temp = []
        ps_array_temp = []
        ticker_sim = peers[i]
        url = (
            f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker_sim}?apikey={api_key}")
        ratios_data = get_jsonparsed_data(url)
        pb_array.append(ratios_data[0]["priceToBookRatioTTM"])
        pe_array.append(ratios_data[0]["priceEarningsRatioTTM"])
        peg_array.append(ratios_data[0]["priceEarningsToGrowthRatioTTM"])
        pfcf_array.append(ratios_data[0]["priceToFreeCashFlowsRatioTTM"])
        ps_array.append(ratios_data[0]["priceSalesRatioTTM"])
        url_hist = (
            f"https://financialmodelingprep.com/api/v3/ratios/{ticker_sim}?limit=10&apikey={api_key}")
        ratios_data_hist = get_jsonparsed_data(url_hist)
        for j in range(len(ratios_data_hist)):
            pe_array_temp.append(ratios_data_hist[j]["priceEarningsRatio"])
            pb_array_temp.append(ratios_data_hist[j]["priceToBookRatio"])
            peg_array_temp.append(
                ratios_data_hist[j]["priceEarningsToGrowthRatio"])
            pfcf_array_temp.append(
                ratios_data_hist[j]["priceToFreeCashFlowsRatio"])
            ps_array_temp.append(ratios_data_hist[j]["priceSalesRatio"])
        pe_array_hist.append(pe_array_temp)
        pb_array_hist.append(pb_array_temp)
        peg_array_hist.append(peg_array_temp)
        pfcf_array_hist.append(pfcf_array_temp)
        ps_array_hist.append(ps_array_temp)
    pe_hist = tolerant_median(np.array(pe_array_hist))
    pb_hist = tolerant_median(np.array(pb_array_hist))
    peg_hist = tolerant_median(np.array(peg_array_hist))
    pfcf_hist = tolerant_median(np.array(pfcf_array_hist))
    ps_hist = tolerant_median(np.array(ps_array_hist))
    df_hist = pd.DataFrame({'pe': pe_hist, 'pb': pb_hist,
                           'peg': peg_hist, 'pfcf': pfcf_hist, 'ps': ps_hist})
    pe = np.median(np.array([i for i in pe_array if type(i) == type(0.0)]))
    pb = np.median(np.array([i for i in pb_array if type(i) == type(0.0)]))
    peg = np.median(np.array([i for i in peg_array if type(i) == type(0.0)]))
    pfcf = np.median(np.array([i for i in pfcf_array if type(i) == type(0.0)]))
    ps = np.median(np.array([i for i in ps_array if type(i) == type(0.0)]))
    return np.array([pe, pb, peg, pfcf, ps]), df_hist


def get_historical_dcf(ticker):
    url = (
        f"https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/{ticker}?apikey={api_key}")
    dcf_hist_data = get_jsonparsed_data(url)
    return np.array([dcf_data['dcf'] for dcf_data in dcf_hist_data])[:10]


def get_pe_pb_value(ticker):
    stock_ratios, df_stock, dates = get_stock_pb_pe(ticker)
    sector_ratios, df_sector = get_sector_industry_pe_pb(ticker)
    current_price = fm.quote_short(api_key, ticker)[0]["price"]
    value_list = []
    for i in range(len(sector_ratios)):
        if type(sector_ratios[i]) != type(None) and type(stock_ratios[i]) != type(None):
            value_list.append(
                (sector_ratios[i]/stock_ratios[i]) * current_price)
    value = np.array(value_list)
    return np.median(value), df_stock, df_sector, dates


def get_chart(data):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Historical Expected vs. Real Stock Price")
        .mark_line()
        .encode(
            x="Date",
            y="Price",
            color='Method',
            strokeDash='Method'
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Date",
            y="Price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Year"),
                alt.Tooltip("Price", title="Price"),
                alt.Tooltip('Method', title="Method")
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


def plot_hist(ticker, df_sector, df_stock, dcf_hist, dates):
    dcf_diff = []
    series_diff = (df_stock/df_sector).median(axis=1)
    financial_df = pd.DataFrame({'date': dates, 'financial_diff': series_diff})
    financial_df["mod_diff"] = financial_df["financial_diff"] / \
        financial_df["financial_diff"].median()
    for i in range(len(financial_df["mod_diff"])):
        start_date = financial_df.at[i, "date"]
        date_1 = datetime.datetime.strptime(
            start_date, "%Y-%m-%d")
        end_date = date_1 + datetime.timedelta(days=10)
        financial_df.at[i, "real_price"] = np.round(yf.download(
            ticker, start=start_date, end=end_date)["Close"][0], 2)
        financial_value_temp = financial_df.at[i,
                                               "real_price"] * financial_df.at[i, "mod_diff"]

    historical_price = pd.DataFrame(
        {'Date': dates, 'Price': financial_df['real_price'], 'Method': 'Historical Price'})
    dcf_diff = np.array([(dcf_hist[i]/historical_price['Price'].values[i])
                        for i in range(len(financial_df["mod_diff"]))])
    av_dcf_diff = np.median(dcf_diff)

    for i in range(len(financial_df["mod_diff"])):
        if type(financial_value_temp) not in [type(0), type(0.0)]:
            financial_df.at[i, "expected_value"] = np.round(
                dcf_hist[i]/av_dcf_diff, 2)
        elif type(financial_value_temp) in [type(0), type(0.0)]:
            financial_df.at[i, "expected_value"] = np.round(
                financial_value_temp, 2)
        else:
            financial_df.at[i, "expected_value"] = np.round(
                np.mean([financial_value_temp, dcf_hist[i]/av_dcf_diff]), 2)

        if financial_df.at[i, "expected_value"] < 0:
            financial_df.at[i, "expected_value"] = 0

    plotting_df = pd.DataFrame(
        {"Date": dates, 'Price': financial_df['expected_value']})
    plotting_df['Method'] = "Expected Value"

    plotting_df = pd.concat([plotting_df, historical_price])
    plotting_df["Date"] = pd.to_datetime(
        plotting_df["Date"], format="%Y-%m-%d")
    plotting_df["Date"] = pd.DatetimeIndex(
        plotting_df["Date"]).year.astype(str)

    chart = get_chart(plotting_df)
    st.altair_chart(chart, use_container_width=True)

    return financial_df["financial_diff"].median(), av_dcf_diff, financial_df


def get_error(financial_df):
    error_array = (np.abs(
        financial_df['real_price'] - financial_df['expected_value'])/financial_df['real_price'])*100
    return np.mean(error_array)


if __name__ == "__main__":
    ticker = "ETL.PA"
    get_pe_pb_value(ticker)
