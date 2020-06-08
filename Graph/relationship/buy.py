# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = purchase
author = Administrator
datetime = 2020/4/7 0007 下午 18:37
from = office desktop
"""
from Graph.relationship import Base


class Buy(Base):

    """
    购买、采购...
    """

    ATTRIBUTES = [
        # ['采购占比', 'PROPORTION'],
        # ['采购金额', 'AMOUNT'],
    ]

    def __init__(self, enterprise=None, thing=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if thing is None:
                    continue
                if a[0] in thing.keys():
                    properties[a[1]] = thing[a[0]]
                elif a[1] in thing.keys():
                    properties[a[1]] = thing[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, enterprise, thing, **properties)
        pass


class BuyFrom(Base):

    """
    从...购买、采购...
    """

    ATTRIBUTES = [
        # ['采购占比', 'PROPORTION'],
        # ['采购金额', 'AMOUNT'],
    ]

    def __init__(self, buy=None, sell=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if sell is None:
                    continue
                if a[0] in sell.keys():
                    properties[a[1]] = sell[a[0]]
                elif a[1] in sell.keys():
                    properties[a[1]] = sell[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, buy, sell, **properties)
        pass