# encoding: utf-8

"""
project = 'zlr'
file_name = 'involve_case'
author = 'Administrator'
datetime = '2020/3/26 0026 下午 13:44'
from = 'office desktop' 
"""
import pandas as pd

from Graph.relationship import Base


class InvolveCase(Base):

    """
    涉及、参与，参加xx案件、事例、事件，case一词意味这件事比较
    正式
    """

    ATTRIBUTES = [
        # ['案件名称', 'CASE_NAME'],
        # ['案件类型', 'CASE_TYPE'],
        ['案件身份', 'CASE_IDENTITY'],  # 被告、原告等
        # ['案由', 'CASE_ORIGIN'],
        # ['案号', 'CASE_NUM'],
        # ['法院', 'COURT'],
        ['最新审理程序', 'LATEST_PRO'],
    ]

    def __init__(self, role=None, case=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if case is None:
                    continue
                if hasattr(case, a[0]):
                    properties[a[1]] = case[a[0]]
                elif hasattr(case, a[1]):
                    properties[a[1]] = case[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, role, case, **properties)
        pass

    def to_pandas(self, rps):
        relationships = {}
        for _rps_ in rps:
            _key_ = '%s_%s_%s' % (_rps_['from_label'],
                                  _rps_['label'],
                                  _rps_['to_label'])
            _rps_['label'] = _rps_['label'] + '_' + _rps_['to_label']
            if _key_ in relationships.keys():
                relationships[_key_].append(_rps_)
            else:
                relationships[_key_] = [_rps_]
            pass
        rps = {}
        for k, v in zip(relationships.keys(),
                        relationships.values()):
            v = pd.DataFrame(v)
            v.drop_duplicates(subset=['from', 'label', 'to'],
                              inplace=True, keep='last')
            v.drop(labels=['from_label', 'to_label'],
                   inplace=True, axis=1)
            v.dropna(axis=1, how='all', inplace=True)
            rps[k] = v
        return rps
        pass
