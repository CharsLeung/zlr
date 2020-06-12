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

    def to_dict(self):
        return dict({
            'label': self.label,
            'from': self.start[self.start.__primarykey__],
            'from_label': list(self.start.labels)[0],
            'to': self.end[self.end.__primarykey__],
            'to_label': list(self.end.labels)[0],
        }, **self.properties)

    def to_pandas(self, rps):
        relationships = {}
        for _rps_ in rps:
            _key_ = '%s_%s_%s' % (_rps_.pop('from_label'),
                                  _rps_['label'],
                                  _rps_.get('to_label'))
            _rps_['label'] = _rps_['label'] + '_' + _rps_.pop('to_label')
            if _key_ in relationships.keys():
                relationships[_key_].append(_rps_)
            else:
                relationships[_key_] = [_rps_]
            pass
        rps = {}
        for k, v in zip(relationships.keys(),
                        relationships.values()):
            v = pd.DataFrame(v)
            v.dropna(axis=1, how='all', inplace=True)
            # v.drop(labels=['from_label', 'to_label'], inplace=True)
            rps[k] = v
        return rps

    def to_csv(self, rps, folder, split_header=False, mode='r'):
        count = 0
        for _label_, _rps_ in zip(rps.keys(), rps.values()):
            data_path = folder + '\{}_{}.csv'.format(self.label, _label_)
            if split_header:
                header_path = folder + '\{}_{}_Header.csv'.format(self.label, _label_)
                if mode[0] == 'a':
                    self.append(_rps_, header_path, data_path)
                else:
                    _rps_.to_csv(data_path, index=False, header=False)
                    with open(header_path, 'w+', encoding='utf-8') as f:
                        header = ','.join(list(_rps_.columns))
                        f.write(header)
            else:
                _rps_.to_csv(data_path, index=False)
                pass
            count += len(_rps_)
        return count

    def getImportCSV(self, rps):
        for _label_, _rps_ in zip(rps.keys(), rps.values()):
            dtypes = dict(_rps_.dtypes)
            lb = _label_.split('_')
            names = {'from': ':START_ID(%s)' % lb[0],
                     'to': ':END_ID(%s)' % lb[2], 'label': ':TYPE'}
            for k, v in zip(dtypes.keys(), dtypes.values()):
                if k in names.keys():
                    continue
                if 'int' in v.name:
                    names[k] = '{}:{}'.format(k, 'int')
                elif 'float' in v.name:
                    names[k] = '{}:{}'.format(k, 'float')
                else:
                    pass
            rps[_label_] = _rps_.rename(columns=names)
        return rps
        pass
