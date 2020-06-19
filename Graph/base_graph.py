# encoding: utf-8

"""
project = 'zlr'
file_name = 'base_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:28'
from = 'office desktop' 
"""
import os
import pandas as pd
import datetime as dt

from Calf.threading import Thread
from Graph.entity import BaseEntity
from Graph.logger import logger
from py2neo import Graph, NodeMatcher, RelationshipMatcher, Subgraph


class BaseGraph:

    def __init__(self, db_uri='http://localhost:7474',
                 username='neo4j', password='12345',
                 log_save_path=None, **kwargs):
        self.graph = Graph(db_uri, username=username, password=password)
        self.NodeMatcher = NodeMatcher(self.graph)
        self.RelationshipMatcher = RelationshipMatcher(self.graph)
        self.logger = logger(self.label, save_path=log_save_path)
        self.logs = []
        self.index_and_constraint_statue = False
        pass

    @property
    def label(self):
        return str(self.__class__.__name__)

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
        # for label in labels:
        #     n = self.NodeMatcher.match(label).where(
        #         cypher).first()
        #     if n is not None:
        #         return n
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
            self.logger.debug('commit subgraph to database '
                              'raise ({})'.format(e))
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
                    self.logger.debug('commit subgraph to database raise ({}) on '
                                      '[{}:{}]'.format(e, i * bk, (i + 1) * bk))
                    self.graph_merge_nodes(nds, toleration)

    def merge_relationships(self, relationships=None,
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
            self.logger.debug('commit subgraph to database raise ({})'.format(e))
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
                    self.logger.debug('commit subgraph to database raise ({}) on '
                                      '[{}:{}]'.format(e, i * bk, (i + 1) * bk))
                    self.merge_relationships(rps, toleration, **kwargs)
            pass

    def graph_merge_relationships(self,
                                  relationships=None,
                                  toleration=10,
                                  use_multiprocessing=False,
                                  timeout=None,
                                  **kwargs):
        if use_multiprocessing:
            th = Thread(self.merge_relationships,
                        **dict(relationships=relationships,
                               toleration=toleration,
                               **kwargs
                               )
                        )
            th.start()
            # th.join(timeout)
            # return th.get_result()
        else:
            self.merge_relationships(
                relationships, toleration, **kwargs
            )
            # return rlt

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
                            self.logger.info('success to create constraint for '
                                             '{}({})'.format(l, c))
                        # self.graph.schema.create_uniqueness_constraint(l, c)
                else:
                    self.logger.info('failed create constraint for {}, '
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
                            self.logger.info('success to create index for '
                                             '{}({})'.format(l, ','.join(i)))
                else:
                    self.logger.info('failed create index for label({}){}, '
                                     'this label not in db.'.format(l, idx))
                    self.index_and_constraint_statue = False
        pass

    @staticmethod
    def get_format_amount(k, v):
        return BaseEntity.get_format_amount(k, v)

    @staticmethod
    def get_format_dict(data):
        _ = BaseEntity.get_format_dict(data)
        return _ if isinstance(_, list) else [_]

    def get_neo_node(self, node):
        if isinstance(node, list):
            nodes = []
            for n_ in node:
                n = n_.get_neo_node(primarykey=n_.primarykey)
                if n is None:
                    self.logger.debug('filed initialize {}'.format(n_))
                    pass
                else:
                    nodes.append(n)
            return nodes
        else:
            n = node.get_neo_node(primarykey=node.primarykey)
            if n is None or n.__primarykey__ is None:
                self.logger.debug('filed initialize {}'.format(node))
                pass
            return n

    def save_graph(self, folder, nodes, rps, mode='w'):
        from Calf.utils import File
        from Graph.entity import entities
        from Graph.relationship import relationships
        # nodes, rps = eg.get_all_nodes_and_relationships()
        nodes_save_folder = os.path.join(folder, self.label, 'nodes')
        File.check_file(nodes_save_folder)
        self.logger.info('save graph data(mode={}):'.format(mode))
        self.logger.info(' nodes:')
        nc = 0
        for k, _nds_ in zip(nodes.keys(), nodes.values()):
            ne = entities(k)
            _nds_ = ne.to_pandas(_nds_, )
            _nds_ = ne.getImportCSV(_nds_)
            count = ne.to_csv(_nds_, nodes_save_folder, True, mode)
            self.logger.info('     {} {}'.format(count, k))
            nc += count
            pass
        rps_save_folder = os.path.join(folder, self.label, 'relationships')
        File.check_file(rps_save_folder)
        self.logger.info(' relationships:')
        rc = 0
        for k, _rps_ in zip(rps.keys(), rps.values()):
            rel = relationships(k)
            _rps_ = rel.to_pandas(_rps_, )
            _rps_ = rel.getImportCSV(_rps_)
            count = rel.to_csv(_rps_, rps_save_folder, True, mode)
            self.logger.info('     {} {}'.format(count, k))
            rc += count
            pass
        return nc, rc
