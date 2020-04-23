# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = t1
author = Administrator
datetime = 2020/4/20 0020 上午 9:20
from = office desktop
"""
import pandas as pd

from Calf.data import BaseModel
from Calf.utils import File
from Graph import workspace
from Graph.data.utils import get_keys


def get_old_keys():
    bm = BaseModel(tn='qcc_cq_new')

    metaModel = '公司新闻'

    enterprises = bm.query(
        sql={'metaModel': metaModel},
        field={'content': 1, '_id': 0},
        no_cursor_timeout=True)
    i = 0
    exit_filed = set()
    for etp in enterprises:
        i += 1
        # if i > 10:
        #     break
        cs = get_keys(etp, metaModel, '$')
        for c in cs:
            exit_filed.add(c)
        pass

    data = []
    for s in exit_filed:
        _ = s.split('$')
        d = []
        for i in _:
            if len(i):
                d.append(i)
        data.append(','.join(d) + '\n')
    fp = workspace + '{}\\'.format(metaModel)
    File.check_file(fp)
    with open(fp + '字段.csv', 'w', encoding='gbk') as f:
        f.writelines(data)
        pass
    # exit_filed = pd.DataFrame(data=[f for f in exit_filed], columns=['key'])
    # fp = workspace + '{}\\'.format(metaModel)
    # File.check_file(fp)
    # exit_filed.to_csv(fp + '字段.csv', index=False)
    pass


get_old_keys()


def match():
    import re
    regs = pd.read_excel(
        workspace + '企查查-属性字段一览表1.1.xlsx',
        sheet_name='基本信息（标准结构）',
        header=[1])
    regs['匹配模式'] = regs['匹配模式'].map(
        lambda x: re.sub('\d+', lambda _: '\d+', x)
    )
    regs['匹配模式-修正'].fillna(regs['匹配模式'], inplace=True)
    pass


# match()
