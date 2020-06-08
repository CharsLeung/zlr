# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = news
author = Administrator
datetime = 2020/4/8 0008 下午 15:22
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class News(BaseEntity):
    """
    新闻舆情
    """
    ATTRIBUTES = [
        ['新闻标题', 'TITLE'],
        ['新闻链接', 'URL'],
        ['来源', 'SOURCE'],
        ['简介', 'INTRODUCTION'],
        ['情感', 'EMOTION'],
        ['标签', 'LABEL'],
        ['发布时间', 'RELEASE_DATE'],
    ]

    synonyms = {
        # '当前版本': '版本'
    }

    primarykey = 'URL'

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
            # _ = c.pop('新闻')
            if '关联对象' in c.keys():
                c['关联对象'] = [_.strip() for _ in c.pop('关联对象').split('\n')]
            if '标签' in c.keys():
                c['标签'] = c['标签'] if len(c['标签']) else []
            # c['新闻标题'] = _['标题']
            # c['新闻链接'] = _['链接']
            return dict(news=News(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for news content.')
        return obj
