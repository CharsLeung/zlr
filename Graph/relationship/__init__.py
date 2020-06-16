# encoding: utf-8

"""
project = 'Spider'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-19 10:16'
IDE = PyCharm
"""
from Graph.relationship.base import Base
from Graph.relationship.have import Have
from Graph.relationship.belong import Belong
from Graph.relationship.be_in_office import BeInOffice
from Graph.relationship.located import Located
from Graph.relationship.legal_rep import LegalRep
from Graph.relationship.principal import Principal
from Graph.relationship.share_holding import Share
from Graph.relationship.invest import Investing
from Graph.relationship.branch_agency import BranchAgency
from Graph.relationship.superior_agency import SuperiorAgency
from Graph.relationship.justice.involve_case import InvolveCase
from Graph.relationship.take_part_in import TakePartIn
from Graph.relationship.sell import SellTo, Sell
from Graph.relationship.buy import BuyFrom, Buy
from Graph.relationship.guaranty import Guaranty
from Graph.relationship.compete import Compete
from Graph.relationship.recruit import Recruit
from Graph.relationship.appraise import Appraise
from Graph.relationship.apply_bankrupt import ApplyBankrupt
from Graph.relationship.produce import Produce


def relationships(name=None):
    # _rsp_ = [
    #     BeInOffice, Located, LegalRep, Principal, Share, Investing,
    #     BranchAgency, SuperiorAgency, InvolveCase, TakePartIn,
    #     SellTo, Sell, Purchase, Buy, Guaranty, Compete, Recruit, Appraise,
    # ]
    # rsp = {}
    # for _ in _rsp_:
    #     __ = _({}, {})
    #     print('"{}": {},'.format(__.label, str(__.__class__.__name__)))
    rsp = {
        "HAVE": Have(),
        'BELONG': Belong(),
        "BE_IN_OFFICE": BeInOffice(),
        "LOCATED": Located(),
        "LEGAL_REP": LegalRep(),
        "PRINCIPAL": Principal(),
        "SHARE": Share(),
        "INVESTING": Investing(),
        "BRANCH_AGENCY": BranchAgency(),
        "SUPERIOR_AGENCY": SuperiorAgency(),
        "INVOLVE_CASE": InvolveCase(),
        "TAKE_PART_IN": TakePartIn(),
        "SELL_TO": SellTo(),
        "SELL": Sell(),
        "BUY_FROM": BuyFrom(),
        "BUY": Buy(),
        "GUARANTY": Guaranty(),
        "COMPETE": Compete(),
        "RECRUIT": Recruit(),
        "APPRAISE": Appraise(),
        "APPLY_BANKRUPT": ApplyBankrupt(),
        'PRODUCE': Produce()
    }
    if name is not None:
        return rsp[name]
    else:
        return rsp


# relationships()