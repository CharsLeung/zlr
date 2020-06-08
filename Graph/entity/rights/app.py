# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = app
author = Administrator
datetime = 2020/4/7 0007 下午 12:07
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class App(BaseEntity):

    """
    app
    """
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['分类', 'TYPE'],
        ['版本', 'VERSION'],
        ['简介', 'ABBREVIATION'],
    ]

    synonyms = {
        '当前版本': '版本'
    }

    primarykey = 'HASH_ID'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of app.')
                    self.BaseAttributes[k] = v
        self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        oas = []

        def f(c):
            # del c['序号']
            # _ = c['证书']
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(app=App(**c))

        if isinstance(content, dict):
            oas.append(f(content))
        elif isinstance(content, list):
            oas += [f(c) for c in content]
        else:
            warnings.warn('invalid type for app content.')
        return oas