# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = news_graph
author = Administrator
datetime = 2020/4/8 0008 下午 15:36
from = office desktop
"""
import datetime as dt

from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo, SuccessMessage
from Graph.entity import Enterprise, News
from Graph.relationship import Have
from Graph.enterprise_graph import EtpGraph


class NewsGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_index_and_constraint(self):
        """
        为涉及到的实体创建唯一性约束跟索引，唯一键自动带有索引
        不比再单独创建索引
        :return:
        """
        # TODO(leung): 要随时确保label的准确性
        constraint = {
            'News': [News.primarykey],
            # 'Possession': [Possession.primarykey],
            # 'Involveder': ['HASH_ID'],
        }
        index = {
            # 'Enterprise': [('NAME',)]
        }
        self.add_index_and_constraint(index, constraint)
        pass

    def create_nodes_from_news(self, news):
        """
        创建公司新闻下的新闻舆情节点对象，news参数是
        news类的实例。
        1.新闻舆情
        :param news:
        :return:
        """
        nodes = []
        if len(news):
            for _ in news:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize news'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_all_relationship(self):
        """
        1.enterprise -[have or x]->x
        :return:
        """
        ops = self.base.query(
            sql={'metaModel': '经营状况'},
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = ops.count()
        relationships = []
        etp = Enterprise()
        for o in ops:
            k += 1
            # if k < 43500:
            #     continue
            etp_n = self.NodeMatcher.match(
                etp.label,
                NAME=o['name']  # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': o['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那就创建一个信息不全的公司
                    etp = Enterprise(**{'名称': o['name']})
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    pass

            if '新闻舆情' in o['content'].keys():
                n_info = o['content']['新闻舆情']
                ns = News.create_from_dict(n_info)
                ns_n = self.create_nodes_from_news(ns)
                for n_n in ns_n:
                    relationships.append(
                        Have(etp_n, n_n).get_relationship()
                    )
                pass
            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                if i == 1:
                    # 第一轮创建索引
                    self.create_index_and_constraint()
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                return
        if len(relationships):
            i += 1
            self.graph_merge_relationships(relationships)
            print(SuccessMessage('{}:success merge relationships to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} relationships.'.format(
                dt.datetime.now(), i, k, etp_count, len(relationships)
            )))
            relationships.clear()
            pass
