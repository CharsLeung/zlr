# encoding: utf-8

"""
project = 'zlr'
file_name = 'be_in_office'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 15:21'
from = 'office desktop' 
"""
from py2neo import Relationship


class BeInOffice:

    """
    任职于、就职于
    """

    name = 'BE_IN_OFFICE'

    def __init__(self, person, enterprise, **kwargs):
        self.person = person
        self.enterprise = enterprise
        self.properties = kwargs

    def get_relationship(self):
        return Relationship(
            self.person,
            self.name,
            self.enterprise,
            **self.properties
        )