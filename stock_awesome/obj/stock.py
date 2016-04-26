import locale

from stock_awesome.obj.mixins import CompareKeyMixin


class StockBlock(CompareKeyMixin):
    def __init__(self, count=0, price=0):
        """
        A stock block is a group of shares and their average price. You can add two stockblocks,
        and the resulting stockblock's price will update accordingly. StockBlocks are sortable
        based on price, then count
        """
        self.count = count
        self.price = price

    @property
    def _key(self):
        return (self.price, self.count)

    def __repr__(self):
        return "{}(count={}, price={})".format(self.__class__.__name__, self.count, self.price)

    def __str__(self):
        return "<{} @ {}>".format(self.count, self.price)


