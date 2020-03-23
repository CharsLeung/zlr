# encoding: utf-8

"""
project = 'Spider'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-16 18:45'
IDE = PyCharm
"""


ENTITY_CATEGORY = {
    'ENTERPRISE': 1,
}

from py2neo import Node as NeoNode
from Graph.entity.base import QccRequest
from Graph.entity.person import Person
