# encoding: utf-8

"""
project = 'zlr'
file_name = 'share_holding'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 15:26'
from = 'office desktop' 
"""
from py2neo import Relationship


class ShareHolding:

    name = 'SHARE_HOLDING'

    ATTRIBUTES = [
        # ['股东名称', 'SHARE_HOLDER_NAME'],
        # ['股东链接', 'SHARE_HOLDER_URL'],
        ['持股比例', 'HOLDING_RATIO'],
        ['认缴出资额', 'SUBSCRIPTION_AMOUNT'],
        ['认缴出资日期', 'SUBSCRIPTION_DATE']
    ]

    def __init__(self, holder, enterprise, **kwargs):
        self.holder = holder
        self.enterprise = enterprise
        self.properties = kwargs
        for a in self.ATTRIBUTES:
            if a[1] not in kwargs.keys():
                self.properties[a[1]] = holder[a[1]]
        pass

    def get_relationship(self):
        return Relationship(
            self.holder,
            self.name,
            self.enterprise,
            **self.properties
        )