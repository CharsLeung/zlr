# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = supplier
author = Administrator
datetime = 2020/4/7 0007 下午 17:53
from = office desktop
"""
import warnings
import pandas as pd

from Graph.entity import BaseEntity


class Supplier(BaseEntity):

    """
    供应商
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
    ]

    synonyms = {
        '供应商链接': '链接',
        '供应商名称': '名称'
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
                    self['URL'] = 'Supplier_%s' % self.getHashValue(
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
            # del c['序号']
            c = _.pop('供应商')
            if '采购金额' in _.keys():
                _ = dict(_, **cls.get_format_amount(
                    '采购金额', _.pop('采购金额')
                ))
            return dict(supplier=Supplier(**c), **_)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for supplier content.')
        return obj