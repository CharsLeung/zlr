# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = principal
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/2 0002 下午 16:06
@from = office desktop
"""
from Graph.relationship import Base


class Principal(Base):

    """
    负责人
    """

    def __init__(self, person=None, enterprise=None, **kwargs):
        Base.__init__(self, person, enterprise, **kwargs)
        pass