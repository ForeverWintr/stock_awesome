import unittest
import random
from operator import itemgetter

from stock_awesome.obj.stock import StockBlock

class StockBlockTest(unittest.TestCase):

    def testStr(self):
        s = StockBlock(10, 50)
        self.assertEqual(repr(s), 'StockBlock(count=10, price=50)')
        self.assertEqual(str(s), '<10 @ 50>')

    def testSort(self):
        t = [(9, 1), (0, 3), (2, 4), (2, 5), (100, 5), (7, 0)]
        random.shuffle(t)
        stocks = [StockBlock(c, p) for p, c in t]

        sortedStocks = sorted(stocks)
        self.assertEqual(sorted(t), [s._key for s in sortedStocks])
