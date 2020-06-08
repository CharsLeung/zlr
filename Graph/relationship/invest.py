# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = invest
author = Administrator
datetime = 2020/5/8 0008 下午 18:18
from = office desktop
"""
from Graph.relationship import Base


class Investing(Base):

    """
    投资
    """

    ATTRIBUTES = [
        ['投资比例', 'INVESTING_RATIO'],
        ['投资数额(金额)', 'INVESTING_AMOUNT'],
        ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, enterprise=None, invested=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if invested is None:
                    continue
                if a[0] in invested.keys():
                    properties[a[1]] = invested[a[0]]
                elif a[1] in invested.keys():
                    properties[a[1]] = invested[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        if 'INVESTING_RATIO' in properties.keys():
            try:
                properties['INVESTING_RATIO'] = round(float(
                    properties['INVESTING_RATIO'].replace('%', '')
                ), 4)
            except Exception:
                properties['INVESTING_RATIO'] = None
        Base.__init__(self, enterprise, invested, **properties)
        pass
