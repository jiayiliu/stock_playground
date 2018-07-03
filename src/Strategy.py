class BaseStrategy:
    def __init__(self, name="strategy"):
        self.name = name

    def is_buy(self, history_to_date, stock, portfolio):
        pass

    def is_sell(self, history_to_date, stock, portfolio):
        pass


class BuyDipHold(BaseStrategy):
    def __init__(self, down_percent=0.01):
        super().__init__(name="buy and hold")
        self.down_percent = down_percent

    def is_buy(self, history, stock, portfolio):
        history = history[stock]
        if len(history["open"]) < 2:
            return 0, 0
        drop = -(history["open"].iloc[-1] - history["close"].iloc[-2]) / history["close"].iloc[-2]
        if drop > self.down_percent:
            share = portfolio.balance / history["close"].iloc[-1]
            return share, history["close"].iloc[-1]
        else:
            return 0, 0

    def is_sell(self, history_to_date, stock, portfolio):
        return 0, 0
