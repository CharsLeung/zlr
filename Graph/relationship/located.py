# encoding: utf-8

"""
project = 'zlr'
file_name = 'located'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 14:55'
from = 'office desktop' 
"""
from Graph.relationship import Base


class Located(Base):

    """
    坐落于、位于
    """

    def __init__(self, enterprise=None, address=None, **kwargs):
        Base.__init__(self, enterprise, address, **kwargs)
        pass