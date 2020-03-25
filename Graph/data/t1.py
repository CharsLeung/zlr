# encoding: utf-8

"""
project = 'Spider'
file_name = 't1'
author = 'Administrator'
datetime = '2020-03-18 10:57'
IDE = PyCharm
"""
import pandas as pd

from Calf.data import BaseModel
from Graph import workspace
from Graph.data.utils import get_keys


bm = BaseModel(tn='qcc_cq_new')
enterprises = bm.aggregate(pipeline=[
            {'$match': {'metaModel': '基本信息'}},
            # {'$project': {'_id': 1, 'name': 1}}
        ])

ds = []
data = []
keep = ['所属行业']
i = 0
for etp in enterprises:
    i += 1
    # if i > 10:
    #     break
    cs = get_keys(etp, '基本信息', return_value=True,
                  filter_key=['_id', 'metaModel', 'source', 'url',
                              'headers', 'get', 'date'])
    for c in cs:
        _ = c.split(':')
        if sum([1 if kp in _[0] else 0 for kp in keep]):
            data.append([_[0], _[1]])

    if i % 1000 == 0:
        d = pd.DataFrame(data, columns=['k', 'v'])
        d = d.groupby(['k'], as_index=False).agg({
            'v': lambda x: '\n'.join(set([_ for _ in ('\n'.join(list(x))).split('\n')]))
        })
        ds.append(d)
        data.clear()
    pass

d = pd.DataFrame(data, columns=['k', 'v'])
d = d.groupby(['k'], as_index=False).agg({
    'v': lambda x: '\n'.join(set([_ for _ in ('\n'.join(list(x))).split('\n')]))
})
ds.append(d)
ds = pd.concat(ds)
ds.to_csv(workspace + 'industry.csv', index=False)
pass