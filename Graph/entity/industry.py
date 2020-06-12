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
        ['行业名称', 'NAME'],
        ['行业代码', 'CODE']
    ]

    def __init__(self, name=None, code=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        self['NAME'] = name if name is not None else None
        self['CODE'] = code if code is not None else None
        pass

