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


def split_case_identity(case_identity):
    ds = []
    names = case_identity['名称']
    urls = case_identity['链接']
    if names is None:
        return []
    names = BaseEntity.textPhrase(names).split(',')
    if urls is None:
        urls = []
    else:
        urls = urls.split(' ')
    if len(names) > len(urls):
        urls = urls + [None for i in range(len(names) - len(urls))]
    for n, u in zip(names, urls):
        ds.append({'名称': n, '链接': u})
    return ds


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
        BaseEntity.__init__(self, **kwargs)
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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
            defendant = split_case_identity(defendant)
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            plaintiff = split_case_identity(plaintiff)
            ca = RegisterCase(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, case=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for register case.')
        return obj

    # @classmethod
    # def split_case_identity(cls, case_identity):
    #     ds = []
    #     names = case_identity['名称']
    #     urls = case_identity['链接']
    #     names = cls.textPhrase(names).split(',')
    #     urls = urls.split(' ')
    #     if len(names) > len(urls):
    #         urls = urls + [None for i in range(len(names) - len(urls))]
    #     for n, u in zip(names, urls):
    #         ds.append({'名称': n, '链接': u})
    #     return ds


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
        BaseEntity.__init__(self, **kwargs)
        if 'CASE_IDENTITY' in self.BaseAttributes.keys():
            self.CASE_IDENTITY = self.BaseAttributes.pop('CASE_IDENTITY')
        else:
            self.CASE_IDENTITY = None
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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
        BaseEntity.__init__(self, **kwargs)
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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