# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = branch
author = Administrator
datetime = 2020/5/9 0009 上午 9:25
from = office desktop
"""
from py2neo import Relationship


class BranchAgency:

    """
    分支机构
    """

    name = 'BRANCH_AGENCY'

    ATTRIBUTES = [
        # ['投资比例', 'INVESTING_RATIO'],
        # ['投资数额(金额)', 'INVESTING_AMOUNT'],
        # ['投资数额(单位)', 'INVESTING_UNIT'],
    ]

    def __init__(self, enterprise, branch, **kwargs):
        self.branch = branch
        self.enterprise = enterprise
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in branch.keys():
                    self.properties[a[1]] = branch[a[0]]
                elif a[1] in branch.keys():
                    self.properties[a[1]] = branch[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)
        pass

    def get_relationship(self):
        return Relationship(
            self.enterprise,
            self.name,
            self.branch,
            **self.properties
        )