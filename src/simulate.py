"""
Investment strategy simulation
===============================

Author: Jiayi (Jason) Liu
Date: July 8, 2018

"""

import logging

logger = logging.getLogger(__name__)

from datetime import timedelta

from .utils import get_history


def simulate(start_time, end_time, strategy, portfolio, stocks=(), history=None):
    """
    Simulate stock trading

    :param start_time: starting date of the simulation
    :param end_time: ending date of the simulation
    :param strategy: :class:Strategy to be used
    :param portfolio: :class:Portfolio
    :param stocks: monitoring stocks
    :param history: if provided, use the history directly, otherwise, will download the history automatically.
    :return: final value if all stocks are sold at the last day
    """
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
            portfolio.update(s, price, share, today)
        today += timedelta(days=1)
    last_price = {s:history[s]["close"].iloc[-1] for s in stocks}
    final_val = portfolio.total_asset(last_price)
    return final_val, portfolio
