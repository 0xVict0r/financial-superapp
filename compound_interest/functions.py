import numpy as np
import altair as alt
import pandas as pd


def get_exp_decay_apr(pc_init, pc_fin, common):
    x = np.arange(common)
    a = pc_init
    b = (np.log(pc_fin/pc_init))/(common-1)
    apr = a * np.exp(b*x)
    return apr


def get_rewards_compound_general(funds_init, apr_array):
    funds = np.ones(len(apr_array) + 1) * funds_init
    for i in range(len(funds)-1):
        funds[i+1] = funds[i] * apr_array[i]
    rewards = funds[-1] - funds[0]
    return rewards, funds


def get_chart(funds):

    data = pd.DataFrame({"Time": np.arange(len(funds)), "Funds": funds})

    hover = alt.selection_single(
        fields=["Time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Funds over Time")
        .mark_line()
        .encode(
            alt.X("Time:Q", scale=alt.Scale(zero=False, nice=False)),
            alt.Y("Funds:Q", scale=alt.Scale(zero=False))
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Time",
            y="Funds",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Time", title="Time"),
                alt.Tooltip("Funds", title="Funds")
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()
