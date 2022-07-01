import streamlit as st
import estimator_optimiser.run_functions as run_functions
import pandas as pd
import numpy as np

tickers_dict = st.session_state

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈",
)

st.title("Portfolio Optimiser")

with st.form("init_form"):
    years = st.slider(
        "Choose the number of years you want to calculate for", 1, 100, 1)
    ticker = st.text_input("Input ticker here",
                           placeholder="eg. AAPL")
    col1, col2 = st.columns(2)
    add_btn = col1.form_submit_button("Add Ticker")
    remove_btn = col2.form_submit_button("Remove Latest Ticker")

    if add_btn:
        tickers_dict[ticker+"-OPT"] = 0.0

    if remove_btn:
        del tickers_dict[ticker]

    for key in tickers_dict:
        if type(tickers_dict[key]) not in [type(0.0), type(0)]:
            del tickers_dict[key]

    df_opt = pd.DataFrame(tickers_dict.items(), columns=[
        'Ticker', 'Allocation [%]'])
    df_opt = df_opt[df_opt["Ticker"].str.contains('-OPT')]
    df_opt["Ticker"] = df_opt["Ticker"].str.replace("-OPT", "")
    cont = st.empty()
    cont.table(df_opt)

init_value = st.number_input(
    "Input funds to allocate", min_value=0, value=1000)
col1, col2 = st.columns(2)
run_btn_mult = col1.button("Run Simulation")
reload_btn = col2.button("Reset Data")

if run_btn_mult:
    tickers = df_opt["Ticker"].values
    final_weights = run_functions.best_portfolio_performance_estimator(
        tickers, init_value, years, mc_plotting=False, monte_carlo_trials=10000)
    df_opt['Allocation [%]'] = np.round(final_weights*100, 2)
    cont.empty()
    cont.table(df_opt)

elif reload_btn:
    st.experimental_singleton.clear()
    st.experimental_memo.clear()
    tickers_dict.clear()
    st.experimental_rerun()
