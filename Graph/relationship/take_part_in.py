# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = take_part_in
author = Administrator
datetime = 2020/4/8 0008 上午 11:10
from = office desktop
"""
from py2neo import Relationship


class TakePartIn:

    """
    一般意义上的参与、参加
    """
    name = 'TAKE_PART_IN'

    ATTRIBUTES = [
    ]

    def __init__(self, role, item, **kwargs):
        self.role = role
        self.item = item
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in item.keys():
                    self.properties[a[1]] = item[a[0]]
                elif a[1] in item.keys():
                    self.properties[a[1]] = item[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.role,
            self.name,
            self.item,
            **self.properties
        )