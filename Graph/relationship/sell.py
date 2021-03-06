# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = sell_to
author = Administrator
datetime = 2020/4/7 0007 下午 18:35
from = office desktop
"""
from Graph.relationship import Base


class Sell(Base):

    """
    销售...商品
    """

    ATTRIBUTES = [
        # ['销售占比', 'PROPORTION'],
        # ['销售金额', 'AMOUNT'],
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


class SellTo(Base):

    """
    向...销售...
    """

    ATTRIBUTES = [
        # ['销售占比', 'PROPORTION'],
        # ['销售金额', 'AMOUNT'],
    ]

    def __init__(self, sell=None, buy=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if buy is None:
                    continue
                if a[0] in buy.keys():
                    properties[a[1]] = buy[a[0]]
                elif a[1] in buy.keys():
                    properties[a[1]] = buy[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, sell, buy, **properties)
        pass