# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = sell_to
author = Administrator
datetime = 2020/4/7 0007 下午 18:35
from = office desktop
"""
from py2neo import Relationship


class Sell:

    """
    销售...商品
    """

    name = 'SELL'

    ATTRIBUTES = [
        # ['销售占比', 'PROPORTION'],
        # ['销售金额', 'AMOUNT'],
    ]

    def __init__(self, enterprise, thing, **kwargs):
        self.enterprise = enterprise
        self.thing = thing
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in thing.keys():
                    self.properties[a[1]] = thing[a[0]]
                elif a[1] in thing.keys():
                    self.properties[a[1]] = thing[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.enterprise,
            self.name,
            self.thing,
            **self.properties
        )
        pass


class SellTo:

    """
    向...销售...
    """

    name = 'SELL_TO'

    ATTRIBUTES = [
        ['销售占比', 'PROPORTION'],
        ['销售金额', 'AMOUNT'],
    ]

    def __init__(self, sell, buy, **kwargs):
        self.sell = sell
        self.buy = buy
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in buy.keys():
                    self.properties[a[1]] = buy[a[0]]
                elif a[1] in buy.keys():
                    self.properties[a[1]] = buy[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.sell,
            self.name,
            self.buy,
            **self.properties
        )
        pass