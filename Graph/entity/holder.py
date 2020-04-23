# encoding: utf-8

"""
project = 'zlr'
file_name = 'holder'
author = 'Administrator'
datetime = '2020/3/24 0024 上午 11:11'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest, NeoNode


class ShareHolder(QccRequest):
    """
    股东
    """

    ATTRIBUTES = [
        ['股东名称', 'NAME'],
        ['股东链接', 'URL'],
        ['持股比例', 'HOLDING_RATIO'],
        ['认缴出资额', 'SUBSCRIPTION_AMOUNT'],
        ['认缴出资日期', 'SUBSCRIPTION_DATE']
    ]

    synonyms = {
        '股东及出资信息': '股东名称',
        '认缴出资额_万元': '认缴出资额',
        '链接': '股东链接'
    }

    primarykey = 'URL'

    def __init__(self, **kwargs):
        QccRequest.__init__(self)
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
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass
