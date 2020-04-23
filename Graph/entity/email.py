# encoding: utf-8

"""
project = 'zlr'
file_name = 'email'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 10:44'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class Email(QccRequest):
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
        QccRequest.__init__(self)
        self.BaseAttributes['EMAIL'] = email if email is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of email.')
                    self.BaseAttributes[k] = v
        self.__split_levels__()
        pass

    def __split_levels__(self):
        if self.BaseAttributes['EMAIL'] is None:
            self.BaseAttributes['ACCOUNT'] = None
            self.BaseAttributes['SERVER'] = None
        else:
            _ = self.BaseAttributes['EMAIL'].split('@')
            if len(_) > 1:
                self.BaseAttributes['ACCOUNT'] = _[0]
                self.BaseAttributes['SERVER'] = _[1]
            else:
                self.BaseAttributes['ACCOUNT'] = None
                self.BaseAttributes['SERVER'] = None
        pass