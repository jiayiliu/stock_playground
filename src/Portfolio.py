class Holding(dict):
    def __init__(self, name, price, share):
        super().__init__()
        self['name'] = name
        self['share'] = share
        self['price'] = price


class Portfolio:
    """
    Create a portfolio with a given balance
    """
    def __init__(self, balance=0):
        self.positions = []
        self.balance = balance

    def total_asset(self, stock_price):
        """
        Return the total value of the portfolio

        :param stock_price:
        :return:
        """
        stock_price = {i.upper():stock_price[i] for i in stock_price}
        total = 0
        for i in self.positions:
            total += stock_price[i['name']] * i['share']
        return total + self.balance

    def update(self, stock, price, share,  FIFO=True):
        stock = stock.upper()
        if share > 0:
            self.balance -= price*share
            bought =  Holding(stock, price, share)
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
                self.positions.append(Holding(stock, price, -share))
                self.balance += share*price
        self.positions = [i for i in self.positions if i is not None]

    def get_position(self):
        return self.positions
