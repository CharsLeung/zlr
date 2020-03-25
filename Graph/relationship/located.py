# encoding: utf-8

"""
project = 'zlr'
file_name = 'located'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 14:55'
from = 'office desktop' 
"""
from py2neo import Relationship


class Located:

    name = 'LOCATED'

    def __init__(self, enterprise, address, **kwargs):
        self.enterprise = enterprise
        self.address = address
        self.properties = kwargs
        pass

    def get_relationship(self):
        return Relationship(
            self.enterprise,
            self.name,
            self.address,
            **self.properties
        )
