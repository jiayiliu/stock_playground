"""
Portfolio management
====================

Author: Jiayi (Jason) Liu
Date: July 8, 2018

"""

import logging

logger = logging.getLogger(__name__)


class _Holding(dict):
    """
    Holding of a stock

    :param name: stock name
    :param share: number of share, negative number for short.
    :param price: trade price
    :param date: trade date
    """
    def __init__(self, name, price, share, date):
        super().__init__()
        self['name'] = name
        self['share'] = share
        self['price'] = price
        self['date'] = date


class Portfolio:
    """
    Create a portfolio with a given balance

    """
    def __init__(self, balance=0):
        self.__positions = []
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

    def update(self, stock, price, share, date, FIFO=True):
        """
        Update the portfolio

        :param stock: stock name
        :param price: price of the stock
        :param share: number of shares to execute - negative number for sell
        :param date: not used
        :param FIFO: accounting for FIFO or FILO
        :return: self
        """
        if share > 0:
            self.balance -= price*share
            bought = _Holding(stock, price, share, date)
            if FIFO:
                self.positions.append(bought)
            else:
                self.positions.insert(0, bought)
        else: # sell
            share = -share
            seq = range(len(self.positions)) if FIFO else range(len(self.positions) - 1, -1, -1)
            for i in seq:
                if self.positions[i]['name'] == stock:
                    if self.positions[i]['share'] > share:
                        self.positions[i]['share'] -= share
                        self.balance += share*price
                        share = 0
                        break
                    else:
                        self.balance += self.positions[i]['share'] * price
                        share -= self.positions[i]['share']
                        self.positions[i] = None
            if share > 0:
                self.positions.append(_Holding(stock, price, -share, date))
                self.balance += share*price
        # remove stock no longer holds
        self.positions = [i for i in self.positions if i is not None]
        return self
