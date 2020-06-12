# encoding: utf-8

"""
project = zlr
file_name = possession
author = Administrator
datetime = 2020/4/1 0001 下午 15:42
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Possession(BaseEntity):

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
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(
                self['URL'])
            if self['URL'] is None:
                if len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = 'Possession_%s' % self.getHashValue(
                        self['NAME'])
        pass