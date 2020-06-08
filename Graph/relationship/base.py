# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = base
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/2 0002 下午 16:20
@from = office desktop
"""
import re

from py2neo import Relationship


class Base:
    """
    所有关系类的基类
    """
    ATTRIBUTES = []

    name_pattern = re.compile('[A-Z]+[a-z]+')

    def __init__(self, start=None, end=None, **kwargs):
        self.start = start
        self.end = end
        self.properties = kwargs
        pass

    @property
    def label(self):
        lb = str(self.__class__.__name__)
        lb = list(re.findall(self.name_pattern, lb))
        lb = '_'.join([l.upper() for l in lb])
        return lb

    def get_relationship(self):
        return Relationship(
            self.start,
            self.label,
            self.end,
            **self.properties
        )
        pass

    def to_dict(self):
        return dict({
            'label': self.label,
            'from': self.start[self.start.__primarykey__],
            'to': self.end[self.end.__primarykey__],
        }, **self.properties)

    def getImportCSV(self, rps):
        dtypes = dict(rps.dtypes)
        names = {'from': ':START_ID', 'to': ':END_ID', 'label': ':TYPE'}
        for k, v in zip(dtypes.keys(), dtypes.values()):
            if k in names.keys():
                continue
            if 'int' in v.name:
                names[k] = '{}:{}'.format(k, 'int')
            elif 'float' in v.name:
                names[k] = '{}:{}'.format(k, 'float')
            else:
                pass
        rps = rps.rename(columns=names)
        return rps
        pass