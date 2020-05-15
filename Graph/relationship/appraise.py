# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = appraise
author = Administrator
datetime = 2020/5/11 0011 上午 11:00
from = office desktop
"""
from py2neo import Relationship


class Appraise:

    """
    评价、评级
    """

    name = 'APPRAISE'

    ATTRIBUTES = [
        # ['投资比例', 'INVESTING_RATIO'],
        # ['投资数额(金额)', 'INVESTING_AMOUNT'],
        # ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, appraiser, etp, **kwargs):
        self.etp = etp
        self.appraiser = appraiser
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in etp.keys():
                    self.properties[a[1]] = etp[a[0]]
                elif a[1] in etp.keys():
                    self.properties[a[1]] = etp[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)
        pass

    def get_relationship(self):
        return Relationship(
            self.appraiser,
            self.name,
            self.etp,
            **self.properties
        )