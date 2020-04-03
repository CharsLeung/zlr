# encoding: utf-8

"""
project = 'zlr'
file_name = 'executed_person'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 17:26'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest, NeoNode


class ExecutedPerson(QccRequest):
    ATTRIBUTES = [
        ['案号名称', 'CASE_NAME'],
        ['案号链接', 'URL'],
        ['立案日期', 'CASE_REGISTER_DATE'],
        ['执行标的', 'CASE_EXECUTED_SUBJECT'],
        ['执行法院', 'CASE_EXECUTED_COURT'],
    ]

    def __init__(self, **kwargs):
        QccRequest.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            _ = kwargs.pop('案号')
            self.BaseAttributes[cad['案号名称']] = _['名称']
            self.BaseAttributes[cad['案号链接']] = _['链接']
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of executed person.')
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass
