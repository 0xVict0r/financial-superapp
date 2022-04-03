import run_functions
import numpy as np

# Variables
years = 1
trials = 10000
ticker = 'FB'
tickers = ['AAPL', 'MSFT', 'BTC-USD']
weights = np.array([0.1, 0.5, 0.4])
price_init = 1000

if __name__ == "__main__":
    run_functions.asset_price_estimator(ticker, years, plotting = True)