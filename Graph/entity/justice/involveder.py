# encoding: utf-8

"""
project = zlr
file_name = involveder
author = Administrator
datetime = 2020/3/30 0030 下午 14:21
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Involveder(BaseEntity):

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
    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(
                self['URL'])
            if self['URL'] is None:
                if len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = '%s_%s' % (
                        self.label,
                        self.getHashValue(self['NAME'])
                    )
        pass

    def to_pandas(self, nodes, **kwargs):
        return BaseEntity.to_pandas(
            self, nodes, drop_suspicious=True, tolerate=3)
        pass