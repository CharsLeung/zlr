# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = product
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/10 0010 上午 11:04
@from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class Product(BaseEntity):
    """
    产品
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['介绍', 'INTRODUCTION'],
        ['图片', 'IMAGE'],
    ]

    synonyms = {
        '产品介绍': '介绍',
        '产品图片': '图片',
    }

    primarykey = 'URL'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if self[self.primarykey] is None:
            if self['NAME'] is not None and \
                    len(str(self['NAME'])) > 1:
                self[self.primarykey] = '%s_%s' % (
                    self.label,
                    self.getHashValue(self['NAME'])
                )
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
            _ = c.pop('产品名').split('|')
            p = {'名称': _[0]}
            if len(_) > 1:
                p['链接'] = _[1]
            p = Product(**dict(产品图片=c['产品图片'], 产品介绍=c['产品介绍'], **p))
            return dict(product=p, **c)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for product content.')
        return obj
