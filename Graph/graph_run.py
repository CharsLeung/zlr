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


eg = EtpGraph()
# eg.create_all_nodes()
eg.create_all_relationship()
if len(eg.logs):
    eg.save_logs('D:\graph_data\graph_run_logs_for_enterprise.csv')

# jg = JusGraph()
# jg.create_all_nodes()
# jg.create_all_relationship()