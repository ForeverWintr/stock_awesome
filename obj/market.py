import os

import requests

import secrets


class Market(object):
    BASE_URL = 'https://api.stockfighter.io/ob/api'
    ORDERS = "{base_url}/venues/{venue}/stocks/{stock}/orders"
    def __init__(self, account, venue, stock):
        """
        A low level interface for the given market (and for now, stock).
        """
        self.account = account
        self.venue = venue
        self.stock = stock
        self.key = secrets.API_KEY

        # How much has been earned/lost since instantiation. In cents.
        self.net_worth = 0
        self.shares_held = 0

        self.orderURL = self.ORDERS.format(base_url=self.BASE_URL, venue=venue, stock=stock)
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

        r = requests.post(self.orderURL, json=order, headers=self.headers)
        r.raise_for_status()
        self._parse_response(r)
        return r

    def stocks(self):
        """
        Return a list of stocks on the given venue.
        """
        r = requests.get('{}/venues/{}/stocks'.format(self.BASE_URL, self.venue))
        r.raise_for_status()
        return r.json()

    def orderbook(self):
        """
        Get the orderbook for this stock.
        """
        r = requests.get('{}/venues/{}/stocks/{}'.format(self.BASE_URL, self.venue, self.stock))
        r.raise_for_status()
        return r.json()

    def quote(self):
        r = requests.get('{}/venues/{}/stocks/{}'.format(self.BASE_URL, self.venue, self.stock))
        r.raise_for_status()
        return r.json()

    def get(self, endpoint, **kwargs):
        """
        Send a get request to the market url + given endpoint.
        """
        return self._request('get', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        r = requests.request(method, '{}/{}'.format(self.BASE_URL, endpoint), **kwargs)
        r.raise_for_status()
        return r

    def _parse_response(self, response):
        """
        Extract info from the given response.
        """
        return response.json()
