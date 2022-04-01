import base_functions
import portfolio_functions

# Variables
years = 1
trials = 10000
ticker = 'FB'

if __name__ == "__main__":
    mean, stdev, init_price = base_functions.get_asset_hist_perf(ticker)
    price_est = base_functions.simulate_mc(init_price, stdev, mean, years*252 + 1, 1000, 'test')
    base_functions.plot_all_prices(price_est)
    #sharpe, sortino, calmar = portfolio_functions.get_performance_ratios(ticker)