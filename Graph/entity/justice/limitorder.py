# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = lhcc
author = Administrator
datetime = 2020/5/14 0014 下午 15:26
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class LimitOrder(BaseEntity):

    """
    限消令
    """

    ATTRIBUTES = [
        ['案号', 'CASE_NUM'],
        ['案号链接', 'URL'],
        # ['执行文号', 'SYMBOL'],
        ['立案日期', 'REGISTER_DATE'],
        ['发布日期', 'RELEASE_DATE'],
        # ['履行情况', 'EXECUTED_SUBJECT'],
        # ['执行法院', 'COURT'],
    ]

    synonyms = {
        # '检查实施机关': '实施机关',
        # '链接': '标的链接'
    }

    primarykey = 'CASE_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.parser_url(
        #         self['URL'])
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
        pass