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
        etp_nds = []
        psn_nds = []
        ads_nds = []

        i = 0
        for _ in enterprises:
            i += 1
            etp = Enterprise(_)
            etp_n = etp.get_neo_node(primarykey='URL')
            if etp_n is None:
                self.to_logs('filed initialize enterprise Neo node',
                             'ERROR', _['name'])
                continue
            else:
                etp_nds.append(etp_n)
            try:
                lr = etp.get_legal_representative()
                lr_n = lr.get_neo_node(primarykey='URL')
                if lr_n is None:
                    self.to_logs('filed initialize legal representative Neo node',
                                 'ERROR', _['name'])
                else:
                    psn_nds.append(lr_n)
            except Exception as e:
                self.to_logs('deal legal representative raise ()'.format(e),
                             'EXCEPTION', _['name'])
            try:
                ms = etp.get_manager()
                if len(ms):
                    for m in ms:
                        m_n = m['person'].get_neo_node(primarykey='URL')
                        if m_n is None:
                            self.to_logs('filed initialize major manager Neo node',
                                         'ERROR', _['name'])

                        else:
                            psn_nds.append(m_n)
            except Exception as e:
                self.to_logs('deal major managers raise ()'.format(e),
                             'EXCEPTION', _['name'])
            # sh = etp.get_share_holder()
            try:
                dz = etp.get_address()
                dz_n = dz.get_neo_node(primarykey='ADDRESS')
                if dz_n is None:
                    self.to_logs('filed initialize address Neo node',
                                 'ERROR', _['name'])
                else:
                    ads_nds.append(dz_n)
            except Exception as e:
                self.to_logs('deal address raise ()'.format(e),
                             'EXCEPTION', _['name'])

            if i % 100 == 0:
                tx = self.graph.begin()
                tx.merge(Subgraph(etp_nds))
                tx.merge(Subgraph(psn_nds))
                tx.merge(Subgraph(ads_nds))
                tx.commit()
                etp_nds.clear()
                psn_nds.clear()
                ads_nds.clear()
                return

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
        lr_rps = []
        lc_rps = []
        bo_rps = []
        sh_rps = []
        unexpected_share_holder_nds = []
        i = 0
        for _ in enterprises:
            i += 1
            etp = Enterprise(_)
            etp_n = etp.get_neo_node(primarykey='URL')
            if etp_n is None:
                self.to_logs('filed initialize enterprise Neo node',
                             'ERROR', _['name'])
                continue
            try:
                lr = etp.get_legal_representative()
                lr_n = lr.get_neo_node(primarykey='URL')
                if lr_n is None:
                    self.to_logs('filed initialize legal representative Neo node',
                                 'ERROR', _['name'])
                else:
                    lr_rps.append(LegalRep(lr_n, etp_n).get_relationship())
            except Exception as e:
                self.to_logs('deal legal representative raise ()'.format(e),
                             'EXCEPTION', _['name'])
            try:
                ms = etp.get_manager()
                if len(ms):
                    for m in ms:
                        m_n = m.pop('person').get_neo_node(primarykey='URL')
                        if m_n is None:
                            self.to_logs('filed initialize major manager Neo node',
                                         'ERROR', _['name'])

                        else:
                            bo_rps.append(BeInOffice(m_n, etp_n, **m).get_relationship())
            except Exception as e:
                self.to_logs('deal major managers raise ()'.format(e),
                             'EXCEPTION', _['name'])
            # sh = etp.get_share_holder()
            try:
                dz = etp.get_address()
                dz_n = dz.get_neo_node(primarykey='ADDRESS')
                if dz_n is None:
                    self.to_logs('filed initialize address Neo node',
                                 'ERROR', _['name'])
                else:
                    lc_rps.append(Located(etp_n, dz_n).get_relationship())
            except Exception as e:
                self.to_logs('deal address raise ()'.format(e),
                             'EXCEPTION', _['name'])

            try:
                sh = etp.get_share_holder()
                if len(sh):
                    for s in sh:
                        s_ = s['share_holder']
                        # 1.在所有公司、人里面去找
                        sh_n_ed = self.NodeMatcher.match(
                            str(etp.label),
                            URL=s_.BaseAttributes['SHARE_HOLDER_URL']
                        ).first()
                        if sh_n_ed is None:
                            sh_n_ed = self.NodeMatcher.match(
                                str(lr.label),
                                URL=s_.BaseAttributes['SHARE_HOLDER_URL']
                            ).first()
                        if sh_n_ed is None:  # 在以有的对象里面没找到这个股东
                            # 创建这个意外的股东
                            sh_n = s_.get_neo_node(primarykey='SHARE_HOLDER_URL')
                            if sh_n is None:
                                self.to_logs('filed initialize unexpected share holder Neo node',
                                             'ERROR', _['name'])
                            else:
                                unexpected_share_holder_nds.append(sh_n)
                                sh_rps.append(ShareHolding(
                                    sh_n, etp_n
                                ).get_relationship())
                        else:
                            # sh_n_ed.__primarylabel__ = str(sh_n_ed.label)
                            # sh_n_ed.__primarykey__ = 'URL'
                            sh_rps.append(ShareHolding(
                                sh_n_ed, etp_n
                            ).get_relationship())
            except Exception as e:
                ExceptionInfo(e)
                self.to_logs('deal share holder raise ()'.format(e),
                             'EXCEPTION', _['name'])

            if i % 100 == 0:
                tx = self.graph.begin()
                if len(unexpected_share_holder_nds):
                    tx.merge(Subgraph(unexpected_share_holder_nds))
                # for r in lr_rps:
                #     tx.merge(r)
                tx.merge(Subgraph(relationships=lr_rps))
                # tx.merge(bo_rps)
                tx.merge(Subgraph(relationships=bo_rps))
                # tx.merge(lc_rps)
                tx.merge(Subgraph(relationships=lc_rps))
                tx.merge(Subgraph(relationships=sh_rps))
                tx.commit()
                unexpected_share_holder_nds.clear()
                lr_rps.clear()
                bo_rps.clear()
                lc_rps.clear()
                sh_rps.clear()
                return


eg = EtpGraph()
# eg.create_all_nodes()
eg.create_all_relationship()
