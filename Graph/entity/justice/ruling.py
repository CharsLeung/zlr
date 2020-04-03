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
from Graph.data.utils import get_keys


class Ruling(QccRequest):
    """
    裁决文书，案号作为id
    """

    ATTRIBUTES = [
        ['案件名称', 'CASE_NAME'],
        ['案件链接', 'URL'],
        ['案件身份', 'CASE_IDENTITY'],  # 这一属性应体现到关系属性当中去
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['执行法院', 'COURT'],
        ['案件金额', 'CASE_AMOUNT'],
        ['发布日期', 'RELEASE_DATE']
    ]

    synonyms = {
        '案号名称': '案号',
        '法院名称': '执行法院',
    }

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
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
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
        c1 = case_identity.pop('裁判文书标题').replace(' ', '')
        case_identity['案件名称'] = c1.split('|')[0]
        case_identity['案件链接'] = c1.split('|')[1]
        _ = case_identity.pop('案件身份')
        _ = _.split('|')
        c2 = {'内容': _[0], '链接': _[1].split(' ')}
        cnt = c2['内容'].replace('-\n', '-').split('\n')
        cnt = [c.split('-') for c in cnt]
        inv = []
        for i in range(len(c2['链接'])):
            c = cnt[i]
            c.append(c2['链接'][i])
            if len(c) == 3:
                inv.append([str(_).strip().replace(' ', '').replace('\n', '') for _ in c])
            else:
                warnings.warn('裁决文书：异常的案件身份({})'.format('-'.join(c)))
        case_identity['涉案对象'] = inv
        return case_identity

    @classmethod
    def create_from_original_text(cls, text):
        pass


class RulingText(QccRequest):

    ATTRIBUTES = [
        ['标题', 'TITLE'],
        ['链接', 'URL'],
        ['原文链接', 'ORIGINAL_URL'],
        ['发布日期', 'RELEASE_DATE'],
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['执行法院', 'COURT'],

    ]

    synonyms = {
        '发表时间': '发布日期',
        '法院': '执行法院',
        '类型': '案由',
    }

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
                    # warnings.warn('Undefined key for dict of ruling text.')
                    self.BaseAttributes[k] = v
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_original_text(cls, text, **kwargs):
        """
        裁决文书的详细页，比在法律诉讼页面得到的裁决文书纲要
        内容更丰富
        :param text:
        :param kwargs:
        :return:
        """
        r = {}
        if isinstance(text, dict):
            _ = text.pop('详情信息')
            r['标题'] = _['标题']
            r['来源文字'] = _['来源']['文字']
            r['来源链接'] = _['来源']['链接']
            r['发表时间'] = text.pop('发表时间')
            tx = text.pop('文书正文')
            r['法院'] = tx.pop('法院')
            r['类型'] = tx.pop('类型')
            r['案号'] = tx.pop('案号')
            for k, v in zip(tx.keys(), tx.values()):
                if isinstance(v, dict):
                    if '内容' in v.keys():
                        r[k] = v['内容']
                else:
                    r[k] = v
        r = dict(r, **kwargs)
        return RulingText(**r)
        pass
