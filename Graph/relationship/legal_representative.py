# encoding: utf-8

"""
project = 'Spider'
file_name = 'legal_representative'
author = 'Administrator'
datetime = '2020-03-19 12:45'
IDE = PyCharm
"""
from Graph.entity import Person
from py2neo import Relationship


class LegalRep:

    name = 'LEGAL_REPRESENTATIVE'

    def __init__(self, person, enterprise, **kwargs):
        self.person = person
        self.enterprise = enterprise

        pass
