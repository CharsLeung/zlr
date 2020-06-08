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
from Graph.entity.base import BaseEntity
from Graph.entity.related import Related
from Graph.entity.address import Address
from Graph.entity.mail import Email
from Graph.entity.telephone import Telephone
from Graph.entity.person import Person
from Graph.entity.holder import ShareHolder
from Graph.entity.construction_project import ConstructionProject
from Graph.entity.justice.case import JudicialCase, RegisterCase, FinalCase
from Graph.entity.justice.judgment import Judgment, JudgmentDoc
from Graph.entity.justice.punishment import Punishment
from Graph.entity.justice.involveder import Involveder
from Graph.entity.justice.possession import Possession
from Graph.entity.justice.enforcement import Enforcement, SXEnforcement
from Graph.entity.justice.limitorder import LimitOrder
from Graph.entity.justice.stockfreeze import StockFreeze
from Graph.entity.justice.announce import CourtAnnounce, OpenAnnounce, DeliveryAnnounce
from Graph.entity.invested import Invested
from Graph.entity.branch import Branch
from Graph.entity.head_company import HeadCompany
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
from Graph.entity.operating.position import Position
from Graph.entity.operating.supplier import Supplier
from Graph.entity.operating.tax import TaxCredit
from Graph.entity.operating.debt import Debt
from Graph.entity.operating.banknote import Banknote
from Graph.entity.news.news import News
from Graph.entity.plot import Plot
from Graph.entity.enterprise import Enterprise


def entities(label=None):
    ets = {
        'BaseEntity': BaseEntity(),
        'Related': Related(),
        'Address': Address(),
        'Email': Email(),
        'Telephone': Telephone(),
        'Website': Website(),
        'Person': Person(),
        'ShareHolder': ShareHolder(),
        'ConstructionProject': ConstructionProject(),
        'JudicialCase': JudicialCase(),
        'RegisterCase': RegisterCase(),
        'FinalCase': FinalCase(),
        'Judgment': Judgment(),
        'JudgmentDoc': JudgmentDoc(),
        'Punishment': Punishment(),
        'Involveder': Involveder(),
        'Possession': Possession(),
        'Enforcement': Enforcement(),
        'SXEnforcement': SXEnforcement(),
        'LimitOrder': LimitOrder(),
        'StockFreeze': StockFreeze(),
        'CourtAnnounce': CourtAnnounce(),
        'OpenAnnounce': OpenAnnounce(),
        'DeliveryAnnounce': DeliveryAnnounce(),
        'Invested': Invested(),
        'Branch': Branch(),
        'HeadCompany': HeadCompany(),
        'Enterprise': Enterprise(),
        'Industry': Industry(),
        'Certificate': Certificate(),
        'Patent': Patent(),
        'Trademark': Trademark(),
        'App': App(),
        'WorkCopyRight': WorkCopyRight(),
        'SoftCopyRight': SoftCopyRight(),
        'OfficialAccount': OfficialAccount(),
        'Applets': Applets(),
        'Weibo': Weibo(),
        'Bidding': Bidding(),
        'Check': Check(),
        'RandomCheck': RandomCheck(),
        'Client': Client(),
        'IAE': IAE(),
        'License': License(),
        'Position': Position(),
        'Supplier': Supplier(),
        'TaxCredit': TaxCredit(),
        'News': News(),
        'Plot': Plot(),
        'Debt': Debt(),
        'Banknote': Banknote(),
    }
    if label is None:
        return ets
    else:
        return ets[label]


# 可能是企业、社会组织等法人对象的实体
legal = [
    'Enterprise',
    # 'ShareHolder',
    # 'Involveder',
    'Related',
    # 'Invested',
    # 'Client',
    # 'Supplier',
    # 'Executed',
    # 'SXExecuted',
    # 'Branch',
    # 'HeadCompany'
    # 'Possession',
]

# 可能是自然人对象的实体
person = [
    'Person',
    # 'ShareHolder',
    # 'Involveder',
    'Related',
    # 'Executed',
    # 'SXExecuted',
]
