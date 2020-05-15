# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = client
author = Administrator
datetime = 2020/4/7 0007 下午 17:41
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Client(QccRequest):

    """
    客户
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['销售占比', 'PROPORTION'],
        ['销售金额', 'AMOUNT'],
        ['报告期', 'REPORT_DATE'],
        ['数据来源', 'SOURCE']
    ]

    synonyms = {
        '销售金额_万元': '销售金额',
        # '链接': '标的链接'
    }

    primarykey = 'URL'

    index = [('NAME',)]

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
                    warnings.warn('Undefined key for dict of client.')
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

        def f(_):
            c = _.pop('客户')
            if '销售金额' in _.keys():
                _ = dict(_, **cls.get_format_amount(
                    '销售金额', _.pop('销售金额')
                ))
            return dict(client=Client(**c), **_)

        # def f(c):
        #     # del c['序号']
        #     _ = c.pop('客户')
        #     c['客户名称'] = _['名称']
        #     c['客户链接'] = _['链接']
        #     return c

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for client content.')
        return obj