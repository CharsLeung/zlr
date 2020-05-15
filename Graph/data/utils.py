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


def read_json(path):
    try:
        with open(path, encoding='utf-8') as file:
            # ds = file.readlines()
            # # ds = json.load(ds)
            # ds = [json.load(d) for d in ds]
            # content = json.load(file)
            result = []
            for line in file:
                result.append(json.loads(line))
            ds = result
        return ds
    except Exception as e:
        # ExceptionInfo(e)
        print(e)
        return []


def get_keys(_, root='', sep='-', return_value=False,
             filter_key=[], keep_key=[], value_sep='\n'):
    """
    从一个结构层次比较复杂的dict中分析出key的结构层次，默认以'-'分割所属关系
    :param value_sep:
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
        print('-----')
        return category
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
                          sep, return_value, filter_key, keep_key, value_sep)
            pass
        elif isinstance(v, list):
            if len(v):
                if len(v) == 1:
                    ks = get_keys(
                        v[0], '{}{}{}'.format(root, sep, k),
                        sep, return_value, filter_key, keep_key, value_sep)
                else:
                    ks = []
                    for sv in v:
                        ks += get_keys(
                            sv, '{}{}{}'.format(root, sep, k),
                            sep, return_value, filter_key, keep_key, value_sep)

                    if return_value:
                        data = [[i.split(':')[0], i.split(':')[1]] for i in ks]
                        d = pd.DataFrame(data=data,
                                         columns=['k', 'v'])
                        d = d.groupby(['k'], as_index=False).agg({
                            'v': lambda x: '{}'.format(value_sep).join(list(x))
                        })
                        ks = (d['k'] + ':' + d['v']).tolist()
                    else:
                        ks = [i.split(':')[0] for i in ks]

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


def dictMerge(dic1, *args):
    """
    嵌套字典合并, 将新字典合并到旧字典中
    :param dic1: 旧字典
    :param dic2: 新字典
    :return:
    """
    # for i in dic2:
    #     if i in dic1:
    #         if isinstance(dic1[i], dict) and isinstance(dic2[i], dict):
    #             dictMerge(dic1[i], dic2[i])
    #     else:
    #         dic1[i] = dic2[i]
    for dic2 in args:
        for i in dic2:
            if i in dic1:
                if isinstance(dic1[i], dict) and isinstance(dic2[i], dict):
                    dictMerge(dic1[i], dic2[i])
            else:
                dic1[i] = dic2[i]
    return dic1
