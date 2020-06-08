# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = news_graph
author = Administrator
datetime = 2020/4/8 0008 下午 15:36
from = office desktop
"""
import re
import time
import datetime as dt

from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo, SuccessMessage
from Graph.entity import entities, legal
from Graph.entity import Enterprise, News, Related
from Graph.relationship import Have
from Graph.enterprise_graph import EtpGraph


class NewsGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(
            tn='qcc.1.1',
            # location='gcxy',
            # dbname='data'
        )
        pass

    def create_index_and_constraint(self):
        """
        为涉及到的实体创建唯一性约束跟索引，唯一键自动带有索引
        不比再单独创建索引
        :return:
        """
        # TODO(leung): 要随时确保label的准确性
        used_entity = [
            'News',
        ]
        constraint = {}
        index = {}
        for l in used_entity:
            constraint[l] = [entities(l).primarykey]
            idx = entities(l).index
            if len(idx):
                index[l] = idx
        self.add_index_and_constraint(index, constraint)
        pass

    def create_all_relationship(self):
        """
        1.enterprise -[have or x]->x
        :return:
        """
        ops = self.base.query(
            sql={'metaModel': '公司新闻'},
            # limit=10,
            skip=2020,
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = ops.count()
        relationships = []
        # etp = Enterprise()
        s_t = time.time()
        for o in ops:
            k += 1
            # if k < 43500:
            #     continue
            # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            etp_n = self.match_node(
                *legal,
                cypher='_.NAME = "{}"'.format(o['name'])
            )
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': o['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = self.get_neo_node(etp)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那就创建一个信息不全的公司
                    etp = Related(**{'名称': o['name'], '链接': o['url']})
                    # etp['NAME'] = o['name']
                    # etp['URL'] = o['url']
                    etp_n = self.get_neo_node(etp)
                    if etp_n is None:
                        continue
                    pass

            if '新闻舆情' in o['content'].keys():
                data = self.get_format_dict(o['content']['新闻舆情'])
                ns = News.create_from_dict(data)
                for n in ns:
                    n_ = n.pop('news')
                    n_n = self.get_neo_node(n_)
                    if n_n is not None:
                        relationships.append(
                            Have(etp_n, n_n, **n).get_relationship()
                        )
                pass
            if len(relationships) > 1000:
                i += 1
                sp = int(time.time() - s_t)
                s_t = time.time()
                self.graph_merge_relationships(relationships)
                if not self.index_and_constraint_statue:
                    self.create_index_and_constraint()
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise and spend {} '
                                     'seconds,and merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, sp, len(relationships)
                )))
                relationships.clear()
                # return
        if len(relationships):
            i += 1
            self.graph_merge_relationships(relationships)
            if not self.index_and_constraint_statue:
                self.create_index_and_constraint()
            print(SuccessMessage('{}:success merge relationships to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} relationships.'.format(
                dt.datetime.now(), i, k, etp_count, len(relationships)
            )))
            relationships.clear()
            pass

    def get_all_nodes_and_relationships_from_enterprise(self, etp):
        etp_n = Enterprise(URL=etp['url'], NAME=etp['name'])
        etp_n = self.get_neo_node(etp_n)
        if etp_n is None:
            return [], []
        nodes, relationships = [], []
        nodes.append(etp_n)

        if '新闻舆情' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['新闻舆情'])
            ns = News.create_from_dict(data)
            for n in ns:
                n_ = n.pop('news')
                n_n = self.get_neo_node(n_)
                if n_n is not None:
                    relationships.append(
                        Have(etp_n, n_n, **n).get_relationship()
                    )
            pass
        return nodes, relationships

    def get_all_nodes_and_relationships(self):
        enterprises = self.base.query(
            sql={
                'metaModel': '公司新闻',
                # 'name': '重庆轩烽建材有限公司'
            },
            limit=1000,
            # skip=2000,
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        nodes, relationships = {}, {}
        unique_code_pattern = re.compile('(?<=unique=)\w{32}')

        def getUniqueCode(url):
            _uc_ = re.search(unique_code_pattern, url)
            if _uc_ is not None:
                return _uc_.group(0)
            else:
                return None

        for ep in enterprises:
            i += 1
            uc = getUniqueCode(ep['url'])
            if uc is None:
                continue
            ep['url'] = '/firm_' + uc + '.html'
            nds, rps = self.get_all_nodes_and_relationships_from_enterprise(ep)
            for _nds_ in nds:
                if _nds_ is None:
                    continue
                # _nds_ = _nds_.to_dict()
                label = list(_nds_.labels)[0]
                _nds_ = dict(label=label, **_nds_)
                if _nds_['label'] in nodes.keys():
                    nodes[_nds_['label']].append(_nds_)
                else:
                    nodes[_nds_['label']] = [_nds_]
                pass
            for _rps_ in rps:
                _rps_ = _rps_.to_dict()
                if _rps_['label'] in relationships.keys():
                    relationships[_rps_['label']].append(_rps_)
                else:
                    relationships[_rps_['label']] = [_rps_]
                pass
            if i % 1000 == 0:
                j += 1
                print(SuccessMessage(
                    '{}:success merge nodes to database '
                    'round {} and deal {}/{} enterprise'
                    ''.format(dt.datetime.now(), i, j, etp_count)
                ))
            pass
        return nodes, relationships
