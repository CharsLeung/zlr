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
        BaseEntity.__init__(self)
        self.BaseAttributes['TELEPHONE'] = telephone if telephone is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of telephone.')
                    self.BaseAttributes[k] = v
        pass