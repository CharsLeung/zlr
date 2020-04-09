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
from Graph.entity.rights.website import Website
from Graph.entity.person import Person
from Graph.entity.holder import ShareHolder
from Graph.entity.justice.case import JusticeCase
from Graph.entity.justice.ruling import Ruling, RulingText
from Graph.entity.justice.punishment import Punishment
from Graph.entity.justice.involveder import Involveder
from Graph.entity.justice.possession import Possession
from Graph.entity.justice.executed_person import ExecutedPerson
from Graph.entity.invested import Invested
from Graph.entity.enterprise import Enterprise
from Graph.entity.industry import Industry
from Graph.entity.rights.website import Website
from Graph.entity.rights.certificate import Certificate
from Graph.entity.rights.patent import Patent
from Graph.entity.rights.trademark import Trademark
from Graph.entity.rights.app import App
from Graph.entity.rights.copyright import WorkCopyRight, SoftCopyRight
from Graph.entity.rights.newmedia import OfficialAccount, Applets, Weibo
from Graph.entity.operating.bidding import Bidding
from Graph.entity.operating.check import Check, RandomCheck
from Graph.entity.operating.client import Client
from Graph.entity.operating.import_and_export import IAE
from Graph.entity.operating.license import License
from Graph.entity.operating.recruitment import Recruitment
from Graph.entity.operating.supplier import Supplier
from Graph.entity.operating.tax import TaxCredit
from Graph.entity.news.news import News


