# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = related
author = Administrator
datetime = 2020/5/8 0008 下午 17:02
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Related(QccRequest):

    """
    有关对象，泛指一切有关对象
    """
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL']
    ]

    primarykey = 'HASH_ID'

    index = [('NAME',), ('URL',)]

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
            if self.BaseAttributes['URL'] is None:
                if len(self.BaseAttributes['NAME']) < 2:
                    self.BaseAttributes['NAME'] = None
        pass