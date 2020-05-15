# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = lhcc
author = Administrator
datetime = 2020/5/14 0014 下午 15:26
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class LimitOrder(QccRequest):

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
                    warnings.warn('Undefined key for dict of check.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        # if 'URL' in self.BaseAttributes.keys():
        #     self.BaseAttributes['URL'] = self.parser_url(
        #         self.BaseAttributes['URL'])
        pass