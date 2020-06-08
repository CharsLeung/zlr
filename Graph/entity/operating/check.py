# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = check
author = Administrator
datetime = 2020/4/7 0007 下午 18:11
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Check(BaseEntity):

    """
    抽查检查
    """

    ATTRIBUTES = [
        ['实施机关', 'CHECK_AGENCY'],
        ['类型', 'TYPE'],
        ['日期', 'DATE'],
        ['结果', 'RESULT'],
    ]

    synonyms = {
        '检查实施机关': '实施机关',
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
                    warnings.warn('Undefined key for dict of check.')
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
            # _ = c.pop('描述')
            # c['项目描述'] = _['描述']
            # c['项目链接'] = _['描述链接']
            return dict(check=Check(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for check content.')
        return obj


class RandomCheck(BaseEntity):

    """
    双随机抽查
    """

    ATTRIBUTES = [
        ['任务编号', 'TASK_NUM'],
        ['任务名称', 'NAME'],
        ['抽查机关', 'CHECK_AGENCY'],
        ['完成日期', 'DATE'],
    ]

    synonyms = {
        # '企业': '标的名称',
        # '链接': '标的链接'
    }

    primarykey = 'TASK_NUM'

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
                    warnings.warn('Undefined key for dict of random-check.')
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
            # _ = c.pop('描述')
            # c['项目描述'] = _['描述']
            # c['项目链接'] = _['描述链接']
            return dict(check=RandomCheck(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for random-check content.')
        return obj