# encoding: utf-8

"""
project = 'zlr'
file_name = 'case'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 17:10'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class RegisterCase(BaseEntity):
    """
    立案信息
    """

    ATTRIBUTES = [
        # ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['立案日期', 'REGISTER_DATE'],
    ]

    primarykey = 'CASE_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of register case.')
                    self.BaseAttributes[k] = v
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            defendant = c.pop('被告人/被告/被上诉人/被申请人')
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            ca = RegisterCase(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, case=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for register case.')
        return obj


class JudicialCase(BaseEntity):
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

    # index = [('CASE_NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
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
        if 'CASE_IDENTITY' in self.BaseAttributes.keys():
            self.CASE_IDENTITY = self.BaseAttributes.pop('CASE_IDENTITY')
        else:
            self.CASE_IDENTITY = None
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
            jcs.append(JudicialCase(**content))
        elif isinstance(content, list):
            for c in content:
                jcs.append(JudicialCase(**c))
        else:
            warnings.warn('invalid type for case content.')

        return jcs


class FinalCase(BaseEntity):
    """
    终本案件
    """

    ATTRIBUTES = [
        # ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['执行法院', 'COURT'],
        ['立案日期', 'REGISTER_DATE'],
        ['终本日期', 'END_DATE'],
    ]

    primarykey = 'CASE_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of register case.')
                    self.BaseAttributes[k] = v
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            # wlx = cls.get_format_amount('未履行金额', c.pop('未履行金额'))
            # zx = cls.get_format_amount('执行标的', c.pop('执行标的'))
            c = dict(c, **cls.get_format_amount('未履行金额', c.pop('未履行金额')))
            c = dict(c, **cls.get_format_amount('执行标的', c.pop('执行标的')))
            return dict(case=FinalCase(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for register case.')
        return obj