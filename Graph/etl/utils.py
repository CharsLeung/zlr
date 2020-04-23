# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = utils
author = Administrator
datetime = 2020/4/23 0023 上午 9:15
from = office desktop
"""


def dictMerge(dic1, *args):
    """
    嵌套字典合并, 将新字典合并到旧字典中,新旧字典
    将自顶向下合并，不会将新字典合并到旧字典的子树
    当中去，例如eg3.的结果不会是：
    {'A': {'A1': {'B1': 1, 'B2': 3}, 'A2': 2}}
    eg1.
    >>> d1={'A': 1, 'B': 2}
    >>> d2={'A': 2, 'B': 2}
    >>> dictMerge(d1, d2)
    >>> d1
    {'A': [1, 2], 'B': 2}
    eg2.
    >>> d1={'A':{'A1':1, 'A2':2}}
    >>> d2={'A':{'A1':1, 'B2':2}}
    >>> dictMerge(d1, d2)
    >>> d1
    {'A': {'A1': [1, 1], 'A2': 2, 'B2': 2}}
    eg3.
    >>> d1={'A':{'A1':{'B1': 1}, 'A2':2}}
    >>> d2={'A1':{'B2':3}}
    >>> dictMerge(d1, d2)
    >>> d1
    {'A': {'A1': {'B1': 1}, 'A2': 2}, 'A1': {'B2': 3}}
    :param dic1: 旧字典
    :param args: 新字典
    :return:
    """
    for dic2 in args:
        for i in dic2:
            if i in dic1:
                # 如果i在原来的dict当中
                if isinstance(dic1[i], dict) and isinstance(
                        dic2[i], dict):
                    dictMerge(dic1[i], dic2[i])
                else:
                    if isinstance(dic2[i], list):
                        dic1[i] = dic1[i].append(dic2[i])
                    else:
                        dic1[i] = [dic1[i], dic2[i]]
            else:
                dic1[i] = dic2[i]
    return dic1


# d1 = {'A':{'A1':{'B1': 1}, 'A2':2}}
# d2 = {'A1':{'B2':3}}
# # dictMerge(d1, d2)
# print(dictMerge(d1, d2))


def dictTranspose2List(dct):
    """
    把一个dict看做一颗树，这颗树的叶节点取值为长度相
    等的list，此函数将这颗树转化成多颗树，转换后的树
    的叶节点取值是原来list中的一个值。
    dct是一个dict，将取值类型为list的节点视为叶节点，
    list当中的值视为最小单位，不能再往下分割，叶节点
    的长度相等，此过程从上到下进行
    eg1.
    >>> dct = {'A': {
    ...            'A1':['x1', 'x2'],
    ...            'A2':['n1', 'n2']
    ...        },
    ...        'B':['m1','m2']
    ...    }
    >>> dictTranspose2List(dct)
    [{'A': {'A1':'x1','A2':'n1'}，'B':'m1'},
     {'A': {'A1':'x2','A2':'n2'}，'B':'m2'}
    ]
    eg2.
    >>> dct = {'A': [{
    ...            'A1':'x1',
    ...            'A2':'n1'
    ...        },{
    ...            'A1':'x1',
    ...            'A2':'n1'
    ...        }],
    ...        'B':['m1','m2']
    ...    }
    >>> dictTranspose2List(dct)
    [{'A': {'A1': 'x1', 'A2': 'n1'}, 'B': 'm1'},
     {'A': {'A1': 'x1', 'A2': 'n1'}, 'B': 'm2'}
    ]
    eg3.
    >>> dct = {'A': [{
    ...            'A1':['x1', 'x2'],
    ...            'A2':['n1', 'n2']
    ...        },{
    ...            'A1':['x1-', 'x2-'],
    ...            'A2':['n1-', 'n2-']
    ...        }],
    ...        'B':['m1','m2']
    ...    }
    >>> dictTranspose2List(dct)
    [{'A': {'A1': ['x1', 'x2'], 'A2': ['n1', 'n2']}, 'A1': 'm1'},
     {'A': {'A1': ['x1-', 'x2-'], 'A2': ['n1-', 'n2-']}, 'A1': 'm2'}
     ]
    需要注意到eg3的例子中A.A1下的['x1', 'x2']并没有
    被拆开，因为A1所在的层是一个list层，A1层被当做叶
    节点，没有继续往下分了，其他几个位置也是一样的。
    :param dct: dict
    :return: list or ValueError
    """

    def func(dic, root=None):
        ds = []
        if isinstance(dic, dict):
            for k_, v_ in zip(dic.keys(), dic.values()):
                if isinstance(v_, list):
                    d = []
                    for i in range(len(v_)):
                        if root is None:
                            d.append({k_: v_[i]})
                        else:
                            d.append({root: {k_: v_[i]}})
                        # dict(**{k_: v_[i]})
                    ds.append(d)
                elif isinstance(v_, dict):
                    ds += func(v_, k_)
                else:
                    ds.append([{k_: v_}])
                    pass
        return ds
        pass

    grid = func(dct)
    if len(grid):
        # 转置
        shape = [len(g) for g in grid]
        if max(shape) != min(shape):
            raise ValueError('non-standard data format.')
        grid = [[row[i] for row in grid] for i in range(len(grid[0]))]
        T = []
        for g in grid:
            if len(g) > 1:
                T.append(dictMerge(g[0], *g[1:]))
            else:
                T.append(g[0])
        # _ = [dictMerge(g[0], *g[1:]) for g in grid]
        return T
    else:
        return []


# dd = {'A': [{
#     'A1': ['x1', 'x2'],
#     'A2': ['n1', 'n2']
#     }, {
#     'A1': ['x1-', 'x2-'],
#     'A2': ['n1-', 'n2-']
#     }],
#     'A1': ['m1', 'm2']
# }
#
# print(dictTranspose2List(dd))
# pass


class JsonPath:

    def __init__(self, paths):
        self.paths = list(set(paths))
        pass

    def father_path(self, path):
        """
        父级路径，json这种结构中，父路径只会有一个
        :param path:
        :return:
        """
        for p in self.paths:
            if len(p) > len(path) and path in p:
                return

    def son_path(self, path):
        """
        子路径
        :param path:
        :return:
        """
        ps = []
        fp = '-'.join(path.split('-')[:-1])
        for p in self.paths:
            if len(p) > len(fp) and fp in p:
                ps.append(p)
        return ps
