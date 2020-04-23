# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = purchase
author = Administrator
datetime = 2020/4/7 0007 下午 18:37
from = office desktop
"""
from py2neo import Relationship


class Purchase:

    """
    从。。。购买、采购。。。
    """

    name = 'BUY_FROM'

    ATTRIBUTES = [
        ['采购占比', 'PROPORTION'],
        ['采购金额', 'AMOUNT'],
    ]

    def __init__(self, buy, sell, **kwargs):
        self.buy = buy
        self.sell = sell
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in sell.keys():
                    self.properties[a[1]] = sell[a[0]]
                elif a[1] in sell.keys():
                    self.properties[a[1]] = sell[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.buy,
            self.name,
            self.sell,
            **self.properties
        )