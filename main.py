import base_functions
import portfolio_functions
import numpy as np

# Variables
years = 1
trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'MSFT', 'BTC-USD']
weights = np.array([0.1, 0.5, 0.4])
price_init = 1000

if __name__ == "__main__":
    portfolio_data = portfolio_functions.get_portfolio_data(tickers)
    best_sharpe, best_weights = portfolio_functions.get_best_portfolio(portfolio_data, num_ports=10)
    mean, vol = portfolio_functions.get_portfolio_hist_perf(portfolio_data, best_weights)
    price_est = base_functions.simulate_mc(price_init, vol, mean, years*252 + 1, 1000, 'Portfolio')
    portfolio_functions.print_portfolio_weights(tickers, best_weights)
    # base_functions.plot_all_prices(price_est)