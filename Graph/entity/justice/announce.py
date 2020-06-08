# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = announce
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/8 0008 下午 15:30
@from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class CourtAnnounce(BaseEntity):

    """
    法院公告
    """

    ATTRIBUTES = [
        # ['文书标题', 'CASE_NAME'],
        # ['文书链接', 'URL'],
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['公告人', 'COURT'],
        ['发布日期', 'RELEASE_DATE'],
        ['公告类型', 'TYPE']
    ]

    synonyms = {
        '刊登日期': '发布日期',
        # '链接': '标的链接'
    }

    primarykey = 'CASE_NUM'

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
                    warnings.warn('Undefined key for dict of court announce.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.format_url(
                self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            defendant = c.pop('被告人/被告/被上诉人/被申请人')
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            ca = CourtAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for court announce.')
        return obj


class OpenAnnounce(BaseEntity):

    """
    开庭公告
    """

    ATTRIBUTES = [
        # ['文书标题', 'CASE_NAME'],
        # ['文书链接', 'URL'],
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['开庭日期', 'OPEN_DATE'],
    ]

    synonyms = {
        '开庭时间': '开庭日期',
        # '链接': '标的链接'
    }

    primarykey = 'CASE_NUM'

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
                    warnings.warn('Undefined key for dict of court open announce.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.format_url(
                self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            defendant = c.pop('被告人/被告/被上诉人/被申请人')
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            ca = OpenAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for court open announce.')
        return obj


class DeliveryAnnounce(BaseEntity):

    """
    送达公告
    """

    ATTRIBUTES = [
        # ['文书标题', 'CASE_NAME'],
        # ['文书链接', 'URL'],
        ['案由', 'CASE_ORIGIN'],
        ['案号', 'CASE_NUM'],
        ['发布日期', 'RELEASE_DATE'],
        ['公告名称', 'NAME']
    ]

    synonyms = {
        # '刊登日期': '发布日期',
        # '链接': '标的链接'
    }

    primarykey = 'CASE_NUM'

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
                    warnings.warn('Undefined key for dict of delivery announce.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.format_url(
                self.BaseAttributes['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            defendant = c.pop('被告人/被告/被上诉人/被申请人')
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            ca = CourtAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for delivery announce.')
        return obj