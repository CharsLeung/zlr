# encoding: utf-8

"""
project = 'zlr'
file_name = 'industry'
author = 'Administrator'
datetime = '2020/3/25 0025 上午 11:00'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class Industry(QccRequest):
    """
    行业
    """

    ATTRIBUTES = [
        ['行业名称', 'NAME']
    ]

    def __init__(self, NAME=None, **kwargs):
        QccRequest.__init__(self)
        self.BaseAttributes['NAME'] = NAME if NAME is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of share holder.')
                    self.BaseAttributes[k] = v
        pass

