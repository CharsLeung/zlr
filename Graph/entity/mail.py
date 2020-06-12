# encoding: utf-8

"""
project = 'zlr'
file_name = 'email'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 10:44'
from = 'office desktop' 
"""
import warnings

from Graph.entity import BaseEntity


class Email(BaseEntity):
    """
    邮箱
    """

    ATTRIBUTES = [
        ['邮箱', 'EMAIL']
    ]

    synonyms = {
        'e-mail': '邮箱',
        'E-MAIL': '邮箱',
    }

    primarykey = 'EMAIL'

    def __init__(self, email=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if email is not None and len(email) > 1:
            self['EMAIL'] = email
        self.__split_levels__()
        pass

    def __split_levels__(self):
        if self.BaseAttributes.get('EMAIL') is None:
            self['ACCOUNT'] = None
            self['SERVER'] = None
        else:
            _ = self['EMAIL'].split('@')
            if len(_) > 1:
                self['ACCOUNT'] = _[0]
                self['SERVER'] = _[1]
            else:
                self['ACCOUNT'] = None
                self['SERVER'] = None
        pass