import streamlit as st
import yfinance as yf

yf.pdr_override()

st.set_page_config(
    page_title="Financial Estimation & Optimiser Tools",
    page_icon="📈",
)
