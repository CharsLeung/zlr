# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = compete
author = Administrator
datetime = 2020/4/10 0010 下午 15:34
from = office desktop
"""
from Graph.relationship import Base


class Compete(Base):

    """
    囊括的关系包括：竞争, 竞, 对抗, 赛, 比等
    主要含义指两者之间存在业务、产品竞争
    """

    def __init__(self, owner=None, competitor=None, **kwargs):
        Base.__init__(self, owner, competitor, **kwargs)
        pass