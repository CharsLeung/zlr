# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = patent
author = Administrator
datetime = 2020/4/7 0007 下午 14:21
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class Patent(BaseEntity):
    """
    专利
    """

    ATTRIBUTES = [
        ['专利名称', 'NAME'],
        ['专利链接', 'URL'],
        ['专利类型', 'TYPE'],
        ['公开号', 'LICENSE'],
        ['公开日期', 'RELEASE_DATE']
    ]

    synonyms = {
        # '网站名称': '名称',
        # '网站备案_许可证号': '备案许可证号',
    }

    primarykey = 'LICENSE'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
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
            _ = c.pop('专利')
            c['专利名称'] = _['名称']
            c['专利链接'] = _['链接']
            return dict(patent=Patent(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for patent content.')
        return obj
