# encoding: utf-8

"""
project = 'zlr'
file_name = 'industry'
author = 'Administrator'
datetime = '2020/3/25 0025 下午 15:07'
from = 'office desktop' 
"""
from py2neo import Subgraph
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import Industry


class IndGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_all_nodes(self, industries):
        """
        创建所有的行业实体，实体对象从外部传进来，因为行业可能
        会作为一个相对独立的研究领域，与数据库中企业基本信息中的
        行业可能不完全匹配
        :return:
        """
        i_nds = []
        for i in industries:
            if isinstance(i, Industry):
                i_n = i.get_neo_node()
                i_nds.append(i_n)
            else:
                raise TypeError('this object is not Industry.')

        if len(i_nds):
            tx = self.graph.begin()
            tx.merge(Subgraph(tx))
            tx.commit()
            i_nds.clear()