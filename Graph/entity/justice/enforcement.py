# encoding: utf-8

"""
project = 'zlr'
file_name = 'executed_person'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 17:26'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class Enforcement(BaseEntity):
    """
    被执行人
    """
    ATTRIBUTES = [
        ['案号', 'CASE_NUM'],
        # ['案号链接', 'URL'],
        # ['执行文号', 'SYMBOL'],
        ['立案日期', 'REGISTER_DATE'],
        ['执行标的(金额)', 'AMOUNT'],
        ['执行标的(单位)', 'UNIT'],
        ['执行法院', 'COURT'],
    ]

    synonyms = {
        # '执行依据文号': '执行文号'
    }

    primarykey = 'CASE_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            # _ = kwargs.pop('案号')
            # self.BaseAttributes[cad['案号名称']] = _['名称']
            # self.BaseAttributes[cad['案号链接']] = _['链接']
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of executed person.')
                    self.BaseAttributes[k] = v
        # if 'URL' in self.BaseAttributes.keys():
        #     self.BaseAttributes['URL'] = self.parser_url(
        #         self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """
        从一个dict或者是dict的list中创建ExecutedPerson对象
        :param content:
        :return: list
        """
        eps = []

        def f(c):
            # del c['序号']
            c = dict(c, **cls.get_format_amount(
                '执行标的', c.pop('执行标的')
            ))
            return dict(executed=Enforcement(**c))
            pass
        if isinstance(content, dict):
            eps.append(f(content))
        elif isinstance(content, list):
            for cnt in content:
                eps.append(f(cnt))
        else:
            warnings.warn('invalid type for ExecutedPerson content.')

        return eps


class SXEnforcement(BaseEntity):
    """
    失信被执行人
    """
    ATTRIBUTES = [
        ['案号', 'CASE_NUM'],
        # ['案号链接', 'URL'],
        ['执行文号', 'SYMBOL'],
        ['立案日期', 'REGISTER_DATE'],
        ['发布日期', 'RELEASE_DATE'],
        ['履行情况', 'EXECUTED_SUBJECT'],
        ['执行法院', 'COURT'],
    ]

    synonyms = {
        '执行依据文号': '执行文号'
    }

    primarykey = 'CASE_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            # _ = kwargs.pop('案号')
            # self.BaseAttributes[cad['案号名称']] = _['名称']
            # self.BaseAttributes[cad['案号链接']] = _['链接']
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of executed person.')
                    self.BaseAttributes[k] = v
        # if 'URL' in self.BaseAttributes.keys():
        #     self.BaseAttributes['URL'] = self.parser_url(
        #         self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """
        从一个dict或者是dict的list中创建ExecutedPerson对象
        :param content:
        :return: list
        """
        eps = []

        def f(c):
            # del c['序号']
            # _ = c.pop('案号')
            # ep = {
            #     '案号': c['执行法院'],
            #     '执行文号': _['案号名称'],
            #     '发布日期': c['省份'],
            #     '执行法院': c['发布日期'],
            #     '履行情况': c['立案日期']
            # }
            return dict(sxexecuted=Enforcement(**c))
            pass

        if isinstance(content, dict):
            eps.append(f(content))
        elif isinstance(content, list):
            for cnt in content:
                eps.append(f(cnt))
        else:
            warnings.warn('invalid type for ExecutedPerson content.')

        return eps
