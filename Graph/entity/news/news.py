# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = news
author = Administrator
datetime = 2020/4/8 0008 下午 15:22
from = office desktop
"""
import warnings

from Graph.entity import QccRequest


class News(QccRequest):
    """
    新闻舆情
    """
    ATTRIBUTES = [
        ['新闻标题', 'TITLE'],
        ['新闻链接', 'URL'],
        ['来源', 'SOURCE'],
        ['发布时间', 'RELEASE_DATE'],
    ]

    synonyms = {
        # '当前版本': '版本'
    }

    primarykey = 'URL'

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
                    warnings.warn('Undefined key for dict of app.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.format_url(
                self.BaseAttributes['URL'])
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
            _ = c.pop('新闻')
            c['新闻标题'] = _['标题']
            c['新闻链接'] = _['链接']
            return c

        if isinstance(content, dict):
            obj.append(News(**f(content)))
        elif isinstance(content, list):
            obj += [News(**f(c)) for c in content]
        else:
            warnings.warn('invalid type for news content.')
        return obj