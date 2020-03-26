# encoding: utf-8

"""
project = 'zlr'
file_name = 'website'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 10:52'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class Website(QccRequest):

    ATTRIBUTES = [
        ['官网', 'WEBSITE']
    ]

    synonyms = {
        '官方网站': '官网',
        # 'E-MAIL': '邮箱',
    }

    def __init__(self, website=None, **kwargs):
        QccRequest.__init__(self)
        self.BaseAttributes['WEBSITE'] = website if website is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of website.')
                    self.BaseAttributes[k] = v
        pass

    def __split_levels__(self):
        pass