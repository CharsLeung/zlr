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
import numpy as np
import pandas as pd

from Calf.net.prpcrypt import Prpcrypt
from Graph.entity import NeoNode
from Graph.exception import ExceptionInfo


class BaseEntity:
    primarykey = None  # 唯一键

    index = []  # 索引

    ATTRIBUTES = []

    synonyms = {}

    cipher = Prpcrypt('syxsyx')
    unique_code_pattern = re.compile('(?<=/)[a-zA-Z]+_\w{32}(?=\.)')

    def __init__(self, data=None):
        self.__load_content__(data)
        pass

    def __load_content__(self, data):
        self.BaseAttributes = {}
        if data is not None:
            if isinstance(data, dict):
                pass
            else:
                try:
                    data = eval(data)
                except Exception:
                    print(data)
                    raise TypeError('not json object')
            ks = data.keys()
            self.name = data['name'] if 'name' in ks else None
            self.metaModel = data['metaModel'] if 'metaModel' in ks else None
            self.url = data['url'] if 'url' in ks else None
            # self.headers = data['headers'] if 'headers' in ks else None
            # self.get = data['get'] if 'get' in ks else None
            self.update_date = data['date'] if 'date' in ks else None
            # self.id = data['url'] if 'url' in ks else None
            self.content = data['content'] if 'content' in ks else None
        pass

    def reload_content(self, data):
        self.__load_content__(data)
        return self
        pass

    def __getitem__(self, key):
        return self.BaseAttributes[key]

    # def __setitem__(self, key, value):
    #     self.BaseAttributes[key] = value

    def to_dict(self):
        return dict(label=self.label, **self.BaseAttributes)

    def to_pandas(self, nodes):
        nodes = pd.DataFrame(nodes)
        nodes = nodes.dropna(subset=[self.primarykey], inplace=True)
        return nodes
        pass

    def getImportCSV(self, nodes):
        dtypes = dict(nodes.dtypes)
        names = {}
        for k, v in zip(dtypes.keys(), dtypes.values()):
            if k == self.primarykey:
                names[k] = '{}:ID'.format(k)
                continue
            if k == 'label':
                names[k] = ':{}'.format('LABEL')
                continue
            if 'int' in v.name:
                names[k] = '{}:{}'.format(k, 'int')
            elif 'float' in v.name:
                names[k] = '{}:{}'.format(k, 'float')
            else:
                pass
        nodes = nodes.rename(columns=names)
        return nodes
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

    @classmethod
    def parser_url(cls, url):
        """
        只针对公司、个人主页的url
        :param url:
        :return:
        """
        try:
            return cls.getUniqueCode(url) if url is not None else url
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

    def get_create_node_cypher(self):
        """

        :return:
        """
        attr = []
        for k, v in zip(self.BaseAttributes.keys(),
                        self.BaseAttributes.values()):
            # attr.append('{}: {}'.format())
            pass
        cp = 'CREATE (:%s {%s})' % (self.label, '')

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
    def getEntityUniqueCodeSYX(data, flag):
        return '{}_{}'.format(flag, BaseEntity.cipher.encrypt(data))

    @staticmethod
    def getHashValue(data):
        return hashlib.md5(data.encode("utf8")).hexdigest()

    @staticmethod
    def getEntityUniqueCodeQCC(data, flag):
        return '{}_{}'.format(flag, BaseEntity.cipher.decrypt(data))

    @staticmethod
    def getUniqueCode(url):
        if url is not None and isinstance(url, str):
            _ = re.search(BaseEntity.unique_code_pattern, url)
            if _ is not None:
                return _.group(0)
            else:
                return None
        else:
            return url

    @staticmethod
    def getTypeForEtpOrPsr(uniqueCode):
        """
        根据传入的这个标签，判断这是一个企业还是一个人
        :param uniqueCode: qcc的KeyNo或者其连接
        :return:无法判断 0；企业 1；  人 2；
        """
        # tp = BaseEntity.getUniqueCode(label)
        if uniqueCode is not None:
            if uniqueCode[0] == 'p':
                return 2
            else:
                return 1
        else:
            return 0

    def isPerson(self, url=None):
        if url is not None:
            uc = url
        elif 'URL' in self.BaseAttributes.keys():
            uc = self.BaseAttributes['URL']
        else:
            return False
            # uc = self.getUniqueCode(url)
        if uc is not None:
            if self.getTypeForEtpOrPsr(uc.split('_')[1]) == 2:
                return True
        return False

    def isEnterprise(self, url=None):
        if url is not None:
            uc = url
        elif 'URL' in self.BaseAttributes.keys():
            uc = self.BaseAttributes['URL']
        else:
            return False
        # uc = self.getUniqueCode(uc)
        if uc is not None:
            if self.getTypeForEtpOrPsr(uc.split('_')[1]) == 1:
                return True
        return False
