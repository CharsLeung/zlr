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
        return dict({
            'label': self.label,
            'from': self.start[self.start.__primarykey__],
            'to': self.end[self.end.__primarykey__],
        }, **self.properties)

    def to_pandas(self, rps):
        rps = pd.DataFrame(rps)
        rps.dropna(subset=['from', 'to'], inplace=True)
        rps.dropna(axis=1, how='all', inplace=True)
        return rps

    @staticmethod
    def append(data, header_path, data_path):
        # 只适用于头文件分离模式
        if os.path.exists(header_path):
            # 头文件存在，需要根据头文件的列名顺序追加数据
            with open(header_path, 'r+', encoding='utf-8') as f:
                exist_header = f.readline()
                exist_header = exist_header.split(',')
                new_header = list(data.columns)
                update = False
                for h in new_header:
                    if h not in exist_header:
                        exist_header.append(h)
                        update = True
                if update:
                    f.write(','.join(exist_header))
                    print('update header file:{}'.format(header_path))
                data = data.loc[:, exist_header]
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
        data_path = folder + '\{}.csv'.format(self.label)
        if split_header:
            header_path = folder + '\{}_Header.csv'.format(self.label)
            if mode[0] == 'a':
                self.append(rps, header_path, data_path)
            else:
                rps.to_csv(data_path, index=False, header=False)
                with open(header_path, 'w+', encoding='utf-8') as f:
                    header = ','.join(list(rps.columns))
                    f.write(header)
        else:
            rps.to_csv(data_path, index=False)
            pass
        return len(rps)

    def getImportCSV(self, rps):
        dtypes = dict(rps.dtypes)
        names = {'from': ':START_ID', 'to': ':END_ID', 'label': ':TYPE'}
        for k, v in zip(dtypes.keys(), dtypes.values()):
            if k in names.keys():
                continue
            if 'int' in v.name:
                names[k] = '{}:{}'.format(k, 'int')
            elif 'float' in v.name:
                names[k] = '{}:{}'.format(k, 'float')
            else:
                pass
        rps = rps.rename(columns=names)
        return rps
        pass
