# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = produce
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/10 0010 上午 11:19
@from = office desktop
"""
from Graph.relationship import Base


class Produce(Base):

    """
    生产、创作
    """

    def __init__(self, enterprise=None, product=None, **kwargs):
        Base.__init__(self, enterprise, product, **kwargs)
        pass