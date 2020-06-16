# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = recruitment
author = Administrator
datetime = 2020/4/7 0007 下午 17:05
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Position(BaseEntity):

    """
    职位
    """

    ATTRIBUTES = [
        ['职位', 'POSITION'],
        ['链接', 'URL'],
    ]

    synonyms = {
        '招聘职位': '职位',
        '招聘链接': '职位'
    }

    primarykey = 'URL'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(self['URL'])
            if self['URL'] is None:
                if self['NAME'] is None or len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = 'Position_%s' % self.getHashValue(
                        self['NAME'])
        pass

    def to_pandas(self, nodes, **kwargs):
        return BaseEntity.to_pandas(
            self, nodes, drop_suspicious=True, tolerate=3)
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            # del c['序号']
            _ = c.pop('职位')
            return dict(position=Position(**_), **c)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for recruitment content.')
        return obj