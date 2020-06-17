# encoding: utf-8

"""
project = zlr
file_name = have
author = Administrator
datetime = 2020/3/27 0027 上午 10:53
from = office desktop
"""
import pandas as pd
from Graph.relationship import Base


class Have(Base):
    """
    囊括的关系包括：有、具有、拥有、具备、有着、
    带有、含有、抱有、所有、占有等
    """

    def __init__(self, owner=None, object=None, **kwargs):
        Base.__init__(self, owner, object, **kwargs)
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
