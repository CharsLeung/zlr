# encoding: utf-8

"""
project = 'Spider'
file_name = 't1'
author = 'Administrator'
datetime = '2020-03-18 10:57'
IDE = PyCharm
"""
from data.basemodel import read_json
from entity.baseinfo import BaseInfo
from py2neo import Graph, Node, Relationship

graph = Graph('http://localhost:7474', username='neo4j', password='12345')
# Graph.delete_all()

from utils import File

fs = File.get_all_file('D:\SYR\\20200220\\20200211\\')
fs = fs[:10]
for p in fs:
    js = read_json(p)
    for d in js:
        if d['metaModel'] == '基本信息':
            bi = BaseInfo(d)
            n1 = bi.get_neo_node()
            n2 = bi.get_legal_representative().get_neo_node()
            graph.create(n1)
            graph.create(n2)
            graph.create(Relationship(n2, 'LEGAL_REPRESENTATIVE', n1))

