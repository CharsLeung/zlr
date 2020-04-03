# encoding: utf-8

"""
project = zlr
file_name = involveder
author = Administrator
datetime = 2020/3/30 0030 下午 14:21
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Involveder(QccRequest):

    """
    案件参与者
    """
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL']
    ]

    # 案件参与者不见得有链接，但一定会有一个名称
    # 但有一个问题，名称很有可能存在重复的，类似
    # 有很多同名的人,所以，根据基础属性算一个哈希
    # ID
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
                    warnings.warn('Undefined key for dict of case involveder.')
        self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass