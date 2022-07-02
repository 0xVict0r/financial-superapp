import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import compound_interest.functions as functions
import plotly.express as px

st.set_page_config(
    page_title="Financial SuperApp",
    page_icon="📈"
)

st.title("Compound Interest Calculator")

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

with st.form("compound_form"):
    col1_bis, col2_bis, col3_bis = st.columns(3)
    col1, col2 = st.columns((2, 4))
    sel_choice = col1.radio("Select the compounding rate", [
        "Bi-daily", "Daily", "Weekly", "Monthly", "Bi-yearly", "Yearly"])
    inital_capital = col2.number_input(
        "Enter your starting capital", min_value=0.00, value=1000.00)

    decay = col1_bis.radio("Will the interest rate change?", ["No change",
                           "Linear change", "Exponential change"])
    col2_bis.write(" ")
    col3_bis.write(" ")
    pc_init = col2_bis.number_input(
        "Enter the initial interest rate [%]", min_value=0.01)
    pc_fin = col3_bis.number_input(
        "Enter the final interest rate [%]", min_value=0.01)

    length = col2.number_input(
        "Enter the legnth you want to compound for in years", 0, step=1, value=1)
    years = length

    if sel_choice == "Bi-daily":
        choice = 0.5
        length *= 2 * 365
    elif sel_choice == "Daily":
        choice = 1
        length *= 365
    elif sel_choice == "Weekly":
        choice = 365/52
        length *= 52
    elif sel_choice == "Monthly":
        choice = 365/12
        length *= 12
    elif sel_choice == "Bi-yearly":
        choice = 365/2
        length *= 2
    elif sel_choice == "Yearly":
        if length == 1:
            decay = "No change"
        choice = 365

    common = 365/choice

    if decay == "Linear change":
        interest = np.linspace(pc_init/common,
                               pc_fin/common, length)/100 + 1
    if decay == "Exponential change":
        interest = functions.get_exp_decay_apr(
            pc_init/common, pc_fin/common, length)/100 + 1
    if decay == "No change":
        pc_fin = pc_init
        interest = (np.ones(length) * pc_init/common)/100 + 1

    form_btn = st.form_submit_button("Run")

if form_btn:
    col1_fin, col2_fin, col3_fin, col4_fin = st.columns(4)
    rewards, funds = functions.get_rewards_compound_general(
        inital_capital, interest)
    col1_fin.metric("Starting Capital", f"${np.round(funds[0], 2)}")
    col2_fin.metric("Total Rewards", f"${np.round(rewards, 2)}")
    col3_fin.metric(
        "Final Capital", f"${np.round(funds[-1], 2)}", f'{np.round((funds[-1]-funds[0])/funds[0] * 100, 2)}%')
    col4_fin.metric("Effecive Annual Rate",
                    f"{np.round(rewards/inital_capital /years * 100, 2)}%")
    plot = px.line(y=funds)
    st.plotly_chart(plot)
