# encoding: utf-8

"""
project = 'zlr'
file_name = 'belong_industry'
author = 'Administrator'
datetime = '2020/3/25 0025 下午 15:00'
from = 'office desktop' 
"""
from Graph.relationship import Base


class BelongIndustry(Base):

    def __init__(self, enterprise, industry, **kwargs):
        Base.__init__(self, enterprise, industry, **kwargs)
        pass