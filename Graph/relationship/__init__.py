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
from Graph.relationship.justice.involve_case import InvolveCase
from Graph.relationship.take_part_in import TakePartIn
from Graph.relationship.sell import Sell
from Graph.relationship.purchase import Purchase
from Graph.relationship.guaranty import Guaranty
from Graph.relationship.compete import Compete


def relationships(name=None):
    rsp = {
        'Have': Have,
        'BeInOffice': BeInOffice,
        'Located': Located,
        'LegalRep': LegalRep,
        'ShareHolding': ShareHolding,
        'InvolveCase': InvolveCase,
        'TakePartIn': TakePartIn,
        'Sell': Sell,
        'Purchase': Purchase,
        'Guaranty': Guaranty,
        'Compete': Compete,
        # 'Have', Have,
    }
    if name is not None:
        return rsp[name]
    else:
        return rsp
