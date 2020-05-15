# encoding: utf-8

"""
project = 'Spider'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-19 10:16'
IDE = PyCharm
"""
from Graph.relationship.have import Have
from Graph.relationship.be_in_office import BeInOffice
from Graph.relationship.located import Located
from Graph.relationship.legal_representative import LegalRep
from Graph.relationship.share_holding import ShareHolding
from Graph.relationship.invest import Investing
from Graph.relationship.branch_agency import BranchAgency
from Graph.relationship.superior_agency import SuperiorAgency
from Graph.relationship.justice.involve_case import InvolveCase
from Graph.relationship.take_part_in import TakePartIn
from Graph.relationship.sell import SellTo, Sell
from Graph.relationship.purchase import Purchase, Buy
from Graph.relationship.guaranty import Guaranty
from Graph.relationship.compete import Compete
from Graph.relationship.recruit import Recruit
from Graph.relationship.appraise import Appraise


def relationships(name=None):
    rsp = {
        'Have': Have,
        'BeInOffice': BeInOffice,
        'Located': Located,
        'LegalRep': LegalRep,
        'ShareHolding': ShareHolding,
        'Investing': Investing,
        'BranchAgency': BranchAgency,
        'InvolveCase': InvolveCase,
        'TakePartIn': TakePartIn,
        'SellTo': SellTo,
        'Sell': Sell,
        'Purchase': Purchase,
        'Buy': Buy,
        'Guaranty': Guaranty,
        'Compete': Compete,
        'Recruit': Recruit,
        'Appraise': Appraise,
    }
    if name is not None:
        return rsp[name]
    else:
        return rsp
