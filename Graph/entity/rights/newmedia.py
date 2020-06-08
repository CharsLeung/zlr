# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = new media
author = Administrator
datetime = 2020/4/7 0007 上午 11:29
from = office desktop
"""
import warnings

from Graph.entity import BaseEntity


class OfficialAccount(BaseEntity):

    """
    公众号
    """
    ATTRIBUTES = [
        ['微信号', 'WC_NUM'],
        ['微信公众号', 'NAME'],
        ['链接', 'URL'],
        ['简介', 'ABBREVIATION'],
    ]

    synonyms = {
        '二维码链接': '链接'
    }

    primarykey = 'WC_NUM'

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
                    warnings.warn('Undefined key for dict of official account.')
                    self.BaseAttributes[k] = v

        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        oas = []

        def f(c):
            # del c['序号']
            # _ = c['证书']
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(WeChat=OfficialAccount(**c))

        if isinstance(content, dict):
            oas.append(f(content))
        elif isinstance(content, list):
            oas += [f(c) for c in content]
        else:
            warnings.warn('invalid type for WeChat official account content.')
        return oas


class Applets(BaseEntity):

    """
    小程序
    """
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['分类', 'TYPE'],
        ['链接', 'URL'],
        ['关联公众号', 'RELATED_OA'],
        ['预估阅读量', 'READING']
    ]

    synonyms = {
        '二维码链接': '链接',
        '二维码': '链接',
        '公众号预估阅读量': '预估阅读量'
    }

    primarykey = 'NAME'

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
                    warnings.warn('Undefined key for dict of applets.')
                    self.BaseAttributes[k] = v

        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        oas = []

        def f(c):
            # del c['序号']
            # _ = c['证书']
            # c['证书名称'] = _['名称']
            # c['证书链接'] = _['链接']
            return dict(applets=Applets(**c))

        if isinstance(content, dict):
            oas.append(f(content))
        elif isinstance(content, list):
            oas += [f(c) for c in content]
        else:
            warnings.warn('invalid type for work applets content.')
        return oas


class Weibo(BaseEntity):

    """
    微博
    """
    ATTRIBUTES = [
        ['昵称', 'NAME'],
        ['链接', 'URL'],
        ['行业类别', 'TYPE'],
        ['简介', 'ABBREVIATION'],
    ]

    synonyms = {
        '微博昵称': '昵称',
        '微博链接': '链接',
        # '公众号预估阅读量': '预估阅读量'
    }

    primarykey = 'URL'

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
                    warnings.warn('Undefined key for dict of weibo.')
                    self.BaseAttributes[k] = v

        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        oas = []

        def f(c):
            # del c['序号']
            # _ = c['微博']
            # c['微博昵称'] = _['昵称']
            # c['微博链接'] = _['链接']
            return dict(weibo=Weibo(**c))

        if isinstance(content, dict):
            oas.append(f(content))
        elif isinstance(content, list):
            oas += [f(c) for c in content]
        else:
            warnings.warn('invalid type for work weibo content.')
        return oas