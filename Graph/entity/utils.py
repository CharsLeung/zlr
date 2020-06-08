# encoding: utf-8

"""
project = 'zlr'
file_name = 'utils'
author = 'Administrator'
datetime = '2020/3/24 0024 上午 11:26'
from = 'office desktop' 
"""
import warnings
# import jieba.posseg
#
#
# def is_person_name(name):
#     """
#         判断一个名称是人名还是公司名称，输入不能为其他类别
#         :param name:
#         :return:
#     """
#     seg = jieba.posseg.cut(name.strip())
#     for s in seg:
#         pass


# is_person_name('重庆富迈商贸有限公司')


def isNull(data, null_flags=None):
    """
    对传入的data数据判断其是否为空
    >>> print(isNull('-'))
    True
    >>> print(isNull('-----'))
    True
    >>> print(isNull('#'))
    False
    >>> print(isNull('#', null_flags=['#']))
    True
    >>> print(isNull(None))
    True
    >>> print(isNull([]))
    True

    :param null_flags: list
    :param data:
    :return:
    """
    nf = [
            '-', '——', ' ', '/', '—'
            'null', 'Null', 'NULL',
            'None',
        ]
    if null_flags is not None:
        null_flags = list(set(null_flags + nf))
    else:
        null_flags = nf
    if data is None or len(data) == 0 or data in nf:
        return True
    if isinstance(data, str):
        for _nf_ in null_flags:
            data = data.replace(_nf_, '')
            if len(data) == 0:
                return True
        return False if len(data) else True
    else:
        # warnings.warn('只支持对字符类型的数据进行连续空值判断！')
        return False
    pass


def isin(flags, string, return_first=True):
    """
    判断string中是不是存在flags中的某个元素,
    若存在则返回这些元素，若string为一个字符串时，模糊匹配
    若string为一个数据时，需完全相等才会匹配
    >>> print(isin('a', 'abc'))
    ['a']
    >>> print(isin(['a', 'b'], 'abc'))
    ['a']
    >>> print(isin(['a', 'b'], 'abc', return_first=False))
    ['a', 'b']
    >>> print(isin(['a', 'b'], ['a', 'b', 'c'], return_first=False))
    ['a', 'b']
    >>> print(isin(['a', 'b'], ['a', 'bc', 'c'], return_first=False))
    ['a']

    :param return_first:
    :param flags: list or str
    :param string: str
    :return:
    """
    if isinstance(flags, str):
        flags = [flags]
    elif isinstance(flags, list):
        pass
    else:
        raise TypeError('flags必须是一个list或者str')
    if not isinstance(string, (list, str)):
        raise TypeError('string必须是一个list或者str')
    mz = []
    for f in flags:
        if f in string:
            mz.append(f)
            if return_first:
                break
    return mz