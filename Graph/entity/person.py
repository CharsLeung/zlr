# encoding: utf-8

"""
project = 'Spider'
file_name = 'person'
author = 'Administrator'
datetime = '2020-03-17 9:46'
IDE = PyCharm
"""
import warnings
from Graph.entity import BaseEntity, NeoNode


class Person(BaseEntity):
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

    def __init__(self, NAME=None, SEX=None, EDUCATION=None, URL=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if NAME is not None:
            self[self.get_englishAttribute_by_chinese('姓名')] = NAME
        if SEX is not None:
            self[self.get_englishAttribute_by_chinese('性别')] = SEX
        if EDUCATION is not None:
            self[self.get_englishAttribute_by_chinese('学历')] = EDUCATION
        if URL is not None:
            self[self.get_englishAttribute_by_chinese('链接')] = URL
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(
                self['URL'])
        pass
