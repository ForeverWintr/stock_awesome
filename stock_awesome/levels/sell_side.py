import time

# A simple strategy might be:
  # Pick a target value. If ask is below it, buy, if bid is above it, sell.
    # How do you pick a target value? -average?
    # Note average ask, bid, open
    #start by using the order book. average closed trade price
#Can you guess someone's target price by spamming increasing asks?


class SimpleMarketMaker(object):
    def __init__(self, api):
        self.api = api
        self.net = 0
        self.shares = 0
        self.avg_price = 0
        self.trades_seen = 0

    def run(self):
        """
        Get the orderbook, analyze it, place/adjust orders.
        """
        self._initial_poll()
        pass

    def _initial_poll(self, trade_count=20):
        """
        Do some initial polling to establish baseline average price.
        """
        last_trade_sig = None
        initial_orders_seen = 0
        while initial_orders_seen < trade_count:
            q = self.api.quote()

            sig = tuple(q.get(k) for k in ('lastTrade', 'lastSize', 'last'))
            if sig != last_trade_sig:
                last_trade_sig = sig
                initial_orders_seen += 1
                self._process_quote(q)
            else:
                time.sleep(1)
                print('Init poll sleeping')


    def _process_quote(self, quote):
        """
        Ingest a quote.
        """
        total_price = self.avg_price * self.trades_seen
        self.trades_seen += quote['lastSize']
        self.avg_price = (total_price + quote['last']) / self.trades_seen

if __name__ == '__main__':
    from stock_awesome.obj.market import StockAPI

    api = StockAPI('WWS52018499', 'VSIPEX', 'HBH')
    market_maker = SimpleMarketMaker(api)
    market_maker.run()
