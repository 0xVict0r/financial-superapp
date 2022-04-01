import base_functions
import portfolio_functions

# Variables
days = 365
trials = 10000
ticker = ['FB']

if __name__ == "__main__":
    data = base_functions.import_stock_data(ticker)
    price_est = base_functions.simulate_mc(data, days + 1, 1000)
    base_functions.plot_all_prices(price_est)
    sharpe, sortino, calmar = portfolio_functions.get_performance_ratios(ticker)