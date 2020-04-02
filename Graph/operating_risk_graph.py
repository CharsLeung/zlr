# encoding: utf-8

"""
project = zlr
file_name = operating_risk_graph
author = Administrator
datetime = 2020/4/1 0001 下午 13:58
from = office desktop
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import Punishment, Involveder
from Graph.entity import Enterprise
from Graph.exception import SuccessMessage
from Graph.relationship import InvolveCase, Have
from Graph.enterprise_graph import EtpGraph


class OptRiskGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_relationships_from_punishment(self):
        pass

    def create_all_relationship(self):
        """
        1.enterprise -[have]->punishment
        :return:
        """
        # justices = self.base.aggregate(pipeline=[
        #     {'$match': {'metaModel': '法律诉讼'}},
        #     # {'$project': {'_id': 1, 'name': 1}}
        # ])
        ors = self.base.query(
            sql={'metaModel': '经营风险'},
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = ors.count()
        relationships = []
        # prs = Person()
        etp = Enterprise()
        for j in ors:
            # 每个公司经营风险下列式的东西，肯定就是这家公司的
            k += 1
            # if k < 43500:
            #     continue
            etp_n = self.NodeMatcher.match(
                etp.label,
                NAME=j['name']  # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': j['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那么就简单的把这个公司理解成一个涉案者
                    # 这里就相当于把一个公司当做了一个风险提示的涉及者
                    etp = Involveder(**{'名称': j['name'], '链接': j['url']})
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    pass

            if '行政处罚_工商局' in j['content'].keys():
                punishment_info = j['content']['行政处罚_工商局']
                ps = Punishment.create_from_dict(punishment_info, '工商局')
                for p in ps:
                    relationships.append(
                        Have(
                            etp_n, p.get_neo_node(primarykey=p.primarykey)
                        ).get_relationship()
                    )
                pass

            if '行政处罚_税务局' in j['content'].keys():
                punishment_info = j['content']['行政处罚_税务局']
                ps = Punishment.create_from_dict(punishment_info, '税务局')
                for p in ps:
                    relationships.append(
                        Have(
                            etp_n, p.get_neo_node(primarykey=p.primarykey)
                        ).get_relationship()
                    )
                pass

            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                pass


org = OptRiskGraph()
org.create_all_relationship()