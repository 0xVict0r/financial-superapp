import numpy as np


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
