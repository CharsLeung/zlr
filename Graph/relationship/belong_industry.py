# encoding: utf-8

"""
project = 'zlr'
file_name = 'belong_industry'
author = 'Administrator'
datetime = '2020/3/25 0025 下午 15:00'
from = 'office desktop' 
"""
from py2neo import Relationship


class BelongIndustry:
    name = 'BELONG_INDUSTRY'

    def __init__(self, enterprise, industry, **kwargs):
        self.enterprise = enterprise
        self.industry = industry
        self.properties = kwargs

    def get_relationship(self):
        return Relationship(
            self.enterprise,
            self.name,
            self.industry,
            **self.properties
        )