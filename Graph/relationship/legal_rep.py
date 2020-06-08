# encoding: utf-8

"""
project = 'Spider'
file_name = 'legal_representative'
author = 'Administrator'
datetime = '2020-03-19 12:45'
IDE = PyCharm
"""
from Graph.relationship import Base


class LegalRep(Base):

    """
    法人代表
    """

    def __init__(self, person=None, enterprise=None, **kwargs):
        Base.__init__(self, person, enterprise, **kwargs)
        pass


