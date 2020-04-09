# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = license
author = Administrator
datetime = 2020/4/7 0007 下午 16:21
from = office desktop
"""
import warnings
from Graph.entity import QccRequest


class License(QccRequest):
    """
    行政许可
    """
    ATTRIBUTES = [
        ['许可文书号', 'PERMIT_LICENSE_NUM'],
        ['许可文件名', 'NAME'],
        ['许可内容', 'CONTENT'],
        ['许可机关', 'PERMIT_AGENCY'],
        ['有效期自', 'START_DATE'],
        ['有效期至', 'END_DATE'],
        ['许可机关类型', 'PERMIT_AGENCY_TYPE']
    ]

    synonyms = {
        '许可文件编号': '许可文书号',
        '许可文件名称': '许可文件名',
        # '处罚事由': '处罚事由',
        # '行政处罚内容': '处罚内容',
        # '决定日期': '处罚日期',
        # '处罚决定日期': '处罚日期',
        # '决定机关': '决定机关',
    }

    primarykey = 'PERMIT_LICENSE_NUM'

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
                    warnings.warn('Undefined key for dict of license.')
                    self.BaseAttributes[k] = v
        if self.primarykey not in self.BaseAttributes.keys() or self.BaseAttributes[
            self.primarykey] is None or len(self.BaseAttributes[self.primarykey]) < 2:
            self.BaseAttributes[self.primarykey] = 'HASH-{}'.format(
                hash(str(self.BaseAttributes)))
        pass

    @classmethod
    def create_from_dict(cls, content, agency):
        """
        从一个dict或者是dict的list中创建punishment对象
        :param agency: 工商局 or 税务局,两种类型的数据结构不一样
        :param content:
        :return: list
        """
        ps = []
        if agency == '工商局':
            def cnt1(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    return License(**c)
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass

            if isinstance(content, dict):
                content['许可机关类型'] = agency
                _ = cnt1(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['许可机关类型'] = agency
                    _ = cnt1(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        if agency == '信用中国':
            def cnt2(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    _ = c.pop('内容')
                    l = {
                        '许可文书号': c['决定文书号'],
                        '许可机关': c['许可机关'],
                        '有效期自': c['决定日期'],
                        '许可内容': _['post链接'],
                        '许可机关类型': c['许可机关类型']
                    }
                    # c = dict(c, **ruling)
                    return License(**l)
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass

            if isinstance(content, dict):
                content['许可机关类型'] = agency
                _ = cnt2(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['许可机关类型'] = agency
                    _ = cnt2(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        return ps
