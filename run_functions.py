import portfolio_functions
import base_functions

def best_portfolio_performance_estimator(tickers, price_init, years, plotting = False, num_ports=10):
    portfolio_data = portfolio_functions.get_portfolio_data(tickers)
    best_sharpe, best_weights = portfolio_functions.get_best_portfolio(portfolio_data, num_ports)
    mean, vol = portfolio_functions.get_portfolio_hist_perf(portfolio_data, best_weights)
    price_est = base_functions.simulate_mc(price_init, vol, mean, years*252 + 1, 1000, 'Portfolio')
    portfolio_functions.print_portfolio_weights(tickers, best_weights)
    if plotting:
        base_functions.plot_all_prices(price_est)