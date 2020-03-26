# encoding: utf-8

"""
project = 'zlr'
file_name = 'justice_graph'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 11:48'
from = 'office desktop' 
"""
from py2neo import Subgraph
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import JusticeCase
from Graph.entity import Enterprise
from Graph.relationship import InvolveCase
from Graph.enterprise_graph import EtpGraph


class JusGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_nodes_from_justice_case(self, justice_case):
        """
        创建法律诉讼相关的实体对象，这些对象可以直接在
        数据库中“法律诉讼”一栏中获取
        1.司法案件
        2.某个司法案件涉及的公司没在数据中，那么应该创建这个公司
        :param justice_case:
        :return:
        """
        nodes = []
        if len(justice_case):
            for jc in justice_case:
                jc_n = jc.get_neo_node(primarykey=jc.primarykey)
                if jc_n is None:
                    self.to_logs('filed initialize justice case Neo node',
                                 'ERROR')
                else:
                    nodes.append(jc_n)
        return nodes

    def create_all_nodes(self):
        """
        创建法律诉讼相关的实体对象，这些对象可以直接在
        数据库中“法律诉讼”一栏中获取
        1.司法案件
        2.某个司法案件涉及的公司没在数据中，那么应该创建这个公司
        :return:
        """
        justices = self.base.aggregate(pipeline=[
            {'$match': {'metaModel': '法律诉讼'}},
            # {'$project': {'_id': 1, 'name': 1}}
        ])
        nodes = []
        eg = EtpGraph()
        for j in justices:
            # 每个公司的法律诉讼下的司法案件肯定跟这个案件有联系
            # 一般情况下司法案件只会涉及到人或法人，法律诉讼这一
            # 板块是依存在企业信息下面的，所有自然跟这个被依存的
            # 企业有联系，我们先不考究这个依存的逻辑正确性，虽然
            # 案件本身里面的信息也能反映出涉案方，后期可能会需要
            etp_n = self.NodeMatcher.match(
                str(Enterprise.label),
                # TODO(leung): 这里要注意，法律诉讼模块中的url确定不了公司
                NAME=j['name']
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                # 不然这个司法案件存在就没有意义
                etp = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': j['name']}
                )
                if etp is not None or len(etp):
                    etp_n = eg.create_nodes_from_enterprise_baseinfo(etp)
                    nodes += etp_n
                    # etp = Enterprise(etp)
                    # etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    # nodes.append(etp_n)

            justice_case_info = j['content']['司法案件']
            jcs = JusticeCase.create_from_dict(justice_case_info)
            jcs_n = self.create_nodes_from_justice_case(jcs)
            nodes += jcs_n
            if len(nodes) > 100:
                tx = self.graph.begin()
                tx.merge(Subgraph(nodes))
                tx.commit()
                nodes.clear()
                return
            pass

    def create_relationship_from_justice_case(self, suspect, justice_case):
        """
        enterprise or person -[involve_case]->justice case
        :param suspect:
        :param justice_case:
        :return:
        """
        rps = []
        for jc in justice_case:
            jc_n = jc.get_neo_node(primarykey=jc.primarykey)
            if jc_n is None:
                self.to_logs('filed initialize justice case Neo node',
                             'ERROR')
            else:
                rps.append(InvolveCase(
                    suspect, jc_n
                ).get_relationship())
        return rps

    def create_all_relationship(self):
        """
        1.enterprise or person -[involve_case]->case
        :return:
        """
        justices = self.base.aggregate(pipeline=[
            {'$match': {'metaModel': '法律诉讼'}},
            # {'$project': {'_id': 1, 'name': 1}}
        ])
        eg = EtpGraph()
        relationships = []
        for j in justices:
            # 每个公司的法律诉讼下的司法案件肯定跟这个案件有联系
            etp_n = self.NodeMatcher.match(
                str(Enterprise.label),
                # TODO(leung): 这里要注意，法律诉讼模块中的url确定不了公司
                NAME=j['name']
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                etp = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': j['name']}
                )
                if etp is not None or len(etp):
                    etp_ = Enterprise(etp)
                    etp_n = etp_.get_neo_node(primarykey=etp_.primarykey)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(etp)
                    pass
            justice_case_info = j['content']['司法案件']
            jcs = JusticeCase.create_from_dict(justice_case_info)
            rps = self.create_relationship_from_justice_case(etp_n, jcs)
            relationships += rps

            if len(relationships) > 100:
                tx = self.graph.begin()
                tx.merge(Subgraph(relationships=relationships))
                tx.commit()
                relationships.clear()
                return
        pass


jg = JusGraph()
jg.create_all_nodes()
jg.create_all_relationship()