# encoding: utf-8

"""
project = 'zlr'
file_name = 'case'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 17:10'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest, NeoNode


class JusticeCase(QccRequest):

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件类型', 'CASE_TYPE'],
        ['案件身份', 'CASE_IDENTITY'],  # 被告、原告
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    def __init__(self, **kwargs):
        QccRequest.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of justice case.')
        pass

    def get_neo_node(self):
        return NeoNode(
            'justice_case',
            **self.BaseAttributes
        )