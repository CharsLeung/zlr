# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = apply_bankrupt
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/8 0008 上午 10:57
@from = office desktop
"""
from Graph.relationship import Base


class ApplyBankrupt(Base):

    """
    申请破产
    """

    ATTRIBUTES = [
        # ['投资比例', 'INVESTING_RATIO'],
        # ['投资数额(金额)', 'INVESTING_AMOUNT'],
        # ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, applicant=None, etp=None, **kwargs):
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
        Base.__init__(self, applicant, etp, **properties)
        pass