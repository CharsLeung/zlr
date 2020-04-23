# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = operating_graph
author = Administrator
datetime = 2020/4/8 0008 上午 9:33
from = office desktop
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo, SuccessMessage
from Graph.entity import Enterprise, License, Bidding
from Graph.entity import Check, RandomCheck, TaxCredit
from Graph.entity import IAE, Recruitment, Client, Supplier
from Graph.relationship import Have, TakePartIn
from Graph.relationship import Sell, Purchase
from Graph.enterprise_graph import EtpGraph


class OptGraph(BaseGraph):

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
            'License': [License.primarykey],
            'Bidding': [Bidding.primarykey],
            'Check': [Check.primarykey],
            'RandomCheck': [RandomCheck.primarykey],
            'TaxCredit': [TaxCredit.primarykey],
            'IAE': [IAE.primarykey],
            'Recruitment': [Recruitment.primarykey],
            'Client': [Client.primarykey],
            'Supplier': [Supplier.primarykey],
            # 'Recruitment': [Recruitment.primarykey],
        }
        index = {
            # 'Enterprise': [('NAME',)]
        }
        self.add_index_and_constraint(index, constraint)
        pass

    def create_nodes_from_license(self, lcs):
        """
        创建经营状况下的行政许可节点对象，lcs参数是
        license类的实例。
        1.行政许可
        :param lcs:
        :return:
        """
        nodes = []
        if len(lcs):
            for _ in lcs:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize license'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_bidding(self, bidding):
        """
        创建经营状况下的招投标节点对象，bidding参数是
        bidding类的实例。
        1.招投标
        :param bidding:
        :return:
        """
        nodes = []
        if len(bidding):
            for _ in bidding:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize bidding'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_check(self, check):
        """
        创建经营状况下的检查节点对象，check参数是
        check类的实例。
        1.抽查检查、双随机抽查
        :param check:
        :return:
        """
        nodes = []
        if len(check):
            for _ in check:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize check'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_tax(self, tax):
        """
        创建经营状况下的税务信用节点对象，tax参数是
        TaxCredit类的实例。
        1.税务信用
        :param tax:
        :return:
        """
        nodes = []
        if len(tax):
            for _ in tax:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize tax-credit'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_iae(self, iae):
        """
        创建经营状况下的进出口信用节点对象，iae参数是
        IAE类的实例。
        1.进出口信用
        :param iae:
        :return:
        """
        nodes = []
        if len(iae):
            for _ in iae:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize iae'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_recruitment(self, recruitment):
        """
        创建经营状况下的招聘节点对象，recruitment参数是
        recruitment类的实例。
        1.招聘
        :param recruitment:
        :return:
        """
        nodes = []
        if len(recruitment):
            for _ in recruitment:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize recruitment'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_client(self, client):
        """
        创建经营状况下的客户节点对象，client参数是
        client类的实例。
        1.客户
        :param client:
        :return:
        """
        nodes = []
        if len(client):
            for _ in client:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize client'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_supplier(self, supplier):
        """
        创建经营状况下的供应商节点对象，supplier参数是
        supplier类的实例。
        1.供应商
        :param supplier:
        :return:
        """
        nodes = []
        if len(supplier):
            for _ in supplier:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize supplier'
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
            sql={
                'metaModel': '经营状况',
                # 'name': '重庆秋之妍园林艺术发展有限公司'
            },
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = ops.count()
        relationships = []
        etp = Enterprise()
        for o in ops:
            k += 1
            # if k < 108990:
            #     continue
            # etp_n = self.NodeMatcher.match(
            #     etp.label,
            #     NAME=o['name']  # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            # ).first()
            etp_n = self.match_node(
                'Enterprise', 'ShareHolder', 'Involveder',
                'Invested', 'Client', 'Supplier',
                cypher='_.NAME = "{}"'.format(o['name'])
            )
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
                    etp = Enterprise({'name': o['name'], 'metaModel': '基本信息'})
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    pass

            if '行政许可_工商局' in o['content'].keys():
                l_info = o['content']['行政许可_工商局']
                ls = License.create_from_dict(l_info, '工商局')
                ls_n = self.create_nodes_from_license(ls)
                for l_n in ls_n:
                    relationships.append(
                        Have(etp_n, l_n).get_relationship()
                    )
                pass
            if '行政许可_信用中国' in o['content'].keys():
                l_info = o['content']['行政许可_信用中国']
                ls = License.create_from_dict(l_info, '信用中国')
                ls_n = self.create_nodes_from_license(ls)
                for l_n in ls_n:
                    relationships.append(
                        Have(etp_n, l_n).get_relationship()
                    )
                pass
            if '招投标信息' in o['content'].keys():
                # 公示的招投标信息一般都是结果，一般情况下是找不到
                # 共同投标的单位，除非是共同中标
                # b_info = o['content']['招投标信息']
                # bs = Bidding.create_from_dict(b_info)
                # bs_n = self.create_nodes_from_bidding(bs)
                # for b_n in bs_n:
                #     # TODO(leung):项目分类用作了招投标结果
                #     relationships.append(
                #         TakePartIn(
                #             etp_n, b_n, **{'RESULT': b_n['TYPE']}
                #         ).get_relationship()
                #     )
                pass
            if '抽查检查' in o['content'].keys():
                c_info = o['content']['抽查检查']
                cs = Check.create_from_dict(c_info)
                cs_n = self.create_nodes_from_check(cs)
                for c_n in cs_n:
                    relationships.append(
                        Have(
                            etp_n, c_n, **{'RESULT': c_n['RESULT']}
                        ).get_relationship()
                    )
                pass
            if '双随机抽查' in o['content'].keys():
                rc_info = o['content']['双随机抽查']
                rcs = RandomCheck.create_from_dict(rc_info)
                rcs_n = self.create_nodes_from_check(rcs)
                for rc_n in rcs_n:
                    # TODO(leung):随机抽查没有结果
                    relationships.append(
                        Have(
                            etp_n, rc_n
                        ).get_relationship()
                    )
                pass
            if '税务信用' in o['content'].keys():
                # t_info = o['content']['税务信用']
                # ts = TaxCredit.create_from_dict(t_info)
                # ts_n = self.create_nodes_from_tax(ts)
                # for t_n in ts_n:
                #     # TODO(leung):纳税信用等级作为税务信用评级结果
                #     relationships.append(
                #         Have(
                #             etp_n, t_n, **{'RESULT': t_n['GRADE']}
                #         ).get_relationship()
                #     )
                pass
            if '进出口信用' in o['content'].keys():
                # ie_info = o['content']['进出口信用']
                # ies = IAE.create_from_dict(ie_info)
                # ies_n = self.create_nodes_from_iae(ies)
                # for ie_n in ies_n:
                #     relationships.append(
                #         Have(
                #             etp_n, ie_n
                #         ).get_relationship()
                #     )
                pass
            if '招聘信息' in o['content'].keys():
                # r_info = o['content']['招聘信息']
                # rs = Recruitment.create_from_dict(r_info)
                # rs_n = self.create_nodes_from_recruitment(rs)
                # TODO(leung):需要将招聘信息体现在关系上
                # for r_n in rs_n:
                #     relationships.append(
                #         Have(
                #             etp_n, r_n
                #         ).get_relationship()
                #     )
                pass
            if '客户' in o['content'].keys():
                # c_info = o['content']['客户']
                # cs = Client.create_from_dict(c_info)
                # cs_n = self.create_nodes_from_client(cs)
                # for c_n in cs_n:
                #     relationships.append(
                #         Sell(etp_n, c_n).get_relationship()
                #     )
                pass
            if '供应商' in o['content'].keys():
                # s_info = o['content']['供应商']
                # ss = Supplier.create_from_dict(s_info)
                # ss_n = self.create_nodes_from_client(ss)
                # for s_n in ss_n:
                #     relationships.append(
                #         Purchase(etp_n, s_n).get_relationship()
                #     )
                pass

            if len(relationships) > 1000:
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


# og = OptGraph()
# og.create_all_relationship()