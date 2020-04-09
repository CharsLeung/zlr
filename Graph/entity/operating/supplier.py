# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = supplier
author = Administrator
datetime = 2020/4/7 0007 下午 17:53
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Supplier(QccRequest):

    """
    供应商
    """

    ATTRIBUTES = [
        ['供应商名称', 'NAME'],
        ['供应商链接', 'URL'],
        ['采购占比', 'PROPORTION'],
        ['采购金额', 'AMOUNT'],
        ['报告期', 'REPORT_DATE'],
        ['数据来源', 'SOURCE']
    ]

    synonyms = {
        '采购金额_万元': '采购金额',
        # '链接': '标的链接'
    }

    primarykey = 'URL'

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
                    warnings.warn('Undefined key for dict of supplier.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
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
            del c['序号']
            _ = c.pop('供应商')
            c['供应商名称'] = _['名称']
            c['供应商链接'] = _['url']
            return c

        if isinstance(content, dict):
            obj.append(Supplier(**f(content)))
        elif isinstance(content, list):
            obj += [Supplier(**f(c)) for c in content]
        else:
            warnings.warn('invalid type for supplier content.')
        return obj