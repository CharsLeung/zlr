# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = branch
author = Administrator
datetime = 2020/5/9 0009 上午 9:25
from = office desktop
"""
from Graph.relationship import Base


class BranchAgency(Base):

    """
    分支机构
    """

    ATTRIBUTES = [
        ['状态', 'STATUS'],
        # ['投资数额(金额)', 'INVESTING_AMOUNT'],
        # ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, enterprise=None, branch=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if branch is None:
                    continue
                if a[0] in branch.keys():
                    properties[a[1]] = branch[a[0]]
                elif a[1] in branch.keys():
                    properties[a[1]] = branch[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, enterprise, branch, **properties)
        pass
