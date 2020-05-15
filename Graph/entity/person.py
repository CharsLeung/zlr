# encoding: utf-8

"""
project = 'Spider'
file_name = 'person'
author = 'Administrator'
datetime = '2020-03-17 9:46'
IDE = PyCharm
"""
import warnings
from Graph.entity import QccRequest, NeoNode


class Person(QccRequest):
    """
    自然人
    """

    # label = Person.__class__._

    ATTRIBUTES = [
        ['姓名', 'NAME'],
        ['性别', 'SEX'],
        ['学历', 'EDUCATION'],
        ['链接', 'URL']
    ]

    synonyms = {
        '名称': '姓名',
        '姓名': '姓名',
        # ''
    }

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self,  NAME=None, SEX=None, EDUCATION=None, URL=None, **kwargs):
        QccRequest.__init__(self)

        self.BaseAttributes[self.get_englishAttribute_by_chinese('姓名')] = NAME if NAME is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('性别')] = SEX if SEX is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('学历')] = EDUCATION if EDUCATION is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('链接')] = URL if URL is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of person.')
                    self.BaseAttributes[k] = v
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass