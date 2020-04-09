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
        """
        只针对公司、个人主页的url
        :param url:
        :return:
        """
        try:
            url = QccRequest.format_url(url)
            _ = re.search('/[a-zA-Z_]+_\w{32}', url)
            if _ is not None:
                # print('"{}",'.format(_.group(0)))
                _ = 'https://www.qcc.com' + _.group(0) + '.html'
            else:
                _ = url
            return _
        except Exception as e:
            print(e)
            return url

    @staticmethod
    def format_url(url):
        """
        针对所有url
        :param url:
        :return:
        """
        if isinstance(url, str):
            fu = []
            url = url.split('/')[1:]
            for _ in url:
                if len(_):
                    fu.append(_)
            return 'https://' + '/'.join(fu)
        else:
            return url

    def get_create_index_cypher(self, attribute):
        """
        生成创建索引的代码
        :return:
        """
        return 'CREATE INDEX ON:{}({})'.format(self.label, attribute)

    def get_create_constraint_cypher(self, attribute=None):
        """
        生成创建唯一键的代码
        :param attribute:
        :return:
        """
        return 'CREATE CONSTRAINT ON (n:{}) ASSERT n.{} IS UNIQUE'.format(
            self.label, attribute if attribute is not None else self.primarykey
        )


