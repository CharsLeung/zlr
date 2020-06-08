# encoding: utf-8

"""
project = 'zlr'
file_name = 'be_in_office'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 15:21'
from = 'office desktop' 
"""
from Graph.relationship import Base


class BeInOffice(Base):

    """
    任职于、就职于
    """

    def __init__(self, person=None, enterprise=None, **kwargs):
        Base.__init__(self, person, enterprise, **kwargs)
        pass