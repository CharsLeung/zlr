# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = banknote
author = Administrator
datetime = 2020/5/13 0013 上午 11:23
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Banknote(BaseEntity):
    """
    票据
    """

    ATTRIBUTES = [
        ['票面金额(金额)', 'AMOUNT'],
        ['票面金额(单位)', 'UNIT'],
        ['票据类型', 'TYPE'],
        ['票据号', 'NUM'],
    ]

    synonyms = {
        # '检查实施机关': '实施机关',
        # '链接': '标的链接'
    }

    primarykey = 'HASH_ID'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        self[self.primarykey] = '%s_%s' % (
            self.label,
            self.getHashValue(str(self.BaseAttributes))
        )
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.parser_url(
        #         self['URL'])
        pass
