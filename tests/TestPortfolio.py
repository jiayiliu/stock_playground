import unittest
from Portfolio import Portfolio

from datetime import datetime


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.portfolio = Portfolio(1000)

    def test_create(self):
        self.assertEqual(self.portfolio.total_asset({}), 1000)

    def test_buy(self):
        self.portfolio.update("AMZN", 100, 10, datetime.now())
        pos = self.portfolio.positions
        self.assertEqual(pos[0]["name"], "AMZN")
        self.assertEqual(pos[0]['price'], 100)
        self.assertEqual(pos[0]['share'], 10)
        self.assertEqual(self.portfolio.balance, 0)
        self.assertEqual(self.portfolio.total_asset({"amzn": 80}),
                         800)

    def test_sell(self):
        # buy $100x10share -> $0 balance
        self.portfolio.update("AMZN", 100, 10, datetime.now())
        self.portfolio.update("AMZN", 50, -5, datetime.now()) # sell $50x5share -> $250
        pos = self.portfolio.positions
        self.assertEqual(pos[0]["name"], "AMZN")
        self.assertEqual(pos[0]['price'], 100)  # bought price
        self.assertEqual(pos[0]['share'], 5)
        self.assertEqual(self.portfolio.balance, 250)
        self.assertEqual(self.portfolio.total_asset({"amzn": 80}), 650) # $80x5shares + 250
        self.portfolio.update("AMZN", 120, -5, datetime.now())
        self.assertEqual(self.portfolio.positions, [])

    def test_shortsell(self):
        self.portfolio.update("AMZN", 100, 5, datetime.now())
        self.portfolio.update("AMZN", 200, -15, datetime.now())
        pos = self.portfolio.positions
        self.assertEqual(pos[0]["name"], "AMZN")
        self.assertEqual(pos[0]['price'], 200)  # bought price
        self.assertEqual(pos[0]['share'], -10)


if __name__ == '__main__':
    unittest.main()
