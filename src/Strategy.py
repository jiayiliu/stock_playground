class BaseStrategy:
    def __init__(self, name="strategy"):
        self.name = name

    def is_buy(self, history_to_date, stocks, portfolio):
        return {}

    def is_sell(self, history_to_date, stocks, portfolio):
        return {}

    def action(self, history_to_date, stocks, portfolio):
        """
        Determine how many stocks to buy / sell, negative shares is sell

        :param history_to_date: History data to *today*
        :param stocks: stock names to track
        :param portfolio: current portfolio
        :return: dict, stock name is key, value is (share, bought price)
        """
        return {}


class BuyDipHold(BaseStrategy):
    """
    Use all money to buy the stock with dip larger than down percent.
    Be aware: this simple demonstration buys the first stock, so no sell.

    :param down_percent: trigger limit to buy
    """
    def __init__(self, down_percent=0.01):
        super().__init__(name="buy and hold")
        self.down_percent = down_percent

    def is_buy(self, history, stocks, portfolio):
        buy_stock = {}
        for stock in stocks:
            h = history[stock]
            if len(h["open"]) < 2:
                continue
            drop = -(h["open"].iloc[-1] - h["close"].iloc[-2]) / h["close"].iloc[-2]
            if drop > self.down_percent:
                share = int(portfolio.balance / h["close"].iloc[-1])
                buy_stock[stock] = (share, h["close"].iloc[-1])
                break  # only buy one stock
        return buy_stock

    def action(self, history_to_date, stocks, portfolio):
        return self.is_buy(history_to_date, stocks, portfolio)
