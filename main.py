import run_functions
import yfinance as yf

# Variables
years = 20
monte_carlo_trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'TSLA', 'BTC-USD']
price_init = 1000

if __name__ == "__main__":
    # yf.pdr_override()
    run_functions.best_portfolio_performance_estimator(
        tickers, price_init, years, mc_plotting=False, num_ports=100, monte_carlo_trials=monte_carlo_trials)
    # run_functions.portfolio_performance_estimator(
    #     years, mc_plotting=False, monte_carlo_trials=monte_carlo_trials)
    # run_functions.asset_price_estimator(ticker, years, mc_plotting=False, monte_carlo_trials=monte_carlo_trials)
