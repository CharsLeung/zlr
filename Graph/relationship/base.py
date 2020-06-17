# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = base
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/2 0002 下午 16:20
@from = office desktop
"""
import re
import os
import pandas as pd

from py2neo import Relationship


class Base:
    """
    所有关系类的基类
    """

    ATTRIBUTES = []

    name_pattern = re.compile('[A-Z]+[a-z]+')

    def __init__(self, start=None, end=None, **kwargs):
        self.start = start
        self.end = end
        self.properties = kwargs
        pass

    @property
    def label(self):
        lb = str(self.__class__.__name__)
        lb = list(re.findall(self.name_pattern, lb))
        lb = '_'.join([l.upper() for l in lb])
        return lb

    def get_relationship(self):
        return Relationship(
            self.start,
            self.label,
            self.end,
            **self.properties
        )
        pass

    def to_dict(self):
        sl = list(self.start.labels)[0]
        el = list(self.end.labels)[0]
        return dict({
            'label': self.label,
            'from': self.start[self.start.__primarykey__],
            'from_label': sl,
            'to': self.end[self.end.__primarykey__],
            'to_label': el,
        }, **self.properties)
        pass

    def to_pandas(self, rps):
        relationships = {}
        for _rps_ in rps:
            _key_ = '%s_%s_%s' % (_rps_['from_label'],
                                  _rps_['label'],
                                  _rps_['to_label'])
            # _rps_['label'] = _rps_['label'] + '_' + _rps_.pop('to_label')
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

    @staticmethod
    def append(data, header_path, data_path):
        # 只适用于头文件分离模式
        if len(data) == 0:
            return
        if os.path.exists(header_path):
            # 头文件存在，需要根据头文件的列名顺序追加数据
            with open(header_path, 'r+', encoding='utf-8') as f:
                exist_header = f.readline()
                exist_header = exist_header.split(',')
                new_header = list(data.columns)
                update = []
                for h in new_header:
                    if h not in exist_header:
                        exist_header.append(h)
                        update.append(h)
                if len(update):
                    f.write(',' + ','.join(update))
                    print('update header file:{}'.format(header_path))
                try:
                    data = data.loc[:, exist_header]
                except Exception as e:
                    print(e)
                    print(new_header)
                    print(exist_header)
                data.to_csv(data_path, index=False,
                            header=False, mode='a')
                pass
        else:
            data.to_csv(data_path, index=False,
                        header=False, mode='a')
            with open(header_path, 'w+', encoding='utf-8') as f:
                header = ','.join(list(data.columns))
                f.write(header)
                pass

    def to_csv(self, rps, folder, split_header=False, mode='replace'):
        count = 0
        for _label_, _rps_ in zip(rps.keys(), rps.values()):
            data_path = folder + '\{}.csv'.format(_label_)
            if split_header:
                header_path = folder + '\{}_Header.csv'.format(_label_)
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
            lb = _label_.split('_{}_'.format(self.label))
            names = {'from': ':START_ID(%s)' % lb[0],
                     'to': ':END_ID(%s)' % lb[1],
                     'label': ':TYPE'}
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

    def read_csv(self, data_path, header_path=None):
        if not os.path.isfile(data_path):
            data_path = os.path.join(data_path, '%s.csv' % self.label)
            if not os.path.isfile(data_path):
                raise FileNotFoundError('not found related data file.')

        if header_path is not None:
            data = pd.read_csv(data_path, header=None,
                               engine='python', encoding='utf-8')
            if not os.path.isfile(header_path):
                header_path = os.path.join(header_path, '%s_Header.csv' % self.label)
                if not os.path.isfile(header_path):
                    raise FileNotFoundError('not found related header file.')
            with open(header_path, 'r+', encoding='utf-8') as f:
                header = f.readline()
                header = header.split(',')
                data = data.rename(columns=dict(zip(list(data.columns), header)))
        else:
            data = pd.read_csv(data_path)
        return data
