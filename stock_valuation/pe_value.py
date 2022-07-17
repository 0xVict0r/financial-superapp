import fmpsdk as fm
from urllib.request import urlopen
import certifi
import json
import numpy as np
import streamlit as st

api_key = st.secrets["fmp_api"]


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_peers(ticker):
    ticker_info = fm.company_profile(apikey=api_key, symbol=ticker)[0]
    mc = ticker_info["mktCap"]
    industry = ticker_info["industry"]
    sector = ticker_info["sector"]
    try:
        peers_info = fm.stock_screener(apikey=api_key, industry=industry, sector=sector,
                                       market_cap_lower_than=int(np.floor(100*mc)), market_cap_more_than=int(np.floor(0.01*mc)), limit=10000)
    except:
        peers_info = fm.stock_screener(apikey=api_key, sector=sector,
                                       market_cap_lower_than=int(np.floor(100*mc)), market_cap_more_than=int(np.floor(0.01*mc)), limit=10000)
    peers = []
    for i in range(len(peers_info)):
        peers.append(peers_info[i]['symbol'])
    print(len(peers))
    return peers


def get_stock_pb_pe(ticker):
    url_ratios = (
        f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}")
    ticker_data = get_jsonparsed_data(url_ratios)
    pe = ticker_data[0]["priceEarningsRatioTTM"]
    pb = ticker_data[0]["priceToBookRatioTTM"]
    peg = ticker_data[0]["priceToFreeCashFlowsRatioTTM"]
    pfcf = ticker_data[0]["priceToFreeCashFlowsRatioTTM"]
    ps = ticker_data[0]["priceSalesRatioTTM"]
    return np.array([pe, pb, peg, pfcf, ps])


def get_sector_industry_pe_pb(ticker):
    peers = get_peers(ticker)
    pe_array = []
    pb_array = []
    peg_array = []
    pfcf_array = []
    ps_array = []
    for i in range(len(peers)):
        ticker_sim = peers[i]
        url = (
            f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker_sim}?apikey={api_key}")
        ratios_data = get_jsonparsed_data(url)
        pb_array.append(ratios_data[0]["priceToBookRatioTTM"])
        pe_array.append(ratios_data[0]["priceEarningsRatioTTM"])
        peg_array.append(ratios_data[0]["priceEarningsToGrowthRatioTTM"])
        pfcf_array.append(ratios_data[0]["priceToFreeCashFlowsRatioTTM"])
        ps_array.append(ratios_data[0]["priceSalesRatioTTM"])
    pe = np.median(np.array([i for i in pe_array if type(i) == type(0.0)]))
    pb = np.median(np.array([i for i in pb_array if type(i) == type(0.0)]))
    peg = np.median(np.array([i for i in peg_array if type(i) == type(0.0)]))
    pfcf = np.median(np.array([i for i in pfcf_array if type(i) == type(0.0)]))
    ps = np.median(np.array([i for i in ps_array if type(i) == type(0.0)]))
    return np.array([pe, pb, peg, pfcf, ps])


def get_pe_pb_value(ticker):
    stock_ratios = get_stock_pb_pe(ticker)
    sector_ratios = get_sector_industry_pe_pb(ticker)
    current_price = fm.quote_short(api_key, ticker)[0]["price"]
    value = (sector_ratios/stock_ratios) * current_price
    return np.median(value)


ticker = "AF.PA"
print(fm.quote_short(api_key, ticker)[0]["price"])
print(get_pe_pb_value(ticker))
