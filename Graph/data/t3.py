# encoding: utf-8

"""
project = zlr
file_name = t3
author = Administrator
datetime = 2020/4/2 0002 下午 14:04
from = office desktop
"""
from Calf.data import BaseModel
from Graph.data.utils import read_json
from Graph.utils import File

# fs = File.get_all_file('D:\graph_data\\temp.json\\')
fs = ['D:\graph_data\\temp.json']
bm = BaseModel(tn='qcc_cq_new_1')
data = []
count = 0
for p in fs:
        js = read_json(p)
        data += js
        if len(data) > 0:
            _ = len(data)
            count += _
            print('deal:', count)
            bm.insert_batch(data)
            data.clear()

pass