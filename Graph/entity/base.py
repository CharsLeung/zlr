# encoding: utf-8

"""
project = 'Spider'
file_name = 'base'
author = 'Administrator'
datetime = '2020-03-16 18:46'
IDE = PyCharm
"""
import re
import copy
import hashlib

from Graph.entity import NeoNode
from Graph.exception import ExceptionInfo


class QccRequest:

    primarykey = None   # 唯一键

    index = []  # 索引

    ATTRIBUTES = []

    synonyms = {}

    unique_code_pattern = re.compile('/[a-zA-Z_]+_\w{32}.html')

    def __init__(self, ReturnString=None):
        self.__load_content__(ReturnString)
        pass

    def __load_content__(self, ReturnString):
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

    def reload_content(self, ReturnString):
        self.__load_content__(ReturnString)
        return self
        pass

    def __getitem__(self, key):
        return self.BaseAttributes[key]

    def __setitem__(self, key, value):
        self.BaseAttributes[key] = value

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
        if sum([1 if v is not None else 0 for v in
                self.BaseAttributes.values()]):
            n = NeoNode(self.label, **self.BaseAttributes)
            if primarylabel is not None:
                n.__primarylabel__ = primarylabel
            else:
                n.__primarylabel__ = self.label
            if primarykey is not None:
                n.__primarykey__ = primarykey
                if n[primarykey] is None:
                    return None
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
            # url = QccRequest.format_url(url)
            _ = re.search(QccRequest.unique_code_pattern, url)
            if _ is not None:
                # print('"{}",'.format(_.group(0)))'https://www.qcc.com' +
                _ = _.group(0)
            else:
                _ = url
            return _
        except Exception as e:
            # ExceptionInfo(e)
            # print('invalid url({}) for person or enterprise.'.format(url))
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
            url = url.split(' ')[0]
            url = url.split('/')[1:]
            for _ in url:
                if len(_):
                    fu.append(_)
            return '/' + '/'.join(fu)
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

    @staticmethod
    def get_format_amount(k, v):
        """
        把类似：'注册资本':{'金额': 123, '单位': '万元人民币'}
        转换成{'注册资本(金额)':123, '注册资本(单位)':'万元人民币'}
        :param v:
        :param k:
        :return:
        """
        _ = {}
        for a, b in zip(v.keys(), v.values()):
            _['{}({})'.format(k, a)] = b
        return _

    @staticmethod
    def get_format_dict(data):
        """
        把原始数据中以“#”加一个数字作为key，这种其实
        是一个数组，把这种还原成数组
        :param data:
        :return:
        """
        if len(data):
            data = copy.deepcopy(data)
            ks = data.keys()
            if sum(['#' in k for k in ks]) == len(ks):
                ds = list(data.values())
                return ds if len(ds) > 1 else ds[0]
            else:
                return data
        else:
            return []

    @staticmethod
    def get_entity_unique_code(data):
        return '/syx_{}'.format(hashlib.md5(
            data.encode("utf8")).hexdigest())

