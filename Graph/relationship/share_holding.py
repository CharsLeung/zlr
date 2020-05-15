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

    """
    持股、拥有股份
    """

    name = 'SHARE_HOLDING'

    ATTRIBUTES = [
        ['持股比例', 'HOLDING_RATIO'],
        ['认缴出资额(金额)', 'SUBSCRIPTION_AMOUNT'],
        ['认缴出资额(单位)', 'SUBSCRIPTION_UNIT'],
        ['认缴出资日期', 'SUBSCRIPTION_DATE'],
        ['实缴出资额(金额)', 'REALITY_SUBSCRIPTION_AMOUNT'],
        ['实缴出资额(单位)', 'REALITY_SUBSCRIPTION_UNIT'],
        ['实缴出资日期', 'REALITY_SUBSCRIPTION_DATE'],
        ['最终受益股份', 'ULTIMATE_RATIO']
    ]

    def __init__(self, holder, enterprise, **kwargs):
        self.holder = holder
        self.enterprise = enterprise
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in holder.keys():
                    self.properties[a[1]] = holder[a[0]]
                elif a[1] in holder.keys():
                    self.properties[a[1]] = holder[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)
        pass

    def get_relationship(self):
        return Relationship(
            self.holder,
            self.name,
            self.enterprise,
            **self.properties
        )