# encoding: utf-8

"""
project = 'zlr'
file_name = 'enterprise_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:25'
from = 'office desktop' 
"""
import datetime as dt
from py2neo import Subgraph
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo, SuccessMessage
from Graph.entity import Enterprise
from Graph.relationship import LegalRep
from Graph.relationship import BeInOffice
from Graph.relationship import Located
from Graph.relationship import ShareHolding
from Graph.relationship import Have


class EtpGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_nodes_from_enterprise_baseinfo(self, enterprise_baseinfo):
        """
        创建企业基本信息衍生出来的所有节点：
        1.企业
        2.法人代表
        3.管理人员
        4.地址
        实际上公司基本信息里面还包含一个很重要的对象：行业，但
        行业作为一个重要的对象单独处理
        :return:
        """
        nodes = []
        eb = enterprise_baseinfo
        etp = Enterprise(eb)
        etp_n = etp.get_neo_node(primarykey=etp.primarykey)
        if etp_n is None:
            self.to_logs('filed initialize enterprise Neo node',
                         'ERROR', eb['name'])
            return None
        else:
            nodes.append(etp_n)
        try:
            lr = etp.get_legal_representative()
            lr_n = lr.get_neo_node(primarykey=lr.primarykey)
            if lr_n is None:
                self.to_logs('filed initialize legal representative Neo node',
                             'ERROR', eb['name'])
            else:
                nodes.append(lr_n)
        except Exception as e:
            self.to_logs('deal legal representative raise ()'.format(e),
                         'EXCEPTION', eb['name'])
        try:
            ms = etp.get_manager()
            if len(ms):
                for m in ms:
                    m_n = m['person']
                    m_n = m_n.get_neo_node(primarykey=m_n.primarykey)
                    if m_n is None:
                        self.to_logs('filed initialize major manager Neo node',
                                     'ERROR', eb['name'])

                    else:
                        nodes.append(m_n)
        except Exception as e:
            self.to_logs('deal major managers raise ()'.format(e),
                         'EXCEPTION', eb['name'])
        # sh = etp.get_share_holder()
        try:
            dz = etp.get_address()
            dz_n = dz.get_neo_node(primarykey=dz.primarykey)
            if dz_n is None:
                self.to_logs('filed initialize address Neo node',
                             'ERROR', eb['name'])
            else:
                nodes.append(dz_n)
        except Exception as e:
            self.to_logs('deal address raise ()'.format(e),
                         'EXCEPTION', eb['name'])

        return nodes

    def create_all_nodes(self):
        """
        创建企业基本信息衍生出来的所有节点：
        1.企业
        2.法人代表
        3.管理人员
        4.地址
        实际上公司基本信息里面还包含一个很重要的对象：行业，但
        行业作为一个重要的对象单独处理
        :return:
        """
        # enterprises = self.base.aggregate(pipeline=[
        #     {'$match': {'metaModel': '基本信息'}},
        #     # {'$project': {'_id': 1, 'name': 1}}
        # ])
        enterprises = self.base.query(
            sql={'metaModel': '基本信息'},
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        nodes = []
        for e in enterprises:
            j += 1
            if j < 0:
                continue
            nds = self.create_nodes_from_enterprise_baseinfo(e)
            nodes += nds
            if len(nodes) > 1000:
                i += 1
                self.graph_merge_nodes(nodes)
                # tx = self.graph.begin()
                # tx.merge(Subgraph(nodes))
                # tx.commit()
                print(SuccessMessage('{}:success merge nodes to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} nodes.'.format(
                    dt.datetime.now(), i, j, etp_count, len(nodes)
                )))
                nodes.clear()

    def create_relationship_from_enterprise_baseinfo(self, enterprise_baseinfo):
        """
        创建从公司基本信息可以看出的关系：
        1.person-[lr]->enterprise
        2.person-[be_in_office]->enterprise
        3.enterprise-[located]->address
        4.person|enterprise-[holding]->enterprise
        5.enterprise-[have]->telephone
        6.enterprise-[have]->email
        :param enterprise_baseinfo:
        :return:
        """
        # 如果关系上的节点不存在，数据库同样会补充创建节点，这一点很重要
        rps = []
        eb = enterprise_baseinfo
        etp = Enterprise(eb)
        etp_n = etp.get_neo_node(primarykey=etp.primarykey)
        if etp_n is None:
            self.to_logs('filed initialize enterprise Neo node',
                         'ERROR', eb['name'])
            return rps
        try:
            lr = etp.get_legal_representative()
            lr_n = lr.get_neo_node(primarykey=lr.primarykey)
            if lr_n is None:
                self.to_logs('filed initialize legal representative Neo node',
                             'ERROR', eb['name'])
            else:
                rps.append(LegalRep(lr_n, etp_n).get_relationship())
        except Exception as e:
            self.to_logs('deal legal representative raise ()'.format(e),
                         'EXCEPTION', eb['name'])
        try:
            ms = etp.get_manager()
            if len(ms):
                for m in ms:
                    m_n = m.pop('person')
                    m_n = m_n.get_neo_node(primarykey=m_n.primarykey)
                    if m_n is None:
                        self.to_logs('filed initialize major manager Neo node',
                                     'ERROR', eb['name'])
                    else:
                        rps.append(BeInOffice(m_n, etp_n, **m).get_relationship())
        except Exception as e:
            self.to_logs('deal major managers raise ()'.format(e),
                         'EXCEPTION', eb['name'])
        # sh = etp.get_share_holder()
        try:
            dz = etp.get_address()
            dz_n = dz.get_neo_node(primarykey=dz.primarykey)
            if dz_n is None:
                self.to_logs('filed initialize address Neo node',
                             'ERROR', eb['name'])
            else:
                rps.append(Located(etp_n, dz_n).get_relationship())
        except Exception as e:
            self.to_logs('deal address raise ()'.format(e),
                         'EXCEPTION', eb['name'])

        try:
            sh = etp.get_share_holder()
            if len(sh):
                for s in sh:
                    s_ = s['share_holder']
                    # 1.在所有公司里面去找
                    sh_n_ed = self.NodeMatcher.match(
                        etp.label,
                        # **{etp.primarykey: s_.BaseAttributes[s_.primarykey]}
                    ).where('_.NAME = "{}" OR _.{} = "{}"'.format(
                        s_.BaseAttributes['NAME'], etp.primarykey,
                        s_.BaseAttributes[s_.primarykey]
                    )).first()
                    if sh_n_ed is None:
                        # 2.在人里面去找
                        sh_n_ed = self.NodeMatcher.match(
                            str(lr.label),
                            **{lr.primarykey: s_.BaseAttributes[s_.primarykey]}
                        ).first()
                    if sh_n_ed is None:  # 在以有的对象里面没找到这个股东
                        # 创建这个意外的股东
                        sh_n = s_.get_neo_node(primarykey=s_.primarykey)
                        if sh_n is None:
                            self.to_logs('filed initialize unexpected share holder Neo node',
                                         'ERROR', eb['name'])
                        else:
                            # unexpected_share_holder_nds.append(sh_n)
                            rps.append(ShareHolding(
                                sh_n, etp_n
                            ).get_relationship())
                    else:
                        # 此时的sh_n_ed可能就是一个企业或者个人，
                        # ShareHolding的属性需要补充进来
                        s_.BaseAttributes.pop('NAME')
                        s_.BaseAttributes.pop('URL')
                        rps.append(ShareHolding(
                            sh_n_ed, etp_n, **s_.BaseAttributes
                        ).get_relationship())
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal share holder raise ()'.format(e),
                         'EXCEPTION', eb['name'])

        try:
            tel = etp.get_telephone_number()
            if tel is None:
                self.to_logs('there is not valid telephone for'
                             ' this enterprise.', 'ERROR', eb['name'])
            else:
                tel_n = tel.get_neo_node(primarykey=tel.primarykey)
                if tel_n is None:
                    self.to_logs('filed initialize telephone Neo node',
                                 'ERROR', eb['name'])
                else:
                    rps.append(Have(etp_n, tel_n).get_relationship())
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal telephone number raise ()'.format(e),
                         'EXCEPTION', eb['name'])

        try:
            eml = etp.get_email()
            if eml is None:
                self.to_logs('there is not valid email for'
                             ' this enterprise.', 'ERROR', eb['name'])
            else:
                eml_n = eml.get_neo_node(primarykey=eml.primarykey)
                if eml_n is None:
                    self.to_logs('filed initialize email Neo node',
                                 'ERROR', eb['name'])
                else:
                    rps.append(Have(etp_n, eml_n).get_relationship())
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal email raise ()'.format(e),
                         'EXCEPTION', eb['name'])
        return rps

    def create_all_relationship(self):
        """
        创建从公司基本信息可以看出的关系：
        1.person-[lr]->enterprise
        2.person-[be_in_office]->enterprise
        3.enterprise-[located]->address
        4.person|enterprise-[holding]->enterprise
        :return:
        """
        # enterprises = self.base.aggregate(pipeline=[
        #     {'$match': {'metaModel': '基本信息'}},
        #     # {'$project': {'_id': 1, 'name': 1}}
        # ])
        enterprises = self.base.query(
            sql={'metaModel': '基本信息'},
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        relationships = []
        for _ in enterprises:
            j += 1
            rps = self.create_relationship_from_enterprise_baseinfo(_)
            relationships += rps

            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, j, etp_count, len(relationships)
                )))
                relationships.clear()
                # return
