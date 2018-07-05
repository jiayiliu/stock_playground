from iexfinance import get_historical_data
import pandas as pd
from datetime import timedelta


def get_history(start_time, end_time, stocks):
    history = {}
    for s in stocks:
        history[s] = get_historical_data(s.upper(), start=start_time, end=end_time, output_format='pandas')
        history[s].index = pd.to_datetime(history[s].index)
    return history


def simulate(start_time, end_time, strategy, portfolio, stocks=(), history=None):
    if history:
        stocks = history.keys()
    else:
        history = get_history(start_time, end_time, stocks)
    today = start_time
    while today <= end_time:
        price_to_day = {s:history[s][history[s].index <= today] for s in stocks}
        actions = strategy.action(price_to_day, stocks, portfolio)
        for s in actions.keys():
            share, price = actions[s]
            portfolio.update(s, price, share)
        today += timedelta(days=1)
    last_price = {s:history[s]["close"].iloc[-1] for s in stocks}
    final_val = portfolio.total_asset(last_price)
    return final_val
