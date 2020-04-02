# encoding: utf-8

"""
project = zlr
file_name = ruling
author = Administrator
datetime = 2020/3/27 0027 下午 15:34
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Ruling(QccRequest):
    """
    裁决文书，案号作为id
    """

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件链接', 'CASE_URL'],
        ['案件身份', 'CASE_IDENTITY'],  # 这一属性应体现到关系属性当中去
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['执行法院', 'COURT'],
        ['案件金额', 'CASE_AMOUNT'],
        ['发布日期', 'RELEASE_DATE']
    ]

    primarykey = 'CASE_NUM'

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
                    warnings.warn('Undefined key for dict of justice case.')
        if 'CASE_IDENTITY' in self.BaseAttributes.keys():
            self.CASE_IDENTITY = self.BaseAttributes.pop('CASE_IDENTITY')
        else:
            self.CASE_IDENTITY = None
        pass

    @classmethod
    def create_from_dict(cls, content):
        """
        从一个dict或者是dict的list中创建Ruling对象
        :param content:
        :return: list
        """
        rls = []
        if isinstance(content, dict):
            _ = cls.split_case_identity(content)
            ivs = _.pop('涉案对象')
            rls.append([Ruling(**_), ivs])
        elif isinstance(content, list):
            for c in content:
                _ = cls.split_case_identity(c)
                ivs = _.pop('涉案对象')
                rls.append([Ruling(**_), ivs])
        else:
            warnings.warn('invalid type for Ruling content.')

        return rls

    @classmethod
    def split_case_identity(cls, case_identity):
        """
        案件身份是一个类似：{'案件身份': {'内容': '...',
        '链接': [{'链接文字':'...', '链接':'...'},]}}
        :param case_identity:
        :return:
        """
        # _ = {}
        c1 = case_identity.pop('案件')
        case_identity['案件名称'] = c1['名称']
        case_identity['案件链接'] = c1['链接']
        c2 = case_identity.pop('案件身份')
        cnt = c2['内容'].replace('-\n', '-').split('\n')
        cnt = [c.split('-') for c in cnt]
        inv = []
        for i in range(len(c2['链接'])):
            c = cnt[i]
            c.append(c2['链接'][i]['链接'])
            if len(c) == 3:
                inv.append(c)
            else:
                warnings.warn('裁决文书：异常的案件身份({})'.format('-'.join(c)))
        case_identity['涉案对象'] = inv
        return case_identity


