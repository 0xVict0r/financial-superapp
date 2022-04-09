import run_functions
import numpy as np

# Variables
years = 5
monte_carlo_trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'TSLA', 'BTC-USD']
price_init = 1000

if __name__ == "__main__":
    # run_functions.best_portfolio_performance_estimator(tickers, price_init, years, plotting=False, num_ports=500, monte_carlo_trials=monte_carlo_trials)
    run_functions.portfolio_performance_estimator(years, plotting=False, monte_carlo_trials=monte_carlo_trials)
    # run_functions.asset_price_estimator(ticker, years, plotting=False, monte_carlo_trials=monte_carlo_trials)