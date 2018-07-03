import unittest
from Strategy import BuyDipHold
from Portfolio import Portfolio
import pandas as pd

class TestStrategy(unittest.TestCase):

    def test_buydiphold(self):
        stat = BuyDipHold(down_percent=0.1)
        port = Portfolio(120)
        stock_prices = {"A":pd.DataFrame({"close":[10, 12],"open":[8, 8]}),
                            "B":pd.DataFrame({"close": [10, 12],"open": [11, 11]})}
        self.assertEqual(stat.is_buy(stock_prices, "A", port), 10)
        self.assertEqual(stat.is_buy(stock_prices, "B", port), 0)
        self.assertEqual(stat.is_sell(stock_prices, "A", port), 0)


if __name__ == '__main__':
    unittest.main()
