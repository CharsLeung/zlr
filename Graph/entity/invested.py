# encoding: utf-8

"""
project = 'zlr'
file_name = 'invested'
author = 'Administrator'
datetime = '2020/3/26 0026 下午 18:05'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class Invested(QccRequest):

    """
    对外投资对象不是某个以存在的企业时，新建一个被投资实体
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['注册资本', 'REGISTERED_CAPITAL'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['经营状态', 'OPERATING_STATUS']
    ]

    synonyms = {
        '状态': '经营状态',
        # '认缴出资额_万元': '认缴出资额',
        # '链接': '股东链接'
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
                    warnings.warn('Undefined key for dict of invested.')
                    self.BaseAttributes[k] = v
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass