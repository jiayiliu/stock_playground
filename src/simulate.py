"""
Investment strategy simulation
===============================

Author: Jiayi (Jason) Liu
Date: July 8, 2018

"""

import logging

from Position import LongOnlyPosition

logger = logging.getLogger(__name__)

from datetime import timedelta

from .utils import get_history


def simulate(strategy, portfolio, history, stocks=(), fp=None):
    """
    Simulate stock trading

    :param strategy: :class:Strategy to be used
    :param portfolio: :class:Portfolio
    :param stocks: monitoring stocks
    :param history: historical stock data create by `get_history(start_time, end_time, stocks)`
    :return: final value if all stocks are sold at the last day
    """
    stocks = list(history.keys())
    if not stocks:
        exit(1)
    # locate start_time and end_time
    start_time = history[stocks[0]].index[0]
    end_time = history[stocks[0]].index[-1]
    for s in stocks[1:]:
        if history[s].index[0] < start_time:
            start_time = history[s].index[0]
        if history[s].index[-1] > end_time:
            end_time = history[s].index[-1]

    today = start_time
    while today <= end_time:
        price_to_today = {s:history[s][history[s].index <= today] for s in stocks}
        actions = strategy.action(price_to_today, stocks, portfolio)
        for s in actions.keys():
            action, share, price = actions[s]
            portfolio.update(s, action, price, share, today)
            if fp:
                fp.write("%s:%s:%s:$%f:%f" % (today, action, s, price, share))
        today += timedelta(days=1)
    last_price = {s:history[s]["close"].iloc[-1] for s in stocks}
    final_val = portfolio.total_asset(last_price)
    return final_val, portfolio


class Portfolio:
    """
    Create a portfolio with a given balance

    """
    def __init__(self, position=LongOnlyPosition(), balance=0):
        self.__positions = position
        self.__balance = balance

    def __repr__(self):
        return_str = super().__repr__()
        return_str += "\nCurrent Cash Balance: %f\n" % self.balance
        return_str += "\n".join([p.__str__() for p in self.positions])
        return return_str

    @property
    def balance(self):
        """
        :return: current cash balance
        """
        return self.__balance

    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance

    @property
    def positions(self):
        """
        :return: current holdings
        """
        return self.__positions

    @positions.setter
    def positions(self, positions):
        self.__positions = positions

    def total_asset(self, stock_price):
        """
        Return the total value of the portfolio

        :param stock_price: {"stock":price} dictionary
        :return: valuation of the current portfolio
        """
        stock_price = {i.upper():stock_price[i] for i in stock_price}
        total = 0
        for i in self.positions:
            total += stock_price[i['name']] * i['share']
        return total + self.balance

    def update(self, stock, action, price, share, date):
        """
        Update the portfolio

        :param stock: stock name
        :param action: open / close
        :param price: price of the stock
        :param share: number of shares to execute - negative number for sell
        :param date: not used
        :param close: open or close position, default is to open
        :param FIFO: accounting for FIFO or FILO
        :return: self
        """
        if action == "close":
            self.positions.close(stock, price, share, date)
        elif action == "open":
            self.positions.open(stock, price, share, date)
        else:
            raise Exception("Wrong action %s" % action)