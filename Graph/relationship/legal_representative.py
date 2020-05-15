# encoding: utf-8

"""
project = 'Spider'
file_name = 'legal_representative'
author = 'Administrator'
datetime = '2020-03-19 12:45'
IDE = PyCharm
"""
from py2neo import Relationship


class LegalRep:

    """
    法人代表
    """

    name = 'LEGAL'

    def __init__(self, person, enterprise, **kwargs):
        self.person = person
        self.enterprise = enterprise
        self.prop = kwargs
        pass

    def get_relationship(self):
        return Relationship(
            self.person,
            self.name,
            self.enterprise,
            **self.prop
        )


