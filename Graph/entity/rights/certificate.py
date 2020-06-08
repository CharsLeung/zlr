# encoding: utf-8

"""
project = zlr
file_name = certificate
author = Administrator
datetime = 2020/4/3 0003 上午 9:22
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class Certificate(BaseEntity):
    """
    资质证书，证书编号作为id属性
    """

    ATTRIBUTES = [
        ['证书编号', 'CTF_NUM'],
        ['证书类型', 'CTF_TYPE'],
        ['证书名称', 'NAME'],
        ['证书链接', 'URL'],
        ['发证日期', 'START_DATE'],
        ['截止日期', 'END_DATE'],
        ['发证机关', 'AGENCY'],
    ]

    synonyms = {
        '资质证书号': '证书编号',
        '资质类型': '证书类型',
        '资质名称': '证书名称',
        '证书有效期': '截止日期'
    }

    primarykey = 'CTF_NUM'

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
                    warnings.warn('Undefined key for dict of Certificate.')
                    self.BaseAttributes[k] = v
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        ctfs = []

        def f(c):
            # del c['序号']
            _ = c.pop('证书')
            c['证书名称'] = _['名称']
            c['证书链接'] = _['链接']
            return dict(certificate=Certificate(**c))

        if isinstance(content, dict):
            ctfs.append(f(content))
        elif isinstance(content, list):
            ctfs += [f(c) for c in content]
        else:
            warnings.warn('invalid type for Certificate content.')
        return ctfs
