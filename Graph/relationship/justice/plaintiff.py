# encoding: utf-8

"""
project = 'zlr'
file_name = 'plaintiff'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 11:28'
from = 'office desktop' 
"""
from py2neo import Relationship


class Plaintiff:

    name = 'Plaintiff'

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件类型', 'CASE_TYPE'],
        # ['案件身份', 'CASE_IDENTITY'],  # 被告、原告
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    def __init__(self, plaintiff, case, **kwargs):
        self.plaintiff = plaintiff
        self.case = case
        self.properties = kwargs
        for a in self.ATTRIBUTES:
            if a[1] not in kwargs.keys():
                self.properties[a[1]] = case[a[1]]

    def get_relationship(self):
        return Relationship(
            self.plaintiff,
            self.name,
            self.case,
            **self.properties
        )