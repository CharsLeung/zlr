# encoding: utf-8

"""
project = 'zlr'
file_name = 'case'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 17:10'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class JusticeCase(QccRequest):
    """
    司法案件，案号作为id属性
    """

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件类型', 'CASE_TYPE'],
        ['案件身份', 'CASE_IDENTITY'],  # 这一属性应体现到关系属性当中去
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    primarykey = 'CASE_NUM'

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

    @classmethod
    def create_from_dict(cls, content):
        """
        从一个dict或者是dict的list中创建JusticeCase对象
        :param content:
        :return: list
        """
        jcs = []
        if isinstance(content, dict):
            jcs.append(JusticeCase(**content))
        elif isinstance(content, list):
            for c in content:
                jcs.append(JusticeCase(**c))
        else:
            warnings.warn('invalid type for case content.')

        return jcs
