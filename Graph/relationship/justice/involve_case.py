# encoding: utf-8

"""
project = 'zlr'
file_name = 'involve_case'
author = 'Administrator'
datetime = '2020/3/26 0026 下午 13:44'
from = 'office desktop' 
"""
from py2neo import Relationship


class InvolveCase:

    """
    涉及、参与，参加xx案件、事例、事件，case一词意味这件事比较
    正式
    """
    name = 'INVOLVE_CASE'

    ATTRIBUTES = [
        # ['案件名称', 'CASE_NAME'],
        # ['案件类型', 'CASE_TYPE'],
        ['案件身份', 'CASE_IDENTITY'],  # 被告、原告等
        # ['案由', 'CASE_ORIGIN'],
        # ['案号', 'CASE_NUM'],
        # ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    def __init__(self, role, case, **kwargs):
        self.role = role
        self.case = case
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if hasattr(case, a[0]):
                    self.properties[a[1]] = case[a[0]]
                elif hasattr(case, a[1]):
                    self.properties[a[1]] = case[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)

    def get_relationship(self):
        return Relationship(
            self.role,
            self.name,
            self.case,
            **self.properties
        )
