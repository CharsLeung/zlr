# encoding: utf-8

"""
project = zlr
file_name = punishment
author = Administrator
datetime = 2020/4/1 0001 上午 11:38
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class Punishment(BaseEntity):

    """
    行政处罚
    """
    ATTRIBUTES = [
        ['决定文书号', 'DECISION_RULING_NUM'],
        ['处罚事由', 'PUNISH_ORIGIN'],
        ['处罚内容', 'PUNISH_CONTENT'],
        ['处罚日期', 'PUNISH_DATE'],
        ['公示日期', 'RELEASE_DATE'],
        ['决定机关', 'DECISION_AGENCY'],
        ['链接', 'URL'],
        ['决定机关类型', 'DECISION_AGENCY_TYPE']
    ]

    synonyms = {
        '决定文书号': '决定文书号',
        '决定书文号': '决定文书号',
        '违法行为类型': '处罚事由',
        '违法类型': '处罚事由',
        '处罚事由': '处罚事由',
        '行政处罚内容': '处罚内容',
        '决定日期': '处罚日期',
        '处罚决定日期': '处罚日期',
        '决定机关': '决定机关',
        '处罚单位': '决定机关',
        '处罚机关': '决定机关',
    }

    primarykey = 'DECISION_RULING_NUM'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if self[self.primarykey] is None or \
                len(str(self[self.primarykey])) < 2:
            self[self.primarykey] = '%s_%s' % (
                self.label,
                self.getHashValue(str(self.BaseAttributes))
            )
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
                    __ = c.pop('决定文书号')
                    c['决定文书号'] = __['名称']
                    c['链接'] = __['链接']
                    return dict(punishment=Punishment(**c))
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass
            if isinstance(content, dict):
                content['决定机关类型'] = agency
                _ = cnt1(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['决定机关类型'] = agency
                    _ = cnt1(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        if agency == '税务局':
            def cnt2(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    # ruling = c.pop('决定文书号')
                    # c = dict(c)
                    return dict(punishment=Punishment(**c))
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass
            if isinstance(content, dict):
                content['决定机关类型'] = agency
                _ = cnt2(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['决定机关类型'] = agency
                    _ = cnt2(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        if agency == '信用中国':
            def cnt2(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    # ruling = c.pop('决定文书号')
                    # c = dict(c)
                    return dict(punishment=Punishment(**c))
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass
            if isinstance(content, dict):
                content['决定机关类型'] = agency
                _ = cnt2(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['决定机关类型'] = agency
                    _ = cnt2(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        if agency == '其他':
            def cnt2(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    # ruling = c.pop('决定文书号')
                    # c = dict(c)
                    return dict(punishment=Punishment(**c))
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass
            if isinstance(content, dict):
                content['决定机关类型'] = agency
                _ = cnt2(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['决定机关类型'] = agency
                    _ = cnt2(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')

        if agency == '环保局':
            def cnt2(c):
                if isinstance(c, dict):
                    if '序号' in c.keys():
                        del c['序号']
                    # ruling = c.pop('决定文书号')
                    # c = dict(c)
                    return dict(punishment=Punishment(**c))
                else:
                    warnings.warn('invalid type for Punishment, need a dict.')
                    return None
                    pass
            if isinstance(content, dict):
                content['决定机关类型'] = agency
                _ = cnt2(content)
                if _ is not None:
                    ps.append(_)
                pass
            elif isinstance(content, list):
                for cnt in content:
                    cnt['决定机关类型'] = agency
                    _ = cnt2(cnt)
                    if _ is not None:
                        ps.append(_)
            else:
                warnings.warn('invalid type for Punishment, need a dict.')
        return ps