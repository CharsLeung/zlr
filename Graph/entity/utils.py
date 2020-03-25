# encoding: utf-8

"""
project = 'zlr'
file_name = 'utils'
author = 'Administrator'
datetime = '2020/3/24 0024 上午 11:26'
from = 'office desktop' 
"""
import jieba.posseg


def is_person_name(name):
    """
        判断一个名称是人名还是公司名称，输入不能为其他类别
        :param name:
        :return:
    """
    seg = jieba.posseg.cut(name.strip())
    for s in seg:
        pass


# is_person_name('重庆富迈商贸有限公司')