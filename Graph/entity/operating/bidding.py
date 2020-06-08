# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = Bidding
author = Administrator
datetime = 2020/4/7 0007 下午 17:17
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Bidding(BaseEntity):

    """
    招投标信息
    """

    ATTRIBUTES = [
        ['项目描述', 'DESCRIPTION'],
        ['项目链接', 'URL'],
        ['项目分类', 'TYPE'],
        ['所属地区', 'AREA'],
        ['发布日期', 'RELEASE_DATE']
    ]

    synonyms = {
        # '企业': '标的名称',
        # '链接': '标的链接'
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
                    warnings.warn('Undefined key for dict of bidding.')
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
            # del c['序号']
            _ = c.pop('描述')
            c['项目描述'] = _['描述']
            c['项目链接'] = _['链接']
            return dict(bidding=Bidding(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for bidding content.')
        return obj