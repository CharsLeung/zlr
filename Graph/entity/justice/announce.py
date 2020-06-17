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


def split_case_identity(case_identity):
    ds = []
    names = case_identity['名称']
    urls = case_identity['链接']
    if names is None:
        return []
    names = BaseEntity.textPhrase(names).split(',')
    if urls is None:
        urls = []
    else:
        urls = urls.split(' ')
    if len(names) > len(urls):
        urls = urls + [None for i in range(len(names) - len(urls))]
    for n, u in zip(names, urls):
        ds.append({'名称': n, '链接': u})
    return ds


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
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.format_url(
        #         self['URL'])
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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
            defendant = split_case_identity(defendant)
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            plaintiff = split_case_identity(plaintiff)
            ca = CourtAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for court announce.')
        return obj

    # @classmethod
    # def split_case_identity(cls, case_identity):
    #     ds = []
    #     names = case_identity['名称']
    #     urls = case_identity['链接']
    #     if names is None:
    #         return []
    #     names = cls.textPhrase(names).split(',')
    #     if urls is None:
    #         urls = []
    #     else:
    #         urls = urls.split(' ')
    #     if len(names) > len(urls):
    #         urls = urls + [None for i in range(len(names) - len(urls))]
    #     for n, u in zip(names, urls):
    #         ds.append({'名称': n, '链接': u})
    #     return ds


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
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.format_url(
        #         self['URL'])
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
            defendant = split_case_identity(defendant)
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            plaintiff = split_case_identity(plaintiff)
            ca = OpenAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for court open announce.')
        return obj

    # @classmethod
    # def split_case_identity(cls, case_identity):
    #     ds = []
    #     names = case_identity['名称']
    #     urls = case_identity['链接']
    #     names = cls.textPhrase(names).split(',')
    #     urls = urls.split(' ')
    #     if len(names) > len(urls):
    #         urls = urls + [None for i in range(len(names) - len(urls))]
    #     for n, u in zip(names, urls):
    #         ds.append({'名称': n, '链接': u})
    #     return ds


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
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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
            defendant = split_case_identity(defendant)
            plaintiff = c.pop('公诉人/原告/上诉人/申请人')
            plaintiff = split_case_identity(plaintiff)
            ca = DeliveryAnnounce(**c)
            return dict(defendant=defendant, plaintiff=plaintiff, announce=ca)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for delivery announce.')
        return obj

    # @classmethod
    # def split_case_identity(cls, case_identity):
    #     ds = []
    #     names = case_identity['名称']
    #     urls = case_identity['链接']
    #     names = cls.textPhrase(names).split(',')
    #     urls = urls.split(' ')
    #     if len(names) > len(urls):
    #         urls = urls + [None for i in range(len(names) - len(urls))]
    #     for n, u in zip(names, urls):
    #         ds.append({'名称': n, '链接': u})
    #     return ds