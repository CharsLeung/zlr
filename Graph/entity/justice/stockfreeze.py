# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = stockfreeze
author = Administrator
datetime = 2020/5/14 0014 下午 15:58
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class StockFreeze(BaseEntity):

    """
    股权冻结
    """

    ATTRIBUTES = [
        ['冻结数额', 'AMOUNT'],
        ['金额单位', 'UNIT'],
        ['执行文号', 'SYMBOL'],
        ['执行法院', 'COURT'],
        ['类型', 'TYPE'],
        ['状态', 'STATE'],
        # ['履行情况', 'EXECUTED_SUBJECT'],
    ]

    synonyms = {
        '执行通知书文号': '执行文号',
        # '链接': '标的链接'
    }

    primarykey = 'HASH_ID'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self[] = hash(str(self.BaseAttributes))
        self['HASH_ID'] = '%s_%s' % (
            self.label,
            self.getHashValue(str(self.BaseAttributes))
        )
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.parser_url(
        #         self['URL'])
        pass