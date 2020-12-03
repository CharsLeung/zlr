# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = related
author = Administrator
datetime = 2020/5/8 0008 下午 17:02
from = office desktop
"""
import warnings
import pandas as pd

from Graph.entity import BaseEntity


class Related(BaseEntity):

    """
    有关对象，泛指一切有关对象，当出现了不明确的对象实体类型时，模糊的处理成“有关对象”
    """
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL']
    ]

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(self['URL'])
            if self['URL'] is None:
                if self['NAME'] is None or len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = '%s_%s' % (
                        self.label,
                        self.getHashValue(str(self.BaseAttributes))
                    )
        pass

    def to_pandas(self, nodes, **kwargs):
        return BaseEntity.to_pandas(
            self, nodes, drop_suspicious=True, tolerate=3)
        pass