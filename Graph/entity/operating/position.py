# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = recruitment
author = Administrator
datetime = 2020/4/7 0007 下午 17:05
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class Position(QccRequest):

    """
    职位
    """

    ATTRIBUTES = [
        ['职位', 'POSITION'],
        ['链接', 'URL'],
    ]

    synonyms = {
        '招聘职位': '职位',
        '招聘链接': '职位'
    }

    primarykey = 'POSITION'

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
                    warnings.warn('Undefined key for dict of recruitment.')
                    self.BaseAttributes[k] = v
        # self.BaseAttributes['HASH_ID'] = hash(str(self.BaseAttributes))
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
            _ = c.pop('职位')
            return dict(position=Position(**_), **c)

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for recruitment content.')
        return obj