# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = t2
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/9/15 0015 下午 16:43
@from = office desktop
"""
import pandas as pd


def f1():
    data = pd.read_csv(
        r'D:\neo4j-community-3.5.14\import\图数据\JusGraph\nodes\Judgment.csv',
        usecols=[2], header=None
    )
    data = data.rename(columns={2: 'case_origin'})
    data['count'] = 1
    data = data.groupby(by=['case_origin'], as_index=False).agg({
        'count': 'count'
    })
    data.to_csv('D:\数宜信\重庆-裁判文书案由统计.csv', index=False)
    pass


f1()