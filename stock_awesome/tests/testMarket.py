import unittest
from unittest import mock

from stock_awesome.obj import market

class MockMarketTest(unittest.TestCase):
    """
    Test against a mocked requests object
    """

    def setUp(self):
        self.m = market.StockAPI('testaccount', 'testvenue', 'teststock', 'testkey')

    @mock.patch('stock_awesome.obj.market.requests.request')
    def testGets(self, mocked):
        self.m.orderbook()
        self.assertEqual(
            mocked.call_args,
            mock.call('get',
                      'https://api.stockfighter.io/ob/api/venues/testvenue/stocks/teststock',
                      headers={'X-Starfighter-Authorization': 'testkey'}))

        self.m.all_stocks()
        self.assertEqual(
            mocked.call_args,
            mock.call('get',
                      'https://api.stockfighter.io/ob/api/venues/testvenue/stocks',
                      headers={'X-Starfighter-Authorization': 'testkey'}))

        self.m.quote()
        self.assertEqual(
            mocked.call_args,
            mock.call(
                'get',
                'https://api.stockfighter.io/ob/api/venues/testvenue/stocks/teststock/quote',
                headers={'X-Starfighter-Authorization': 'testkey'}))


    @mock.patch('stock_awesome.obj.market.requests.request')
    def testBuy(self, mocked):
        self.m.buy(1, 2)
        self.assertEqual(
            mocked.call_args,
            mock.call(
                'post',
                'https://api.stockfighter.io/ob/api/venues/testvenue/stocks/teststock/orders',
                headers={'X-Starfighter-Authorization': 'testkey'},
                json={'direction': 'buy', 'qty': 1, 'account': 'testaccount',
                      'symbol': 'teststock', 'orderType': 'limit', 'price': 2,
                      'venue': 'testvenue'})
        )


class RealMarketTest(unittest.TestCase):
    """
    An integration test against the starfighter test api (I wrote this as I was learning the api).
    """

    def testOrderCancel(self):
        m = market.StockAPI('EXB123456', 'TESTEX', 'FOOBAR')

        #place an order
        id_ = m.buy(1, 1)['id']

        #get status of order
        s = m.order_status(id_)
        self.assertEqual(s['direction'], 'buy')
        self.assertEqual(s['id'], id_)
        self.assertEqual(s['ok'], True)
        self.assertEqual(s['open'], True)
        self.assertEqual(s['orderType'], 'limit')

        #cancel the order
        s = m.cancel(id_)
        self.assertEqual(s['direction'], 'buy')
        self.assertEqual(s['id'], id_)
        self.assertEqual(s['ok'], True)
        self.assertEqual(s['open'], False)
        self.assertEqual(s['orderType'], 'limit')

        #buy 10 stocks
        r = m.buy(10, 1, order_type='market')
        self.assertEqual(r['totalFilled'], 10)

