import base_functions

# Variables
days = 365
trials = 10000
tickers = ['GOOGL']

if __name__ == "__main__":
    data = base_functions.import_stock_data(tickers)
    price_df = base_functions.simulate_mc(data, days + 1, 1000)
    base_functions.plot_all_prices(price_df)