# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = appraise
author = Administrator
datetime = 2020/5/11 0011 上午 11:00
from = office desktop
"""
from Graph.relationship import Base


class Appraise(Base):

    """
    评价、评级
    """

    ATTRIBUTES = [
        # ['投资比例', 'INVESTING_RATIO'],
        # ['投资数额(金额)', 'INVESTING_AMOUNT'],
        # ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, appraiser=None, etp=None, **kwargs):
        # self.etp = etp
        # self.appraiser = appraiser
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if etp is None:
                    continue
                if a[0] in etp.keys():
                    properties[a[1]] = etp[a[0]]
                elif a[1] in etp.keys():
                    properties[a[1]] = etp[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, appraiser, etp, **properties)
        pass