# encoding: utf-8

"""
project = 'Spider'
file_name = 'basemodel'
author = 'Administrator'
datetime = '2020-03-16 11:48'
IDE = PyCharm
"""
import json


def read_json(path):
    try:
        with open(path, encoding='utf-8') as file:
            ds = file.readlines()
            ds = [eval(d) for d in ds]
            # content = json.load(file)
        return ds
    except Exception as e:
        # ExceptionInfo(e)
        print(e)
        return []


# js = read_json('D:\SYR\\20200301_public\demo3.json')
# c = js['content']
# [print(k) for k in js[0]['content']['工商信息'].keys()]
from utils import File


def get_keys(_, root):
    category = []
    if isinstance(_, dict):
        pass
    else:
        return []
    for k, v in zip(_.keys(), _.values()):
        # print('{}-{}'.format(root, k))
        category.append('{}-{}'.format(root, k))
        if isinstance(v, dict):
            ks = get_keys(v, '{}-{}'.format(root, k))
            pass
        elif isinstance(v, list):
            if len(v):
                ks = get_keys(v[0], '{}-{}'.format(root, k))
            else:
                ks = []
        else:
            ks = []
            pass
        category += ks
    return category


# fs = File.get_all_file('D:\SYR\\20200229\\')
# fs = fs[-1000:]
# base_info = set()
# for p in fs:
#     js = read_json(p)
#     for d in js:
#         if d['metaModel'] == '上市信息':
#             # try:
#             cs = get_keys(d['content'], '上市信息')
#             # except Exception as e:
#             #     print(e)
#             #     print(d['content'])
#             #     continue
#             for c in cs:
#                 base_info.add(c)
#
# data = []
# for s in base_info:
#     data.append(','.join(s.split('-')) + '\n')
#
# with open('D:\SYR\\ssxx.csv', 'w', encoding='gbk') as f:
#     f.writelines(data)
#     pass
