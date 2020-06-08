# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = guaranty
author = Administrator
datetime = 2020/4/8 0008 下午 16:14
from = office desktop
"""
from Graph.relationship import Base


class Guaranty(Base):

    """
    抵押...
    """

    ATTRIBUTES = [
        # ['销售占比', 'PROPORTION'],
        # ['销售金额', 'AMOUNT'],
    ]

    def __init__(self, owner=None, possession=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if possession is None:
                    continue
                if a[0] in possession.keys():
                    properties[a[1]] = possession[a[0]]
                elif a[1] in possession.keys():
                    properties[a[1]] = possession[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, owner, possession, **properties)
        pass