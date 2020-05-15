# encoding: utf-8

"""
project = 'zlr'
file_name = 'base_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:28'
from = 'office desktop' 
"""
import pandas as pd
import datetime as dt

from Graph.entity import QccRequest
from py2neo import Graph, NodeMatcher, RelationshipMatcher, Subgraph


class BaseGraph:

    def __init__(self, db_uri='http://localhost:7474',
                 username='neo4j', password='12345'
                 ):
        self.graph = Graph(db_uri, username=username, password=password)
        self.NodeMatcher = NodeMatcher(self.graph)
        self.RelationshipMatcher = RelationshipMatcher(self.graph)
        self.logs = []
        self.index_and_constraint_statue = False
        pass

    def to_logs(self, info, tp='LOG', name=''):
        self.logs.append({
            'datetime': dt.datetime.now(),
            'info': info,
            'type': tp,
            'name': name
        })

    def save_logs(self, path):
        logs = pd.DataFrame(self.logs)
        logs.to_csv(path, index=False)
        pass

    def match_node(self, *labels, cypher=None):
        """
        py2neo的match不支持多label的查询，cypher也
        不支持，但同一条件去查询满足的多个label是经常
        用到的，找到一个就结束
        :param cypher:
        :param labels:
        :return:
        """
        ns = None
        # _ = graph.run('match (n:Enterprise{URL:"%s"}) return n limit 1' % url)
        for label in labels:
            n = self.NodeMatcher.match(label).where(
                cypher).first()
            if n is not None:
                return n
        return ns
        pass

    def graph_merge_nodes(self, nodes=None, toleration=10):
        """
        把一个子图合并到数据库中去，因为我们一般都是批量插入节点或者关系，
        但有时候在这批量数据中可能有一些异常的节点，会影响整批数据的插入，
        因此，在一般情况下，将这些少数的坏节点抛弃掉，将大部分正常的节点
        继续写入数据库。
        :param toleration: 容忍失败的最大节点数
        :param nodes:
        :return:
        """
        try:
            if nodes is not None:
                tx = self.graph.begin()
                tx.merge(Subgraph(nodes=nodes))
                tx.commit()
        except Exception as e:
            self.to_logs('commit subgraph to database raise ({})'.format(e),
                         'EXCEPTION')
            l = len(nodes)
            if l < toleration:
                return
            bk = l // 10 + 1  # 每块的数量
            for i in range(0, 11):
                nds = nodes[i * bk:(i + 1) * bk]
                try:
                    if len(nds):
                        tx = self.graph.begin()
                        tx.merge(Subgraph(nodes=nds))
                        tx.commit()
                except Exception as e:
                    self.to_logs('commit subgraph to database raise ({}) on '
                                 '[{}:{}]'.format(e, i * bk, (i + 1) * bk),
                                 'EXCEPTION')
                    self.graph_merge_nodes(nds, toleration)

    def graph_merge_relationships(self, relationships=None,
                                  toleration=10, **kwargs):
        """
        把一个子图合并到数据库中去，因为我们一般都是批量插入节点或者关系，
        但有时候在这批量数据中可能有一些异常的节点，会影响整批数据的插入，
        因此，在一般情况下，将这些少数的坏节点抛弃掉，将大部分正常的节点
        继续写入数据库。
        :param toleration: 容忍失败的最大节点数
        :param relationships:
        :return:
        """
        try:
            if relationships is not None:
                tx = self.graph.begin()
                tx.merge(Subgraph(relationships=relationships))
                tx.commit()
        except Exception as e:
            print(e)
            self.to_logs('commit subgraph to database raise ({})'.format(e),
                         'EXCEPTION', name=str(kwargs))
            l = len(relationships)
            if l < toleration:
                return
            bk = l // 10 + 1  # 每块的数量
            for i in range(0, 11):
                rps = relationships[i * bk:(i + 1) * bk]
                try:
                    if len(rps):
                        tx = self.graph.begin()
                        tx.merge(Subgraph(relationships=rps))
                        tx.commit()
                except Exception as e:
                    self.to_logs('commit subgraph to database raise ({}) on '
                                 '[{}:{}]'.format(e, i * bk, (i + 1) * bk),
                                 'EXCEPTION', name=str(kwargs))
                    self.graph_merge_relationships(rps, toleration, **kwargs)

    def add_index_and_constraint(self, index=None, constraint=None):
        """
        为涉及到的实体创建唯一性约束跟索引，唯一键自动带有索引
        不比再单独创建索引
        :return:
        """
        self.index_and_constraint_statue = True
        labels = list(self.graph.schema.node_labels)
        if constraint is not None:
            for l, cst in zip(constraint.keys(), constraint.values()):
                if l in labels:
                    cst0 = self.graph.schema.get_uniqueness_constraints(l)
                    for c in cst:
                        if c not in cst0:
                            self.graph.schema.create_uniqueness_constraint(l, c)
                            print('success to create constraint for '
                                  '{}({})'.format(l, c))
                else:
                    print('failed create constraint for {}, '
                          'this label not in db.'.format(l))
                    self.index_and_constraint_statue = False
            pass
        if index is not None:
            for l, idx in zip(index.keys(), index.values()):
                if l in labels:
                    idx0 = self.graph.schema.get_indexes(l)
                    for i in idx:
                        f = True
                        for i0 in idx0:
                            if i == i0:
                                f = False
                        if f:
                            self.graph.schema.create_index(l, *i)
                            print('success to create index for '
                                  '{}({})'.format(l, ','.join(i)))
                else:
                    print('failed create index for label({}){}, '
                          'this label not in db.'.format(l, idx))
                    self.index_and_constraint_statue = False
        pass

    @staticmethod
    def get_format_amount(k, v):
        return QccRequest.get_format_amount(k, v)

    @staticmethod
    def get_format_dict(data):
        _ = QccRequest.get_format_dict(data)
        return _ if isinstance(_, list) else [_]

    def get_neo_node(self, node):
        if isinstance(node, list):
            nodes = []
            for n_ in node:
                n = n_.get_neo_node(primarykey=n_.primarykey)
                if n is None:
                    self.to_logs('filed initialize {} Neo node'.format(
                        n_.label), 'ERROR')
                else:
                    nodes.append(n)
            return nodes
        else:
            n = node.get_neo_node(primarykey=node.primarykey)
            if n is None or n.__primarykey__ is None:
                print('--')
                self.to_logs('filed initialize {} Neo node'.format(
                    node.label), 'ERROR')
            return n
