# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = debt
author = Administrator
datetime = 2020/5/13 0013 上午 10:48
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Debt(QccRequest):

    """
    债务
    """

    ATTRIBUTES = [
        ['债务(金额)', 'AMOUNT'],
        ['债务(单位)', 'UNIT'],
        ['履行期限', 'DEADLINE'],
        # ['结果', 'RESULT'],
    ]

    synonyms = {
        # '检查实施机关': '实施机关',
        # '链接': '标的链接'
    }

    primarykey = 'HASH_ID'

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
        self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        # if 'URL' in self.BaseAttributes.keys():
        #     self.BaseAttributes['URL'] = self.parser_url(
        #         self.BaseAttributes['URL'])
        pass