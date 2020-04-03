# encoding: utf-8

"""
project = 'Spider'
file_name = 'base'
author = 'Administrator'
datetime = '2020-03-16 18:46'
IDE = PyCharm
"""
import re

from Graph.entity import NeoNode


class QccRequest(object):

    primarykey = None

    ATTRIBUTES = []

    synonyms = {}

    def __init__(self, ReturnString=None):
        self.BaseAttributes = {}
        if ReturnString is not None:
            if isinstance(ReturnString, dict):
                pass
            else:
                try:
                    ReturnString = eval(ReturnString)
                except Exception:
                    print(ReturnString)
                    raise TypeError('not json object')
            ks = ReturnString.keys()
            self.name = ReturnString['name'] if 'name' in ks else None
            self.metaModel = ReturnString['metaModel'] if 'metaModel' in ks else None
            self.url = ReturnString['url'] if 'url' in ks else None
            self.headers = ReturnString['headers'] if 'headers' in ks else None
            self.get = ReturnString['get'] if 'get' in ks else None
            self.update_date = ReturnString['date'] if 'date' in ks else None
            # self.id = ReturnString['url'] if 'url' in ks else None
            self.content = ReturnString['content'] if 'content' in ks else None
        pass

    def content_keys(self):
        pass

    def get_englishAttribute_by_chinese(self, name):
        for _ in self.ATTRIBUTES:
            if _[0] == name:
                return _[1]
        return None

    def get_chineseAttribute_by_english(self, name):
        for _ in self.ATTRIBUTES:
            if _[1] == name:
                return _[0]
        return None

    def chineseAttributeDict(self):
        return dict((a[0], a[1]) for a in self.ATTRIBUTES)

    def englishAttributeDict(self):
        return dict((a[1], a[0]) for a in self.ATTRIBUTES)

    @property
    def label(self):
        return str(self.__class__.__name__)

    def get_neo_node(self, primarylabel=None, primarykey=None):
        if sum([1 if v is not None else 0 for v in self.BaseAttributes.values()]):
            n = NeoNode(self.label, **self.BaseAttributes)
            if primarylabel is not None:
                n.__primarylabel__ = primarylabel
            else:
                n.__primarylabel__ = self.label
            if primarykey is not None:
                n.__primarykey__ = primarykey
            return n
        else:
            return None

    @staticmethod
    def parser_url(url):
        _ = re.search('/[a-zA-Z_]+_\w{32}', url).group(0)
        return _[1:]


