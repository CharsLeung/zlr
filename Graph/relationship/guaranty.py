# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = guaranty
author = Administrator
datetime = 2020/4/8 0008 下午 16:14
from = office desktop
"""
from py2neo import Relationship


class Guaranty:

    """
    抵押...
    """

    name = 'GUARANTY'

    ATTRIBUTES = [
        # ['销售占比', 'PROPORTION'],
        # ['销售金额', 'AMOUNT'],
    ]

    def __init__(self, owner, possession, **kwargs):
        self.owner = owner
        self.possession = possession
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if hasattr(possession, a[0]):
                    self.properties[a[1]] = possession[a[0]]
                elif hasattr(possession, a[1]):
                    self.properties[a[1]] = possession[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.owner,
            self.name,
            self.possession,
            **self.properties
        )
        pass