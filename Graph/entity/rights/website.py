# encoding: utf-8

"""
project = 'zlr'
file_name = 'website'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 10:52'
from = 'office desktop' 
"""
import warnings

from Graph.entity import QccRequest


class Website(QccRequest):
    """
    网站
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['网址', 'URL'],
        ['域名', 'DOMAIN'],
        ['备案许可证号', 'LICENSE'],
        ['审核日期', 'REVIEW_DATE']
    ]

    synonyms = {
        '网站名称': '名称',
        '网站备案_许可证号': '备案许可证号',
        '网站备案许可证号': '备案许可证号',
    }

    primarykey = 'LICENSE'

    def __init__(self, URL=None, **kwargs):
        QccRequest.__init__(self)
        self.BaseAttributes['URL'] = URL if URL is not None else None
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of website.')
                    self.BaseAttributes[k] = v
        pass

    def __split_levels__(self):
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        wbs = []

        def f(c):
            # del c['序号']
            # _ = c.pop('证书')
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(website=Website(**c))

        if isinstance(content, dict):
            wbs.append(f(content))
        elif isinstance(content, list):
            wbs += [f(c) for c in content]
        else:
            warnings.warn('invalid type for Website content.')
        return wbs