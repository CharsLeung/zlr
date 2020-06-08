# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = import_and_export
author = Administrator
datetime = 2020/4/7 0007 下午 16:49
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class IAE(BaseEntity):

    """
    进出口信息
    """

    ATTRIBUTES = [
        ['注册海关', 'CUSTOMS'],
        ['经营类别', 'TYPE'],
        ['内容', 'CONTENT'],
        ['注册日期', 'REGISTRATION_DATE'],
        # ['登记编号', 'REGISTRATION_NUM'],
        # ['状态', 'STATUS']
    ]

    synonyms = {
        # '企业': '标的名称',
        # '链接': '标的链接'
    }

    primarykey = 'HASH_ID'

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
                    warnings.warn('Undefined key for dict of import-and-export'
                                  ' subject.')
                    self.BaseAttributes[k] = v
        self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        # if 'URL' in self.BaseAttributes.keys():
        #     self.BaseAttributes['URL'] = self.parser_url(
        #         self.BaseAttributes['URL'])
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
            _ = c.pop('内容')
            c['内容'] = _['内容']
            c['内容链接'] = _['链接']
            return dict(iae=IAE(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for import-and-export content.')
        return obj
