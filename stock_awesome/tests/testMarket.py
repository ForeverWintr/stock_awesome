import unittest

from ..obj import market

class MarketTest(unittest.TestCase):

    @unittest.mock.patch('market.requests.get')
    def testGets(self):
        m = market.Market('testaccount', 'testvenue', 'teststock')

        pass
