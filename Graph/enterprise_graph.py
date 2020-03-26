# encoding: utf-8

"""
project = 'zlr'
file_name = 'enterprise_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:25'
from = 'office desktop' 
"""
from py2neo import Subgraph
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo
from Graph.entity import Enterprise
from Graph.relationship import LegalRep
from Graph.relationship import BeInOffice
from Graph.relationship import Located
from Graph.relationship import ShareHolding


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
        enterprises = self.base.aggregate(pipeline=[
            {'$match': {'metaModel': '基本信息'}},
            # {'$project': {'_id': 1, 'name': 1}}
        ])
        nodes = []

        for _ in enterprises:
            nds = self.create_nodes_from_enterprise_baseinfo(_)
            nodes += nds
            if len(nodes) > 100:
                tx = self.graph.begin()
                tx.merge(Subgraph(nodes))
                tx.commit()
                nodes.clear()
                return

    def create_relationship_from_enterprise_baseinfo(self, enterprise_baseinfo):
        """
        创建从公司基本信息可以看出的关系：
        1.person-[lr]->enterprise
        2.person-[be_in_office]->enterprise
        3.enterprise-[located]->address
        4.person|enterprise-[holding]->enterprise
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
                        str(etp.label),
                        **{etp.primarykey: s_.BaseAttributes[s_.primarykey]}
                    ).first()
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
                        rps.append(ShareHolding(
                            sh_n_ed, etp_n
                        ).get_relationship())
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal share holder raise ()'.format(e),
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
        enterprises = self.base.aggregate(pipeline=[
            {'$match': {'metaModel': '基本信息'}},
            # {'$project': {'_id': 1, 'name': 1}}
        ])
        relationships = []
        for _ in enterprises:
            rps = self.create_relationship_from_enterprise_baseinfo(_)
            relationships += rps

            if len(relationships) > 100:
                tx = self.graph.begin()
                tx.merge(Subgraph(relationships=relationships))
                tx.commit()
                relationships.clear()
                return

# eg = EtpGraph()
# eg.create_all_nodes()
# eg.create_all_relationship()
