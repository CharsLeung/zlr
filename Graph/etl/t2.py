# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = t2
author = Administrator
datetime = 2020/4/20 0020 上午 9:45
from = office desktop
"""
import pandas as pd

from Calf.data import BaseModel
from Calf.utils import File
from Graph import workspace
from Graph.data.utils import get_keys

metaModel = '基本信息'


def f1():
    bm = BaseModel(tn='qcc_cq_new')
    # enterprises = bm.aggregate(pipeline=[
    #     {'$match': {'metaModel': '基本信息'}},
    #     # {'$project': {'_id': 1, 'name': 1}}
    # ])

    enterprises = bm.query(
        sql={'metaModel': metaModel},
        field={'content': 1, '_id': 0},
        no_cursor_timeout=True, )

    ds = []
    data = []
    keep = []
    i = 0
    for etp in enterprises:
        i += 1
        # if i > 10:
        #     break
        cs = get_keys(etp, metaModel, return_value=True)
        for c in cs:
            _ = c.split(':')
            if len(keep):
                if sum([1 if kp in _[0] else 0 for kp in keep]):
                    data.append([_[0], _[1]])
            else:
                data.append([_[0], _[1]])

        if i % 1000 == 0:
            d = pd.DataFrame(data, columns=['k', 'v'])
            d['f'] = 1
            d = d.groupby(['k', 'v'], as_index=False).agg({
                # 'v': lambda x: '\n'.join(set([_ for _ in ('\n'.join(list(x))).split('\n')]))
                'f': 'sum'
            })
            ds.append(d)
            data.clear()
        pass

    d = pd.DataFrame(data, columns=['k', 'v'])
    d['f'] = 1
    d = d.groupby(['k', 'v'], as_index=False).agg({
        # 'v': lambda x: '\n'.join(set([_ for _ in ('\n'.join(list(x))).split('\n')]))
        'f': 'sum'
    })
    ds.append(d)
    ds = pd.concat(ds)
    ds = ds.groupby(['k', 'v'], as_index=False).agg({
        # 'v': lambda x: '\n'.join(set([_ for _ in ('\n'.join(list(x))).split('\n')]))
        'f': 'sum'
    })
    # ds.to_csv(workspace + 'flss-all.csv', index=False)
    return ds
    pass


def f2():
    # from Calf.utils import File
    # ds = pd.read_csv(workspace + 'flss-all.csv')
    # ew = pd.ExcelWriter()
    ds = f1()
    ds['k'] = ds['k'].map(lambda x: x.replace('\\', '_'))
    ds['k'] = ds['k'].map(lambda x: x.replace('/', '_'))
    ds['k'] = ds['k'].map(lambda x: x.replace('|', 'or'))
    for i, r in ds.iterrows():
        d = pd.DataFrame([_ for _ in r['v'].split('\n')], columns=['Ranges'])
        d['Ranges'] = d['Ranges'].map(lambda x: x.replace('\r', ''))
        d['Ranges'] = d['Ranges'].map(lambda x: x.replace('\n', ''))
        try:
            fp = workspace + '{}\\'.format(metaModel)
            File.check_file(fp)
            d.to_csv(fp + '{}.csv'.format(r['k']), index=False)
        except Exception as e:
            print(e)
            d.to_csv(fp + 'error-{}.csv'.format(
                i), index=False)


f2()
