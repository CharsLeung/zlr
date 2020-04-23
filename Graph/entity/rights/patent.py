# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = patent
author = Administrator
datetime = 2020/4/7 0007 下午 14:21
from = office desktop
"""
import warnings

from Graph.entity import QccRequest


class Patent(QccRequest):
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
        QccRequest.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of patent.')
                    self.BaseAttributes[k] = v
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            del c['序号']
            _ = c.pop('专利')
            c['专利名称'] = _['名称']
            c['专利链接'] = _['链接']
            return c

        if isinstance(content, dict):
            obj.append(Patent(**f(content)))
        elif isinstance(content, list):
            obj += [Patent(**f(c)) for c in content]
        else:
            warnings.warn('invalid type for patent content.')
        return obj
