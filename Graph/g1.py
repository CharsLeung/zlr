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


# match (e:Enterprise) where e.NAME=~".*数宜信.*" return e
# MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
# MATCH (e:Enterprise)-[r:HAVE]->(c:Check) delete r
# MATCH (p:Person)-[r]->() where p.URL="https://www.qichacha.com" delete p, r
# MATCH (n:Person) where size((n)-[:LEGAL_REPRESENTATIVE]->())>2 return n
# MATCH p=(e1:Enterprise)-[*..20]-(e2:Enterprise) where e1.NAME='重庆市龙井泡沫塑料有限公司' and e2.NAME='重庆玮兰床垫家具有限公司' RETURN p


graph = Graph('http://localhost:7474', username='neo4j', password='12345')
# bm = BaseModel(tn='qcc_cq_new', location='local')
# p1 = Person(**{'性别': '1245', '姓名': 'A'})
# p2 = Person(**{'性别': '123', 'name': 'A'})
# enterprises = bm.distinct(field='name', sql={'metaModel': '基本信息'})
# enterprises = bm.aggregate(pipeline=[
#     {'$match': {'metaModel': '基本信息'}},
#     # {'$project': {'_id': 1, 'name': 1}}
# ])

# n1 = Person(**{'姓名': 'A', 'URL': 'asd-x', 'name': 'x'}).get_neo_node(primarykey='URL')
# n2 = Person(**{'姓名': 'B', 'URL': 'asd-y', 'name': 'y'}).get_neo_node(primarykey='URL')
# n3 = Person(**{'姓名': 'C', 'URL': 'asd-z', 'name': 'z'}).get_neo_node(primarykey='URL')
# r1 = Relationship(n1, 'lr', n2)
# r2 = Relationship(n2, 'lr', n3)
#
# tx = graph.begin()
# tx.merge(Subgraph([n1, n2]))
# tx.merge(Subgraph(relationships=[r1, r2]))
# tx.commit()

url = 'https://www.qcc.com/firm_e69a6ff5e714ad65d477895bc1df5848.html'
nm = NodeMatcher(graph)
# _ = nm.match('Enterprise').where(
#     '_.URL="{}"'.format()
# ).first()
_ = graph.run('match (n:Enterprise) return n.PAID_UP_CAPITAL_AMOUNT, n.PAID_UP_CAPITAL_UNIT').to_data_frame()
# r = graph.run('match (e:Enterprise)-[:HAVE]-(em:Email) where e.NAME="重庆数宜信信用管理有限公司" return em.EMAIL')
# 1.
# idx = graph.schema.get_indexes('Enterprise')
pass
