# encoding: utf-8

"""
project = 'zlr'
file_name = 'invested'
author = 'Administrator'
datetime = '2020/3/26 0026 下午 18:05'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class Invested(BaseEntity):

    """
    被投资企业，对外投资对象不是某个以存在的企业时，新建一个被投资实体
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['注册资本(金额)', 'REGISTERED_CAPITAL_AMOUNT'],
        ['注册资本(单位)', 'REGISTERED_CAPITAL_UNIT'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['经营状态', 'OPERATING_STATUS']
    ]

    synonyms = {
        '状态': '经营状态',
        # '认缴出资额_万元': '认缴出资额',
        # '链接': '股东链接'
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