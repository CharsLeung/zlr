# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = copyright
author = Administrator
datetime = 2020/4/7 0007 上午 10:59
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class WorkCopyRight(BaseEntity):
    """
    作品著作权，证书编号作为id属性
    """

    ATTRIBUTES = [
        ['登记号', 'CR_NUM'],
        ['作品名称', 'NAME'],
        ['登记日期', 'CR_DATE'],
        ['登记类别', 'CR_TYPE'],
        ['发布日期', 'RELEASE_DATE'],
        # ['创作完成日期', 'END_DATE'],
    ]

    synonyms = {
        '首次发表日期': '发布日期'
    }

    primarykey = 'CR_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        crs = []

        def f(c):
            # del c['序号']
            # _ = c['证书']
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(workcopyright=WorkCopyRight(**c))

        if isinstance(content, dict):
            crs.append(f(content))
        elif isinstance(content, list):
            crs += [f(c) for c in content]
        else:
            warnings.warn('invalid type for work copy right content.')
        return crs


class SoftCopyRight(BaseEntity):
    """
    软件著作权，登记号作为id属性
    """

    ATTRIBUTES = [
        ['登记号', 'CR_NUM'],
        ['软件名称', 'NAME'],
        ['软件简称', 'ABBREVIATION'],
        ['登记日期', 'CR_DATE'],
        ['发布日期', 'RELEASE_DATE'],
        ['版本号', 'VERSION']
        # ['首次发表日期', 'START_DATE'],
        # ['创作完成日期', 'END_DATE'],
    ]

    synonyms = {
        '登记批准日期': '登记日期',
    }

    primarykey = 'CR_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        crs = []

        def f(c):
            # del c['序号']
            # _ = c['证书']
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(softcopyright=SoftCopyRight(**c))

        if isinstance(content, dict):
            crs.append(f(content))
        elif isinstance(content, list):
            crs += [f(c) for c in content]
        else:
            warnings.warn('invalid type for soft copy right content.')
        return crs