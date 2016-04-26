import time

from stock_awesome.obj import market



def main():
    """
    Algorithm: Wait for an ask, then send a fill or kill for the quantity of the ask at the ask
    price.
    """
    m = market.StockAPI('RAJ40214463', 'SSMCEX', 'IPSO')

    #collection of orders placed
    orders = {}
    filled = 0

    upper_limit = 2450

    #try to buy 100000
    to_buy = 100000
    while to_buy > 0:
        quote = m.quote()
        ask = quote.get('ask', 0)
        bid = quote.get('bid')

        if ask < upper_limit:
            r = m.buy(quote['askSize'], ask, order_type='fill-or-kill')
            to_buy -= r['totalFilled']
            print("Bought {}, {} remaining".format(r['totalFilled'], to_buy))

        else:
            time.sleep(1)
    print('done')


def update_orders(m, orders):
    """
    update order status
    """
    return {o: m.order_status(o) for o in orders}

def update_filled(orders):
    """
    Remove filled orders and update our count.
    """
    closed = [o for o in orders if not orders[o]['open']]

    #remove and sum filled orders
    filled = sum(orders.pop(o)['totalFilled'] for o in closed)

    return filled


if __name__ == '__main__':
    main()
