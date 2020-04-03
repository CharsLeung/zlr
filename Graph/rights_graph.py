# encoding: utf-8

"""
project = zlr
file_name = rights_graph
author = Administrator
datetime = 2020/4/3 0003 上午 10:27
from = office desktop
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import Enterprise
from Graph.exception import SuccessMessage
from Graph.relationship import Have
from Graph.enterprise_graph import EtpGraph


class RightsGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_all_relationship(self):
        """
        1.ruling -[have]->ruling_text
        :return:
        """
        rts = self.base.query(
            sql={'metaModel': '知识产权'},
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp = Enterprise()
        etp_count = rts.count()
        relationships = []
        # prs = Person()
        for r in rts:
            k += 1
            # if k < 43500:
            #     continue
            etp_n = self.NodeMatcher.match(
                etp.label,
                NAME=r['name']  # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': r['name']}
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
                    etp = Enterprise(**{'名称': r['name']})
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    pass

