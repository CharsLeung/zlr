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

# nm = NodeMatcher(graph)
ds = [
    "/firm_c25afa3e6430f8d0349de0e99a3bead0",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_p4491f80a6e03c1f787eb45c49018f77",
    "/firm_dd51e1dfc0e9eaaafddd9eb305b4302a",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_p4491f80a6e03c1f787eb45c49018f77",
    "/firm_d8e6a99720a839656d4d86a6d9db65b1",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr181fe7ab572cf53629ad792333d5df",
    "/firm_9880c1b7d6fce46792ca1b0b7324332e",
    "/pl_p3ef1aba7ccbe66ee2ad2d906206a0c2",
    "/pl_p3ef1aba7ccbe66ee2ad2d906206a0c2",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/firm_c0ab32bec9b6e9e718bc743acd006737",
    "/pl_pc1f3b8324d2a1b1b702791007bbc0a9",
    "/pl_pc1f3b8324d2a1b1b702791007bbc0a9",
    "/pl_p0450f5ba42578d971727f66a3f7dfd0",
    "/firm_dd51e1dfc0e9eaaafddd9eb305b4302a",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_p4491f80a6e03c1f787eb45c49018f77",
    "/firm_b12171caddbd0b54465fb96e2968fa1c",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_p4491f80a6e03c1f787eb45c49018f77",
    "/firm_6eb2a45f01862a025f66973fffbe710d",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pf6518627578dd71e7fd72e42758e388",
    "/pl_pcbf9071137b0b5b5dea068549a2e929",
    "/firm_39551ee3e7455778247d46a88201648a",
    "/pl_p3ef1aba7ccbe66ee2ad2d906206a0c2",
    "/pl_pr4ed3d6634b8eafcbb75e700ed931a7",
    "/pl_p3ef1aba7ccbe66ee2ad2d906206a0c2",
    "/pl_p4491f80a6e03c1f787eb45c49018f77",
    "/firm_792b994be92485bd4826e5f5a48a1e55",
    "/pl_p31094ae5e54e8afb8ac3e8da4c9150f",
    "/pl_p31094ae5e54e8afb8ac3e8da4c9150f",
    "/pl_p3635c484b4a2284a7f9f5539e478b40",
    "/pl_pe0b65f62451d5e6ba7484d89760ce3e",
    "/pl_p4f73f42033ed992720ba4a9e2749202",
    "/pl_p381e36f982ab6b8b26fa05283209b00",
    "/pl_p34db24d2c01da8ca9ab81aa14c5a17e",
    "/pl_pc1f3b8324d2a1b1b702791007bbc0a9",
    "/firm_2a6b78dcec94328df3bb767e28de5c69",
    "/pl_p87a38443f3770db0b7b2ebeaf72f4a2",
    "/pl_p87a38443f3770db0b7b2ebeaf72f4a2",
    "/pl_p7997544c28c9722b98a434d451165b3",
    "/firm_a10efefc2e55177b1c8f0c3eab0b0296",
    "/pl_p0d5da2d552c32b5a885fc7eea80557f",
    "/pl_p0d5da2d552c32b5a885fc7eea80557f",
    "/pl_p2e2b38c0ed1190027ffa291b6f92410",
    "/pl_prede75249879f16906b6a1a5fb734d1",
    "/pl_pdb068385ed30e71cc602fb58c12af1c",
    "/pl_p2329dae02281456b7e29f4fd48d5100",
    "/pl_p89f39651da46af61201ed24552c59e1",
    "/firm_61c44dd81e4549513d7a096a52f879d7",
    "/pl_p44c11551dc3b1b68855bece0a058d5e",
    "/pl_p44c11551dc3b1b68855bece0a058d5e",
    "/pl_p59f3d7985808d77924f85c2fbc4f349",
    "/firm_5a8f00136f02eab2c731805d8f28b27c",
    "/pl_p372b6834d319bae32a923b616bcb2fd",
    "/pl_p8219f0f109419d1bc8fbcd8bd4c7aae",
    "/pl_p372b6834d319bae32a923b616bcb2fd",

]
for d in ds:
    try:
        graph.run('MATCH (n:Enterprise) OPTIONAL '
                  'MATCH (n)-[r]-() where n.URL=~".*{}.*" '
                  'DELETE n,r'.format(d))
        print(d)
    except Exception as e:
        print(e)
# 1.

pass
