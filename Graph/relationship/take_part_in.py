# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = take_part_in
author = Administrator
datetime = 2020/4/8 0008 上午 11:10
from = office desktop
"""
from Graph.relationship import Base


class TakePartIn(Base):

    """
    一般意义上的参与、参加
    """

    ATTRIBUTES = [
    ]

    def __init__(self, role=None, item=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if item is None:
                    continue
                if a[0] in item.keys():
                    properties[a[1]] = item[a[0]]
                elif a[1] in item.keys():
                    properties[a[1]] = item[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, role, item, **properties)
        pass
