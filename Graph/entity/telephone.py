# encoding: utf-8

"""
project = 'zlr'
file_name = 'telephone'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 10:18'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class Telephone(BaseEntity):
    """
    电话
    """

    ATTRIBUTES = [
        ['电话', 'TELEPHONE']
    ]

    synonyms = {
        '电话号码': '电话',
        '手机号码': '电话',
        '座机': '电话',
        '号码': '电话'
    }

    primarykey = 'TELEPHONE'

    def __init__(self, telephone=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if telephone is not None and len(str(telephone)) > 1:
            self['TELEPHONE'] = telephone
        pass