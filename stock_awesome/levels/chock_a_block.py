import time

from stock_awesome.obj import market



def main():
    """
    Algorithm: Wait for an ask, then send a fill or kill for the quantity of the ask at the ask
    price.
    """
    m = market.StockAPI('WEB29978261', 'NOWUEX', 'BBCM')

    #collection of orders placed
    orders = {}
    filled = 0

    upper_limit = 3300

    #try to buy 100000
    to_send = 1000
    while to_send > 0:
        quote = m.quote()
        ask = quote.get('ask')

        if ask and ask < upper_limit:
            r = m.buy(quote['askSize'], quote['ask'], order_type='fill-or-kill')
            to_send -= 1

            orders[r['id']] = r

            orders = update_orders(m, orders)
            filled += update_filled(orders)
        else:
            time.sleep(1)



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
