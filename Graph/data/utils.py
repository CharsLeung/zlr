# encoding: utf-8

"""
project = 'zlr'
file_name = 'utils'
author = 'Administrator'
datetime = '2020/3/25 0025 上午 11:09'
from = 'office desktop' 
"""
import json
import pandas as pd

from Graph.exception import ExceptionInfo


def read_json(path):
    try:
        with open(path, encoding='utf-8') as file:
            ds = file.readlines()
            # ds = json.load(ds)
            ds = [eval(d) for d in ds]
            # content = json.load(file)
            # result = []
            # for line in file:
            #     result.append(json.loads(line))
            # ds = result
        return ds
    except Exception as e:
        ExceptionInfo(e)
        # print(e)
        return []


def get_keys(_, root='', sep='-', return_value=False, filter_key=[], keep_key=[]):
    """
    从一个结构层次比较复杂的dict中分析出key的结构层次，默认以'-'分割所属关系
    :param keep_key:
    :param filter_key:
    :param return_value:
    :param sep:
    :param _:
    :param root:
    :return:
    """
    category = list()
    if isinstance(_, dict):
        pass
    else:
        return []
    # keep = True if len(keep_key) else False
    for k, v in zip(_.keys(), _.values()):
        if k in filter_key:
            continue
        # if keep:
        #     for kp in keep_key:
        #         if kp not in '{}{}'.format(root, k):
        #             continue
        # print('{}-{}'.format(root, k))
        if isinstance(v, dict):
            ks = get_keys(v, '{}{}{}'.format(root, sep, k),
                          sep, return_value, filter_key)
            pass
        elif isinstance(v, list):
            if len(v):
                if len(v) == 1:
                    ks = get_keys(
                        v[0], '{}{}{}'.format(root, sep, k),
                        sep, return_value, filter_key)
                else:
                    ks = []
                    for sv in v:
                        ks += get_keys(
                            sv, '{}{}{}'.format(root, sep, k),
                            sep, return_value, filter_key)
                    d = pd.DataFrame(data=[[i.split(':')[0], i.split(':')[1]] for i in ks],
                                     columns=['k', 'v'])
                    d = d.groupby(['k'], as_index=False).agg({'v': lambda x: '\n'.join(list(x))})
                    ks = (d['k'] + ':' + d['v']).tolist()

            else:
                ks = []
        else:
            if return_value:
                ks = ['{}{}{}:{}'.format(root, sep, k, v)]
            else:
                ks = ['{}{}{}'.format(root, sep, k)]
            pass
        category += ks
    return category
