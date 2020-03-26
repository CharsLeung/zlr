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
from Graph.entity.address import Address
from Graph.entity.email import Email
from Graph.entity.telephone import Telephone
from Graph.entity.website import Website
from Graph.entity.person import Person
from Graph.entity.holder import ShareHolder
from Graph.entity.justice.case import JusticeCase
from Graph.entity.invested import Invested
from Graph.entity.enterprise import Enterprise
from Graph.entity.industry import Industry
