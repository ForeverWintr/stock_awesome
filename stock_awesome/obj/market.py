import os

import requests

from stock_awesome import secrets


class StockAPI(object):
    BASE_URL = 'https://api.stockfighter.io/ob/api'
    def __init__(self, account, venue, stock, api_key=secrets.API_KEY):
        """
        A low level interface for the given stock and market.
        """
        self.account = account
        self.venue = venue
        self.stock = stock
        self.key = api_key

        self.headers = {'X-Starfighter-Authorization': self.key}

    def buy(self, qty, price, order_type='limit'):
        """
        Place a buy order and return the result.
        """
        order = {
            "account": self.account,
            "venue": self.venue,
            "symbol": self.stock,
            "price": price,
            "qty": qty,
            "direction": "buy",
            "orderType": order_type,
        }

        r = self._request('post', 'stocks/{}/orders'.format(self.stock), json=order)
        return r.json()

    def all_stocks(self):
        """
        Return a list of stocks on the given venue.
        """
        r = self.get('stocks')
        return r.json()

    def orderbook(self):
        """
        Get the orderbook for this stock.
        """
        r = self.get('stocks/{}'.format(self.stock))
        return r.json()

    def quote(self):
        """
        Get a quick look at the most recent trade information for a stock.
        """
        r = self.get('stocks/{}/quote'.format(self.stock))
        return r.json()

    def order_status(self, orderId=None):
        """
        Get the status of the given order id.
        """
        r = self.get('stocks/{}/orders/{!s}'.format(self.stock, orderId))
        return r.json()

    def orders(self, account=None):
        """
        Retrieve all orders associated with this account (try another account if you want).
        """
        if account is None:
            account = self.account
        return self.get('accounts/{}/orders'.format(account)).json()

    def cancel(self, orderId):
        """
        Cancel the given order ID
        """
        r = self._request('delete', 'stocks/{}/orders/{!s}'.format(self.stock, orderId))
        return r.json()

    def get(self, endpoint, **kwargs):
        """
        Send a get request to the market url + given endpoint.
        """
        return self._request('get', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        """
        Format a request to our current base url and venue.
        """
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)

        r = requests.request(method, '{}/venues/{}/{}'.format(
            self.BASE_URL, self.venue, endpoint), headers=headers, **kwargs)
        r.raise_for_status()
        return r
