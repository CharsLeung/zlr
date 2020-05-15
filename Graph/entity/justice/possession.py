# encoding: utf-8

"""
project = zlr
file_name = possession
author = Administrator
datetime = 2020/4/1 0001 下午 15:42
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Possession(QccRequest):

    """
    标的物，一般情况下出质的标的物都是企业
    所有, 所有权, 属地, 领地, 领土, 货
    """

    ATTRIBUTES = [
        ['标的名称', 'NAME'],
        ['标的链接', 'URL'],
        # ['出质股权数额', 'AMOUNT'],
        # ['登记日期', 'REGISTRATION_DATE'],
        # ['登记编号', 'REGISTRATION_NUM'],
        # ['状态', 'STATUS']
    ]

    synonyms = {
        '企业': '标的名称',
        '链接': '标的链接',
        '名称': '标的名称'
    }

    primarykey = 'URL'

    index = [('NAME',)]

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
                    warnings.warn('Undefined key for dict of possession subject.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass