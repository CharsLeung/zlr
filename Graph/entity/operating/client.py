# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = client
author = Administrator
datetime = 2020/4/7 0007 下午 17:41
from = office desktop
"""
import warnings
import pandas as pd

from Graph.entity import BaseEntity


class Client(BaseEntity):

    """
    客户
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['销售占比', 'PROPORTION'],
        ['销售金额', 'AMOUNT'],
        ['报告期', 'REPORT_DATE'],
        ['数据来源', 'SOURCE']
    ]

    synonyms = {
        '销售金额_万元': '销售金额',
        # '链接': '标的链接'
    }

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(
                self['URL'])
            if self['URL'] is None:
                if len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = 'Client_%s' % self.getHashValue(
                        self['NAME'])
        pass

    def to_pandas(self, nodes, **kwargs):
        return BaseEntity.to_pandas(
            self, nodes, drop_suspicious=True, tolerate=3)
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(_):
            c = _.pop('客户')
            if '销售金额' in _.keys():
                _ = dict(_, **cls.get_format_amount(
                    '销售金额', _.pop('销售金额')
                ))
            return dict(client=Client(**c), **_)

        # def f(c):
        #     # del c['序号']
        #     _ = c.pop('客户')
        #     c['客户名称'] = _['名称']
        #     c['客户链接'] = _['链接']
        #     return c

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for client content.')
        return obj