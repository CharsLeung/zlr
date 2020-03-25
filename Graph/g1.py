# encoding: utf-8

"""
project = 'zlr'
file_name = 'g1'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 15:30'
from = 'office desktop' 
"""
from py2neo import Graph, NodeMatcher, Subgraph, Node, Relationship
from Calf.data import BaseModel
from Graph.entity import Person, Enterprise
from Graph.relationship import *


# MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
# MATCH (n:Person) where size((n)-[:LEGAL_REPRESENTATIVE]->())>2 return n


graph = Graph('http://localhost:7474', username='neo4j', password='12345')
# bm = BaseModel(tn='qcc_cq_new', location='local')
# p1 = Person(**{'性别': '1245', '姓名': 'A'})
# p2 = Person(**{'性别': '123', 'name': 'A'})
# enterprises = bm.distinct(field='name', sql={'metaModel': '基本信息'})
# enterprises = bm.aggregate(pipeline=[
#     {'$match': {'metaModel': '基本信息'}},
#     # {'$project': {'_id': 1, 'name': 1}}
# ])

n1 = Person(**{'姓名': 'A', 'URL': 'asd-x', 'name': 'x'}).get_neo_node(primarykey='URL')
n2 = Person(**{'姓名': 'B', 'URL': 'asd-y', 'name': 'y'}).get_neo_node(primarykey='URL')
# n3 = Person(**{'姓名': 'C', 'URL': 'asd-z', 'name': 'z'}).get_neo_node(primarykey='URL')
# r1 = Relationship(n1, 'lr', n2)
# r2 = Relationship(n2, 'lr', n3)
#
# tx = graph.begin()
# tx.merge(Subgraph([n1, n2]))
# tx.merge(Subgraph(relationships=[r1, r2]))
# tx.commit()

# nm = NodeMatcher(graph)



pass
