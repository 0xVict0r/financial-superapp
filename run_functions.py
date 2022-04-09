from email.mime import base
import portfolio_functions
import base_functions

def best_portfolio_performance_estimator(tickers, price_init, years, plotting = False, num_ports=10, monte_carlo_trials=100000):
    portfolio_data = portfolio_functions.get_portfolio_data(tickers)
    best_sharpe, best_weights = portfolio_functions.get_best_portfolio(portfolio_data, num_ports)
    mean, vol = portfolio_functions.get_portfolio_hist_perf(portfolio_data, best_weights)
    price_est = base_functions.simulate_mc(price_init, vol, mean, years*252 + 1, monte_carlo_trials, 'Portfolio')
    portfolio_functions.print_portfolio_weights(tickers, best_weights)
    percentile_prices = base_functions.get_percentile_prices(price_est)
    base_functions.plot_percentiles(price_init, percentile_prices, years*252 + 1)
    if plotting:
        base_functions.plot_all_prices(price_est)
        
def portfolio_performance_estimator(years, plotting = False, monte_carlo_trials=100000):
    tickers, weights, init_value = base_functions.get_weights_and_tickers()
    portfolio_data = portfolio_functions.get_portfolio_data(tickers)
    mean, vol = portfolio_functions.get_portfolio_hist_perf(portfolio_data, weights)
    price_est = base_functions.simulate_mc(init_value, vol, mean, years*252 + 1, monte_carlo_trials, 'Portfolio')
    portfolio_functions.print_portfolio_weights(tickers, weights)
    percentile_prices = base_functions.get_percentile_prices(price_est)
    base_functions.plot_percentiles(init_value, percentile_prices, years*252 + 1)
    if plotting:
        base_functions.plot_all_prices(price_est)
        
def asset_price_estimator(ticker, years, plotting = False, monte_carlo_trials=100000):
    mean, vol, init_price = base_functions.get_asset_hist_perf(ticker)
    price_est = base_functions.simulate_mc(init_price, vol, mean, years*252, monte_carlo_trials, ticker)
    base_functions.plot_percentiles(init_price, base_functions.get_percentile_prices(price_est), years*252)
    if plotting:
        base_functions.plot_all_prices(price_est)