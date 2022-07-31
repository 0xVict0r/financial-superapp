import streamlit as st
import estimator_optimiser.run_functions as run_functions
import pandas as pd

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

st.title("Portfolio Value Estimation")

st.write("Given a multitude of tickers and their value inside one's portfolio, the tool will estimate the most probable value of that portfolio at the end of the specified time. This uses the same method as the single stock estimator tool. The estimation is performed using the same methods as the single asset estimator (Monte Carlo and historical data).")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("init_form"):
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)
    col1, col2 = st.columns(2)
    ticker = col1.text_input("Input ticker here", placeholder="eg. AAPL")
    amount = col2.number_input(
        "Input value of ticker in portfolio", min_value=0, value=1000)
    add_btn = col1.form_submit_button("Add Ticker")
    remove_btn = col2.form_submit_button("Remove Latest Ticker")

    if add_btn:
        tickers_dict[ticker+"-EST"] = amount

    if remove_btn:
        del tickers_dict[ticker+"-EST"]

    for key in tickers_dict:
        if type(tickers_dict[key]) not in [type(0.0), type(0)]:
            del tickers_dict[key]

    df = pd.DataFrame(tickers_dict.items(), columns=[
        'Ticker', 'Value [$]'])
    df = df[df["Ticker"].str.contains('-EST')].reset_index(drop=True)
    df["Ticker"] = df["Ticker"].str.replace("-EST", "")
    st.table(df)

col1, col2 = st.columns(2)
init_value = df['Value [$]'].sum()
run_btn_mult = col1.button("Run Simulation")
reload_btn = col2.button("Reset Data")

if run_btn_mult:
    tickers = df["Ticker"].values
    weights = df['Value [$]'].values / init_value
    run_functions.portfolio_performance_estimator(tickers, weights, init_value,
                                                  years, mc_plotting=False, monte_carlo_trials=10000)
elif reload_btn:
    st.experimental_singleton.clear()
    st.experimental_memo.clear()
    tickers_dict.clear()
    st.experimental_rerun()
