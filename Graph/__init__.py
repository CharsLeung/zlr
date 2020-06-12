# encoding: utf-8

"""
project = 'zlr'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-23 11:09'
IDE = PyCharm
"""
from os.path import abspath, dirname

project_dir = dirname(dirname(abspath(__file__)))

workspace = 'D:\graph_data\\'
desktop = 'C:\\Users\Administrator\Desktop\\'


from Graph.base_graph import BaseGraph
from Graph.enterprise_graph import EtpGraph
from Graph.operating_graph import OptGraph
from Graph.operating_risk_graph import OptRiskGraph
from Graph.develop_graph import DvpGraph
from Graph.rights_graph import RightsGraph
from Graph.justice_graph import JusGraph
from Graph.news_graph import NewsGraph


def graphs(name=None):
    gps = {
        'BaseGraph': BaseGraph(),
        'EtpGraph': EtpGraph(),
        'OptGraph': OptGraph(),
        'OptRiskGraph': OptRiskGraph(),
        'DvpGraph': DvpGraph(),
        'RightsGraph': RightsGraph(),
        'JusGraph': JusGraph(),
        'NewsGraph': NewsGraph(),
    }
    if name is not None:
        return gps[name]
    else:
        return gps
