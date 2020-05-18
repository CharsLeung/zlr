# encoding: utf-8

"""
project = zlr
file_name = graph_run
author = Administrator
datetime = 2020/3/27 0027 下午 14:03
from = office desktop
"""
from Graph.enterprise_graph import EtpGraph
from Graph.justice_graph import JusGraph
from Graph.justice_rulingtext_graph import JusRulingTextGraph
from Graph.operating_risk_graph import OptRiskGraph
from Graph.operating_graph import OptGraph
from Graph.news_graph import NewsGraph
from Graph.develop_graph import DvpGraph
from Graph.rights_graph import RightsGraph


def f1():
    eg = EtpGraph()
    # eg.create_index_and_constraint()
    eg.create_all_nodes()
    eg.create_all_relationship()
    if len(eg.logs):
        eg.save_logs('D:\graph_data\graph_run_logs_for_enterprise.csv')
    pass


# f1()


def f2():
    jg = JusGraph()
    # jg.create_all_nodes()
    jg.create_all_relationship()
    if len(jg.logs):
        jg.save_logs('D:\graph_data\graph_run_logs_for_justice.csv')
    pass


# f2()


def f3():
    jtg = JusRulingTextGraph()
    jtg.create_all_relationship()
    if len(jtg.logs):
        jtg.save_logs('D:\graph_data\graph_run_logs_for_justice_text.csv')
    pass


# f3()


def f4():
    org = OptRiskGraph()
    org.create_all_relationship()
    if len(org.logs):
        org.save_logs('D:\graph_data\graph_run_logs_for_org.csv')
    pass


# f4()


def f5():
    og = OptGraph()
    og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_og.csv')
    pass


# f5()


def f6():
    ng = NewsGraph()
    ng.create_all_relationship()
    if len(ng.logs):
        ng.save_logs('D:\graph_data\graph_run_logs_for_news.csv')
    pass


# f6()


def f7():
    dg = DvpGraph()
    dg.create_all_relationship()
    if len(dg.logs):
        dg.save_logs('D:\graph_data\graph_run_logs_for_dg.csv')
    pass


# f7()


def f8():
    dg = RightsGraph()
    dg.create_all_relationship()
    if len(dg.logs):
        dg.save_logs('D:\graph_data\graph_run_logs_for_right.csv')
    pass


# f8()