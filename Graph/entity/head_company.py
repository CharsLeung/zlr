# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = head_company
author = Administrator
datetime = 2020/5/8 0008 下午 16:32
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class HeadCompany(BaseEntity):

    """
    总公司，总公司对象不是某个已存在的企业时，新建一个总公司实体
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['注册资本(金额)', 'REGISTERED_CAPITAL_AMOUNT'],
        ['注册资本(单位)', 'REGISTERED_CAPITAL_UNIT'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['经营状态', 'OPERATING_STATUS']
    ]

    synonyms = {
        '状态': '经营状态',
        # '认缴出资额_万元': '认缴出资额',
        # '链接': '股东链接'
    }

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
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