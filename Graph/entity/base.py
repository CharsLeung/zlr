# encoding: utf-8

"""
project = 'Spider'
file_name = 'base'
author = 'Administrator'
datetime = '2020-03-16 18:46'
IDE = PyCharm
"""
import re
import os
import copy
import hashlib
import warnings
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
    unique_code_pattern = re.compile('[a-zA-Z]+_\w{32}')  # (?<=/)(?=\.)

    def __init__(self, data=None, **kwargs):
        # self.BaseAttributes = {}
        self.__load_content__(data)
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self[cad[k]] = v
                elif k in sks:
                    self[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict {}.'.format(self.label))
                    self[k] = v
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

    def __getitem__(self, *key):
        # use like base['URL'] or base['NAME', 'URL']
        if len(key) > 1:
            _ = {}
            for k in key:
                _[k] = self.BaseAttributes.get(k)
        else:
            _ = self.BaseAttributes.get(key[0])
        return _

    def __setitem__(self, key, value):
        # use like base['URL'] = 'abc'
        self.BaseAttributes[key] = value

    def __str__(self):
        _ = ['LABEL:%s' % self.label]
        for k, v in zip(self.BaseAttributes.keys(),
                        self.BaseAttributes.values()):
            _.append('%s:%s' % (k, v))
        return ' '.join(_)

    def __getattr__(self, item):
        return self[item]

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self[self.primarykey] == other[other.primarykey]
        else:
            return False

    def to_dict(self, with_label=True):
        if with_label:
            _ = dict(label=self.label,
                     **self.BaseAttributes)
        else:
            _ = self.BaseAttributes
        return _

    def to_pandas(self, nodes, drop_suspicious=False,
                  tolerate=5, **kwargs):
        """

        :param nodes: list-like
        :param drop_suspicious: primarykey重复一般情况下是正常的
        但是在有些实体当中存在重复的是不正常的，可能是因为重名但
        primarykey又为空，有些实体则会根据name生成一个primarykey，
        这种情况极易导致异常，
        :param tolerate: 重复数据达到一定数量则认为是异常的，
        当drop_suspicious=True时起作用
        :return:
        """
        nodes = pd.DataFrame(nodes)
        if drop_suspicious:
            use_col = [self.primarykey]
            agg_col = {'count': 'count'}
            # TODO(lj):可能需要把根据名称长短来忽略部分去重规则移到子类中
            if 'NAME' in list(nodes.columns):
                use_col.append('NAME')
                agg_col['NAME'] = 'first'
                pass
            drop = nodes.loc[:, use_col]
            drop['count'] = 1
            drop = drop.groupby([self.primarykey], as_index=False
                                ).agg(agg_col)
            if 'NAME' in list(nodes.columns):
                # 名称长度短于4的认为是人名，很多没有url
                # 的而且重复的人名无法确定唯一性
                drop = drop[drop['NAME'].str.len() < 4]
            drop = drop[drop['count'] > tolerate]
            # drop = drop.tolist()
            if len(drop):
                drop = drop[self.primarykey]
                nodes = nodes[~nodes[self.primarykey].isin(drop)]
        nodes.dropna(subset=[self.primarykey], inplace=True)
        nodes.drop_duplicates(subset=[self.primarykey], inplace=True)
        nodes.dropna(axis=1, how='all', inplace=True)
        return nodes
        pass

    @staticmethod
    def append(data, header_path, data_path):
        # 只适用于头文件分离模式
        if os.path.exists(header_path):
            # 头文件存在，需要根据头文件的列名顺序追加数据
            with open(header_path, 'r+', encoding='utf-8') as f:
                exist_header = f.readline()
                exist_header = exist_header.split(',')
                new_header = list(data.columns)
                update = False
                for h in new_header:
                    if h not in exist_header:
                        exist_header.append(h)
                        update = True
                if update:
                    f.write(','.join(exist_header))
                    print('update header file:{}'.format(header_path))
                data = data.loc[:, exist_header]
                data.to_csv(data_path, index=False,
                            header=False, mode='a')
                pass
        else:
            data.to_csv(data_path, index=False,
                        header=False, mode='a')
            with open(header_path, 'w+', encoding='utf-8') as f:
                header = ','.join(list(data.columns))
                f.write(header)
                pass

    def to_csv(self, nodes, folder, split_header=False, mode='replace'):
        data_path = folder + '\{}.csv'.format(self.label)
        if split_header:
            header_path = folder + '\{}_Header.csv'.format(self.label)
            if mode[0] == 'a':
                self.append(nodes, header_path, data_path)
            else:
                nodes.to_csv(data_path, index=False, header=False)
                with open(header_path, 'w+', encoding='utf-8') as f:
                    header = ','.join(list(nodes.columns))
                    f.write(header)
        else:
            nodes.to_csv(data_path, index=False)
            pass
        return len(nodes)

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

    def read_csv(self, data_path, header_path=None):
        if not os.path.isfile(data_path):
            data_path = os.path.join(data_path, '%s.csv' % self.label)
            if not os.path.isfile(data_path):
                raise FileNotFoundError('not found related data file.')

        if header_path is not None:
            data = pd.read_csv(data_path, header=None,
                               engine='python', encoding='utf-8')
            if not os.path.isfile(header_path):
                header_path = os.path.join(header_path, '%s_Header.csv' % self.label)
                if not os.path.isfile(header_path):
                    raise FileNotFoundError('not found related header file.')
            with open(header_path, 'r+', encoding='utf-8') as f:
                header = f.readline()
                header = header.split(',')
                data = data.rename(columns=dict(zip(list(data.columns), header)))
        else:
            data = pd.read_csv(data_path)
        return data

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
    def textPhrase(text):
        """
        对一个文本短语进行清洗
        所谓文本短语，就是区别与句子和段落的短小词语
        所以不应该出现空格、\n \t等等
        :param text:
        :return:
        """
        if isinstance(text, str):
            return text.replace(' ', '') \
                .replace('\n', '') \
                .replace('\t', '')
            pass
        else:
            return str(text)

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
            uc = self['URL']
        else:
            return False
        uc = self.getUniqueCode(uc)
        if uc is not None:
            _uc_ = uc.split('_')
            if self.getTypeForEtpOrPsr(_uc_[1]) == 2:
                return True
        return False

    def isEnterprise(self, url=None):
        if url is not None:
            uc = url
        elif 'URL' in self.BaseAttributes.keys():
            uc = self['URL']
        else:
            return False
        uc = self.getUniqueCode(uc)
        if uc is not None:
            _uc_ = uc.split('_')
            if self.getTypeForEtpOrPsr(_uc_[1]) == 1:
                return True
        return False
