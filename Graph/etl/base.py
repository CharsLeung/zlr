# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = base
author = Administrator
datetime = 2020/4/20 0020 下午 17:26
from = office desktop
"""
import re
from typing import Dict, Any

import pandas as pd

from Graph import workspace
# from Graph.data.utils import get_keys, dictMerge
from Graph.exception import SuccessMessage, \
    WarningMessage, ErrorMessage, ExceptionInfo
from Graph.etl.utils import JsonPath, dictMerge, \
    dictTranspose2List


class QccRequest(object):

    ATTRIBUTES = []

    synonyms = {}

    match = {}

    # patterns属性是一个关键的数据，它代表了数据清洗的关键
    # 它应该是一个二维数组，每个元素有三个子元素，分别是：
    # 1.标准的字段域结构；2.针对字段域结构的reg；3.针对取值的reg
    patterns = {}

    def __init__(self, ReturnString=None):
        self.source_dim_2_content = []
        self.format_dim_2_content = []
        self.__load_content__(ReturnString)
        pass

    def __load_content__(self, ReturnString):
        """
        :param ReturnString:
        :return:
        """
        self.source_dim_2_content = []
        self.BaseAttributes = {}
        self.format_dim_2_content = []
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
            self.hash_value = hash(str(self.content))
        pass

    def reload_content(self, ReturnString):
        self.__load_content__(ReturnString)

    @classmethod
    def load_regular_expression(cls, metaModel):
        """
        从excel文档中加载标准化信息
        :return:
        """
        # TODO(leung): 保持标准化模板的及时性
        regs = pd.read_excel(
            workspace + '企查查-属性字段一览表1.1.xlsx',
            sheet_name='{}（标准结构）'.format(metaModel),
            header=[1])
        regs['匹配模式'] = regs['匹配模式'].map(
            lambda x: re.sub('\d+', lambda _: '\d+', x)
        )
        regs['匹配模式-修正'].fillna(regs['匹配模式'], inplace=True)
        regs = regs.loc[:, ['完整目录', '匹配模式-修正', '值匹配模式', '值类型']]
        # regs.sort_values(['完整目录'], ascending=False, inplace=True)
        regs['匹配模式-修正'] = regs['匹配模式-修正'].map(
            lambda x: None if pd.isnull(x) else x
        )
        regs['值匹配模式'] = regs['值匹配模式'].map(
            lambda x: None if pd.isnull(x) else x
        )
        regs['值类型'].fillna('str', inplace=True)
        rs = {}
        for i, r in regs.iterrows():
            rs[r['完整目录']] = [r['匹配模式-修正'], r['值匹配模式'], r['值类型']]
        print(SuccessMessage('success load standardization data doc.'))
        return rs

    def get_keys(self, _, root='', sep='-', return_value=False,
                 filter_key=[], keep_key=[], value_sep='\n'):
        """
        从一个结构层次比较复杂的dict中分析出key的结构层次，
        默认以'-'分割所属关系
        :param value_sep:
        :param keep_key:
        :param filter_key:
        :param return_value:
        :param sep:
        :param _:
        :param root:
        :return:
        """
        # category = list()
        if isinstance(_, list):
            if len(_):
                for sv in _:
                    self.get_keys(sv, root, sep, return_value,
                                  filter_key, keep_key, value_sep)
            else:
                self.source_dim_2_content.append(
                    '{}:{}'.format(root, {}))
                pass
        elif isinstance(_, dict):
            # keep = True if len(keep_key) else False
            for k, v in zip(_.keys(), _.values()):
                if k in filter_key:
                    continue
                # if keep:
                #     for kp in keep_key:
                #         if kp not in '{}{}'.format(root, k):
                #             continue
                # print('{}-{}'.format(root, k))
                if isinstance(v, dict):
                    self.get_keys(v, '{}{}{}'.format(root, sep, k),
                                  sep, return_value, filter_key,
                                  keep_key, value_sep)
                    pass
                elif isinstance(v, list):
                    if len(v):
                        if len(v) == 1:
                            sv = v[0]
                            if '序号' not in sv.keys():
                                sv['序号'] = 1
                            self.get_keys(
                                v[0], '{}{}{}'.format(root, sep, k),
                                sep, return_value, filter_key,
                                keep_key, value_sep)
                        else:
                            xh = 1
                            for sv in v:
                                if '序号' not in sv.keys():
                                    sv['序号'] = xh
                                    xh += 1
                                self.get_keys(
                                    sv, '{}{}{}'.format(root, sep, k),
                                    sep, return_value, filter_key,
                                    keep_key, value_sep)


                            # if return_value:
                            #     data = [[i.split(':')[0], i.split(':')[1]] for i in ks]
                            #     d = pd.DataFrame(data=data,
                            #                      columns=['k', 'v'])
                            #     d = d.groupby(['k'], as_index=False).agg({
                            #         'v': lambda x: '{}'.format(value_sep).join(list(x))
                            #     })
                            #     ks = (d['k'] + ':' + d['v']).tolist()
                            #
                            # else:
                            #     ks = [i.split(':')[0] for i in ks]
                            # self.dim_2_content += ks

                    else:
                        self.source_dim_2_content.append(
                            '{}{}{}:{}'.format(root, sep, k, {}))
                        pass
                else:
                    if return_value:
                        self.source_dim_2_content.append(
                            '{}{}{}:{}'.format(root, sep, k, v))
                        # ks = []
                    else:
                        self.source_dim_2_content.append(
                            '{}{}{}'.format(root, sep, k))
                        # ks = ['{}{}{}'.format(root, sep, k)]
                    pass
                # self.dim_2_content += ks
                # for i in ks:
                #     if 'content-变更记录-变更后-变更后中的链接-链接:' in i:
                #         print(i)
        else:
            self.source_dim_2_content.append('{}:{}'.format(root, _))
        # return category

    def get_source_dim_2_content(self):
        """
        把多层结构的json数据转换成二维平面的数据
        :return:
        """
        # ds = get_keys(self.content, root='content',
        #               sep='-', return_value=True,
        #               value_sep='<tbl>')
        self.get_keys(self.content, root='content',
                      sep='-', return_value=True,
                      value_sep='<tbl>')
        ds = self.source_dim_2_content
        data = [[i.split(':')[0], ':'.join(i.split(':')[1:])] for i in ds]
        # jp = JsonPath(paths=[d[0] for d in data])
        # data2 = []
        # for d in data:
        #     if d[1] == '{}':
        #         sp = jp.son_path(d[0])
        #         sp = [[s, ''] for s in sp]
        #         data2 += sp
        #     else:
        #         data2.append(d)
        # ds = pd.DataFrame(data=data2,
        #                   columns=['k', 'v'])
        # ds = ds.groupby(['k'], as_index=False).agg({
        #     'v': lambda x: list(x)
        # })
        # ds = ds.values.tolist()
        # dim_2_data = {}
        # for d in ds:
        #     _ = d[1] if len(d[1]) > 1 else d[1][0]
        #     dim_2_data[d[0]] = _
        # self.dim_2_content = dim_2_data
        self.source_dim_2_content = data
        # return dim_2_data

    def get_format_dim_2_content(self):
        jp = JsonPath(paths=[d[0] for d in self.format_dim_2_content])
        data = []
        for d in self.format_dim_2_content:
            if d[1] == '{}':
                sp = jp.son_path(d[0])
                sp = [[s, ''] for s in sp]
                data += sp
            else:
                data.append(d)
        ds = pd.DataFrame(data=data,
                          columns=['k', 'v'])
        ds = ds.groupby(['k'], as_index=False).agg({
            'v': lambda x: list(x)
        })
        ds = ds.values.tolist()
        dim_2_data = {}
        for d in ds:
            _ = d[1] if len(d[1]) > 1 else d[1][0]
            dim_2_data[d[0]] = _
        self.format_dim_2_content = dim_2_data

    @classmethod
    def compile_regular_pattern(cls):
        """
        编译所有的匹配模式
        :return:
        """
        ps = []
        for p in cls.patterns:
            _ = [p[0], re.compile(p[1]),
                 p[2] if p[2] is None else re.compile(p[2])]
            ps.append(_)
        cls.patterns = ps
        pass

    # @staticmethod
    # def

    def format_dim_2_content_to_json(self):
        """

        :return:
        """
        content = {}

        def trans(cnt, last_layer_key):
            for layer in last_layer_key:
                p = '["' + '"]["'.join(reversed(layer)) + '"]'
                _ = eval('cnt{}'.format(p))
                # 关键一招
                _ = dictTranspose2List(_)
                try:
                    exec('cnt{}={}'.format(p, _))
                except Exception as e:
                    ExceptionInfo(e)

        list_keys = []
        for k, v in zip(self.format_dim_2_content.keys(),
                        self.format_dim_2_content.values()):
            d = {}
            f = False
            p = []
            for _ in reversed(k.split('-')):
                d = {_: v} if len(d) == 0 else {_: d}
                if f:
                    p.append(_)
                if _ == '序号':
                    f = True
            if len(p):
                list_keys.append(p)
            dictMerge(content, d)
        list_keys.sort(key=lambda x: len(x), reverse=True)
        trans(content, list_keys)
        return content
        pass

    def replace_keys(self, print_process=False):
        """
        对所有key值标准化
        :return:
        """
        # 轮询所有已知的表达式
        if self.source_dim_2_content is None or len(
                self.source_dim_2_content) == 0:
            self.get_source_dim_2_content()
        dim_2_data = []

        def trans_key(key, format_key, pattern):
            if pattern is None:
                f_k = key
            elif pattern[0:5] == 'func:':
                # 说明这是一个函数名，调用即可
                f_k = getattr(self, pattern[1][5:])(key)
            else:  # 当做一个正则表达式
                _ = re.search(pattern, key)
                if _ is not None:
                    f_k = format_key
                    # print(pattern, key)
                else:
                    f_k = None
            return f_k

        match_type = None
        for d in self.source_dim_2_content:
            # fk, fv = None, None
            if d[0] in self.match.keys():
                mk = self.match[d[0]]
                for fk in mk:
                    dim_2_data.append([fk, d[1]])
                match_type = 'cache'
            else:
                ms = []
                for pk, pv in zip(self.patterns.keys(),
                                  self.patterns.values()):
                    fk = trans_key(d[0], pk, pv[0])
                    if fk is not None:
                        dim_2_data.append([fk, d[1]])
                        # self.match[k] = fk
                        ms.append(fk)
                        match_type = 'regular'
                        # break
                self.match[d[0]] = ms
                if len(ms) > 1:
                    print(WarningMessage('multiple replace for {}: {}.'
                                         ''.format(d[0], ms)))
            if d[0] in self.match.keys():
                if print_process:
                    print(SuccessMessage('replace({}): {} => {}'.format(
                        match_type, d[0], self.match[d[0]])))
                pass
            else:
                print(ErrorMessage('mismatch {}:{}'.format(
                    d[0], d[1])))
        self.format_dim_2_content = dim_2_data
        pass

    def replace_values(self, print_process=False):
        """
        对所有值进行标准化
        :return:
        """
        # 轮询所有已知的表达式
        # if self.format_dim_2_content is None or len(
        #         self.format_dim_2_content) == 0:
        self.get_format_dim_2_content()

        dim_2_data = {}

        def trans_v(value, pattern):
            if pattern[1] is None:
                f_v = value
            elif pattern[1][0:5] == 'func:':
                # 说明这是一个函数名，调用即可
                f_v = getattr(self, pattern[1][5:])(value)
            else:  # 当做一个正则表达式
                _ = re.search(pattern[1], value)
                if _ is not None:
                    f_v = _.group(0)
                else:
                    f_v = None

            if f_v is not None:
                if isinstance(f_v, str) and len(f_v) == 0:
                    f_v = None
                else:
                    try:
                        if pattern[2] in ['int', 'float']:
                            f_v = eval('{}("{}")'.format(pattern[2], f_v))
                    except Exception as e:
                        ExceptionInfo(e)
                        f_v = None
                        pass
            return f_v

        def trans_value(value, pattern):

            if isinstance(value, str):
                return trans_v(value, pattern)
            elif isinstance(value, list):
                fvs = []
                for val in value:
                    f_v = trans_v(val, pattern)
                    fvs.append(f_v)
                return fvs
                pass
            else:
                raise TypeError('this type of value must in (str, list).')

        for k, v in zip(self.format_dim_2_content.keys(),
                        self.format_dim_2_content.values()):
            p = self.patterns[k]
            fv = trans_value(v, p)
            dim_2_data[k] = fv
            if print_process and v != fv:
                print('{} replace: {} => {}'.format(k, v, fv))

        self.format_dim_2_content = dim_2_data
        pass
