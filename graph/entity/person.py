# encoding: utf-8

"""
project = 'Spider'
file_name = 'person'
author = 'Administrator'
datetime = '2020-03-17 9:46'
IDE = PyCharm
"""
import warnings
from entity import QccRequest, NeoNode


class Person(QccRequest):

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

    def __init__(self,  name=None, sex=None, education=None, url=None, **kwargs):
        QccRequest.__init__(self)

        self.BaseAttributes[self.get_englishAttribute_by_chinese('姓名')] = name if name is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('性别')] = sex if sex is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('学历')] = education if education is not None else None
        self.BaseAttributes[self.get_englishAttribute_by_chinese('链接')] = url if url is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[self.synonyms[k]] = v
                else:
                    warnings.warn('Undefined key for dict of person.')
        pass

    def get_neo_node(self):
        return NeoNode(
            'person',
            **self.BaseAttributes
        )

# Person()