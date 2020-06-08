# encoding: utf-8

"""
project = 'zlr'
file_name = 'defendant'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 11:21'
from = 'office desktop' 
"""
from Graph.relationship import Base


class Defendant(Base):

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件类型', 'CASE_TYPE'],
        # ['案件身份', 'CASE_IDENTITY'],  # 被告、原告
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    def __init__(self, defendant, case, **kwargs):
        Base.__init__(self, defendant, case, **kwargs)
        pass