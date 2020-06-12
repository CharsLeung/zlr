# encoding: utf-8

"""
project = 'zlr'
file_name = 'holder'
author = 'Administrator'
datetime = '2020/3/24 0024 上午 11:11'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity, NeoNode


class ShareHolder(BaseEntity):
    """
    股东
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        # ['持股比例', 'HOLDING_RATIO'],
        # ['认缴出资额', 'SUBSCRIPTION_AMOUNT'],
        # ['认缴出资日期', 'SUBSCRIPTION_DATE']
    ]

    synonyms = {
        '股东及出资信息': '名称',
        # '认缴出资额_万元': '认缴出资额',
        '股东链接': '链接'
    }

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(self['URL'])
            if self['URL'] is None:
                if len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = '%s_%s' % (
                        self.label,
                        self.getHashValue(self['NAME'])
                    )
        pass

    def to_pandas(self, nodes, **kwargs):
        return BaseEntity.to_pandas(
            self, nodes, drop_suspicious=True, tolerate=3)
        pass
