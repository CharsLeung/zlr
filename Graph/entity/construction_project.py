# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = construction_project
author = Administrator
datetime = 2020/5/8 0008 下午 16:52
from = office desktop
"""
import warnings

from Graph.entity import QccRequest


class ConstructionProject(QccRequest):

    """
    建筑工程项目
    """

    ATTRIBUTES = [
        ['项目名称', 'NAME'],
        ['项目编码', 'PROJECT_NUM'],
        ['项目类别', 'PROJECT_TYPE'],
        ['项目属地', 'PROJECT_CITY'],
    ]

    synonyms = {
        # '状态': '经营状态',
        # '认缴出资额_万元': '认缴出资额',
        # '链接': '股东链接'
    }

    primarykey = 'PROJECT_NUM'

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
                    warnings.warn('Undefined key for dict of invested.')
                    self.BaseAttributes[k] = v
        if 'URL' in self.BaseAttributes.keys():
            self.BaseAttributes['URL'] = self.parser_url(
                self.BaseAttributes['URL'])
        pass