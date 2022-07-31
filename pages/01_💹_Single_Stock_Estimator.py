import streamlit as st
import estimator_optimiser.run_functions as run_functions

tickers_dict = st.session_state

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Single Asset Price Estimation")

st.write("Given an asset's ticker (eg. AAPL for Apple Inc.), the tool will determine the most probable asset price at the end of the specified period. This is done using historical stock data (10 years) and a Monte Carlo estimation method.")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("my_form"):
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)
    ticker = st.text_input("Input ticker here",
                           placeholder="eg. AAPL")
    run_btn_single = st.form_submit_button("Run")

if run_btn_single:
    run_functions.asset_price_estimator(
        ticker, years, mc_plotting=False, monte_carlo_trials=10000)
