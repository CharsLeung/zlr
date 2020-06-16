# encoding: utf-8

"""
project = 'zlr'
file_name = 'industry'
author = 'Administrator'
datetime = '2020/3/25 0025 上午 11:00'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class Industry(BaseEntity):
    """
    行业
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['代码', 'CODE'],
        ['类别', 'TYPE']
    ]

    synonyms = {
        '行业': '行业',
        '行业名称': '行业',
        'Industry': '行业',
        '行业代码': '代码',
        'IndustryCode': '代码',
    }

    primarykey = 'CODE'
    index = [('NAME', )]

    def __init__(self, name=None, code=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if name is not None:
            self['NAME'] = name
        if code is not None:
            self['CODE'] = code
        pass


