# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = plot
author = Administrator
datetime = 2020/5/11 0011 上午 11:22
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Plot(BaseEntity):

    """
    地块
    """
    ATTRIBUTES = [
        ['位置', 'NAME'],
        ['链接', 'URL'],
        ['面积(数量)', 'AMOUNT'],
        ['面积(单位)', 'UNIT'],
        ['供地方式', 'SUPPLY_TYPE'],
        ['土地用途', 'USE'],
        ['行政区', 'CITY'],
    ]

    synonyms = {
        '面积': '面积(数量)',
        '所属地区': '行政区'
    }

    primarykey = 'HASH_ID'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        self['HASH_ID'] = '%s_%s' % (
            self.label,
            self.getHashValue(str(self.BaseAttributes))
        )
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.parser_url(
        #         self['URL'])
        pass