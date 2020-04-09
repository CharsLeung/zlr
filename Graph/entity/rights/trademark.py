# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = trademark
author = Administrator
datetime = 2020/4/7 0007 下午 14:33
from = office desktop
"""
import warnings

from Graph.entity import QccRequest


class Trademark(QccRequest):

    ATTRIBUTES = [
        ['商标名称', 'NAME'],
        ['商标链接', 'URL'],
        ['国际分类', 'TYPE'],
        ['注册号', 'LICENSE'],
        ['申请日期', 'RELEASE_DATE'],
        ['流程状态', 'STATUE']
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
                    warnings.warn('Undefined key for dict of trademark.')
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
            _ = c.pop('商标')
            c['商标名称'] = _['名称']
            c['商标链接'] = _['商标']
            _ = c.pop('内容')
            c['内容详情'] = _['链接']
            return c

        if isinstance(content, dict):
            obj.append(Trademark(**f(content)))
        elif isinstance(content, list):
            obj += [Trademark(**f(c)) for c in content]
        else:
            warnings.warn('invalid type for trademark content.')
        return obj