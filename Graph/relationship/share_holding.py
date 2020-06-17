# encoding: utf-8

"""
project = 'zlr'
file_name = 'share_holding'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 15:26'
from = 'office desktop' 
"""
from Graph.relationship import Base


class Share(Base):

    """
    持股、拥有股份
    """

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

    def __init__(self, enterprise=None, holder=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if holder is None:
                    continue
                if a[0] in holder.keys():
                    properties[a[1]] = holder[a[0]]
                elif a[1] in holder.keys():
                    properties[a[1]] = holder[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        if 'HOLDING_RATIO' in properties.keys():
            try:
                properties['HOLDING_RATIO'] = round(float(
                    properties['HOLDING_RATIO'].replace('%', '')
                ), 4)
            except Exception:
                properties['HOLDING_RATIO'] = None
        if 'ULTIMATE_RATIO' in properties.keys():
            try:
                properties['ULTIMATE_RATIO'] = round(float(
                    properties['ULTIMATE_RATIO'].replace('%', '')
                ), 4)
            except Exception:
                properties['ULTIMATE_RATIO'] = None
        Base.__init__(self, enterprise, holder, **properties)
        pass