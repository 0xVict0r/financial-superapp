import base_functions
import portfolio_functions
import numpy as np

# Variables
years = 1
trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'MSFT', 'GOOGL']
weights = np.array([0.1, 0.5, 0.4])

if __name__ == "__main__":
    # mean, stdev, init_price = base_functions.get_asset_hist_perf(ticker)
    # price_est = base_functions.simulate_mc(init_price, stdev, mean, years*252 + 1, 1000, 'test')
    # base_functions.plot_all_prices(price_est)
    vol, mean, price_init = portfolio_functions.get_portfolio_hist_perf(tickers, weights)
    price_est = base_functions.simulate_mc(price_init, vol, mean, years*252 + 1, 1000, 'test')
    base_functions.plot_all_prices(price_est)