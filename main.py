import base_functions
import portfolio_functions
import numpy as np
import itertools

# Variables
years = 1
trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'MSFT', 'GOOGL']
weights = np.array([0.1, 0.5, 0.4])

if __name__ == "__main__":
    # vol, mean, price_init = portfolio_functions.get_portfolio_hist_perf(tickers, weights)
    # price_est = base_functions.simulate_mc(price_init, vol, mean, years*252 + 1, 1000, 'Portfolio')
    # base_functions.plot_all_prices(price_est)
    # print(portfolio_functions.get_sharpe_ratio(mean, vol))
    portfolio_functions.get_best_portfolio(tickers)