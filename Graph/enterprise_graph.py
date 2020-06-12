# encoding: utf-8

"""
project = 'zlr'
file_name = 'enterprise_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:25'
from = 'office desktop' 
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.exception import ExceptionInfo, SuccessMessage
from Graph.entity import Enterprise, entities, legal, person
from Graph.relationship import LegalRep, Principal
from Graph.relationship import BeInOffice
from Graph.relationship import Located
from Graph.relationship import Share
from Graph.relationship import Have
from Graph.relationship import Investing
from Graph.relationship import BranchAgency
from Graph.relationship import SuperiorAgency


class EtpGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(
            tn='cq_all',
            # location='local2',
            # dbname='data'
        )
        pass

    def create_index_and_constraint(self):
        """
        为涉及到的实体创建唯一性约束跟索引，唯一键自动带有索引
        不必再单独创建索引
        :return:
        """
        # 用到的实体对象
        used_entity = [
            'Enterprise',
            'Person',
            'Telephone',
            'Address',
            'Email',
            # 'ShareHolder',
            # 'Branch',
            # 'HeadCompany',
            # 'Invested',
            # 'Related',
            'ConstructionProject',
            'Certificate'
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

    def create_nodes_from_enterprise_baseinfo(self, eb):
        """
        创建企业基本信息衍生出来的所有节点：
        1.企业
        2.法人代表
        3.管理人员
        4.地址
        实际上公司基本信息里面还衍生出了很多实体对象
        但这些对象是在后面随关系一并创建的
        :return:
        """
        nodes = []
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
                self.to_logs('filed initialize legal representative '
                             'Neo node', 'ERROR', eb['name'])
            else:
                nodes.append(lr_n)
        except Exception as e:
            self.to_logs('deal legal representative raise ({})'
                         ''.format(e), 'EXCEPTION', eb['name'])
        try:
            ms = etp.get_manager()
            if len(ms):
                for m in ms:
                    m_n = m['person']
                    m_n = m_n.get_neo_node(primarykey=m_n.primarykey)
                    if m_n is None:
                        self.to_logs('filed initialize major manager '
                                     'Neo node', 'ERROR', eb['name'])

                    else:
                        nodes.append(m_n)
        except Exception as e:
            self.to_logs('deal major managers raise ({})'.format(e),
                         'EXCEPTION', eb['name'])
        try:
            dz = etp.get_address()
            dz_n = dz.get_neo_node(primarykey=dz.primarykey)
            if dz_n is None:
                self.to_logs('filed initialize address Neo node',
                             'ERROR', eb['name'])
            else:
                nodes.append(dz_n)
        except Exception as e:
            self.to_logs('deal address raise ({})'.format(e),
                         'EXCEPTION', eb['name'])

        return nodes

    def get_all_nodes_from_enterprise(self, etp):
        nodes = [etp]
        try:
            lr = etp.get_legal_representative()
            if lr.isPerson():
                nodes.append(lr)
        except Exception as e:
            self.to_logs('deal legal representative raise ({})'
                         ''.format(e), 'EXCEPTION', etp['NAME'])
        try:
            ms = etp.get_manager()
            if len(ms):
                nodes += [m['person'] for m in ms]
        except Exception as e:
            self.to_logs('deal major managers raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            nodes.append(etp.get_address())
        except Exception as e:
            self.to_logs('deal address raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            nodes.append(etp.get_telephone_number())
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal telephone number raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            nodes.append(etp.get_email())
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal email raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            cps = etp.get_construction_project()
            if len(cps):
                nodes += [
                    c.pop('project') for c in cps
                ]
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction project raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ccs = etp.get_construction_certificate()
            nodes += [c.pop('ctf') for c in ccs]
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction certificate raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            sh = etp.get_share_holder()
            if len(sh):
                _nds_ = []
                for s in sh:
                    _s_ = s.pop('share_holder')
                    if _s_.isPerson():
                        _nds_.append(_s_)
                nodes += _nds_
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal share holder raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            brs = etp.get_branch()
            if len(brs):
                _nds_ = []
                for b in brs:
                    _p_ = b['principal']
                    if _p_.isPerson():
                        _nds_.append(_p_)
                nodes += _nds_
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal branch raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            hcs = etp.get_head_company()
            if len(hcs):
                _nds_ = []
                for h in hcs:
                    _p_ = h['principal']
                    if _p_.isPerson():
                        _nds_.append(_p_)
                nodes += _nds_
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal head company raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        return nodes

    def get_all_nodes(self):
        enterprises = self.base.query(
            sql={
                'metaModel': '基本信息',
                # 'name': {'$in': ns['name'].tolist()}
            },
            limit=10000,
            no_cursor_timeout=True)
        i, j = 0, 0
        # etp_count = enterprises.count()
        etp_count = 1000
        nodes = dict()
        for ep in enterprises:
            i += 1
            etp = Enterprise(ep)
            nds = self.get_all_nodes_from_enterprise(etp)
            for _nds_ in nds:
                if _nds_ is None:
                    continue
                _nds_ = _nds_.to_dict()
                if _nds_['label'] in nodes.keys():
                    nodes[_nds_['label']].append(_nds_)
                else:
                    nodes[_nds_['label']] = [_nds_]
                pass
            if i % 1000 == 0:
                j += 1
                print(SuccessMessage(
                    '{}:success merge nodes to database '
                    'round {} and deal {}/{} enterprise'
                    ''.format(dt.datetime.now(), j, i, etp_count)
                ))
            pass
        return nodes

    def create_all_nodes(self):
        """
        创建企业基本信息衍生出来的所有节点
        :return:
        """
        # import pandas as pd
        # ns = pd.read_csv('D:\graph_data\graph_run_logs_for_enterprise.csv')
        enterprises = self.base.query(
            sql={
                'metaModel': '基本信息',
                # 'name': {'$in': ns['name'].tolist()}
            },
            limit=1000,
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        nodes = []
        for e in enterprises:
            j += 1
            nds = self.create_nodes_from_enterprise_baseinfo(e)
            # nds = self.get_nodes_from_enterprise_baseinfo(e)
            nodes += nds
            if len(nodes) > 1000:
                i += 1
                # self.graph_merge_nodes(nodes)
                # if not self.index_and_constraint_statue:
                #     self.create_index_and_constraint()
                print(SuccessMessage('{}:success merge nodes to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} nodes.'.format(
                    dt.datetime.now(), i, j, etp_count, len(nodes)
                )))
                nodes.clear()
        if len(nodes):
            i += 1
            # self.graph_merge_nodes(nodes)
            # if not self.index_and_constraint_statue:
            #     self.create_index_and_constraint()
            print(SuccessMessage('{}:success merge nodes to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} nodes.'.format(
                dt.datetime.now(), i, j, etp_count, len(nodes)
            )))
            nodes.clear()
        pass

    def get_all_relationships_from_enterprise(self, etp):
        """
        创建从公司基本信息可以看出的关系：
        1.person-[lr]->enterprise
        2.person-[be_in_office]->enterprise
        3.enterprise-[located]->address
        4.person|enterprise-[holding]->enterprise
        5.enterprise-[have]->telephone
        6.enterprise-[have]->email
        :param :
        :return:
        """
        # 如果关系上的节点不存在，数据库同样会补充创建节点，这一点很重要
        rps = []
        etp_n = etp.get_neo_node(primarykey=etp.primarykey)
        if etp_n is None:
            self.to_logs('filed initialize enterprise Neo node',
                         'ERROR', etp['NAME'])
            return rps
        try:
            lr = etp.get_legal_representative()
            # 法定代表人有可能会是以下这些对象
            lr_n = self.match_node(
                *['Person'] + legal,
                cypher='_.URL = "{}"'.format(lr['URL'])
            )
            if lr_n is None:
                lr_n = lr.get_neo_node(primarykey=lr.primarykey)
            if lr_n is None:
                self.to_logs('filed initialize legal representative Neo node',
                             'ERROR', etp['NAME'])
            else:
                rps.append(LegalRep(lr_n, etp_n))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal legal representative raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ms = etp.get_manager()
            if len(ms):
                for m in ms:
                    # 主要人员 下面必然是人
                    m_n = m.pop('person')
                    m_n = m_n.get_neo_node(primarykey=m_n.primarykey)
                    if m_n is None:
                        self.to_logs('filed initialize major manager Neo node',
                                     'ERROR', etp['NAME'])
                    else:
                        rps.append(BeInOffice(m_n, etp_n, **m))
        except Exception as e:
            self.to_logs('deal major managers raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            dz = etp.get_address()
            dz_n = dz.get_neo_node(primarykey=dz.primarykey)
            if dz_n is None:
                self.to_logs('filed initialize address Neo node',
                             'ERROR', etp['NAME'])
            else:
                rps.append(Located(etp_n, dz_n))
        except Exception as e:
            self.to_logs('deal address raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            sh = etp.get_share_holder()
            if len(sh):
                for s in sh:
                    s_ = s.pop('share_holder')
                    # 股东有可能会是以下这些对象
                    sh_n = self.match_node(
                        'Person',
                        cypher='_.URL = "{}"'.format(s_['URL'])
                    )
                    if sh_n is None:
                        sh_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                s_['URL'], s_['NAME'])
                        )
                    if sh_n is None:  # 在以有的对象里面没找到这个股东
                        # 创建这个意外的股东
                        sh_n = s_.get_neo_node(primarykey=s_.primarykey)
                        if sh_n is None:
                            self.to_logs('filed initialize unexpected share '
                                         'holder Neo node', 'ERROR', etp['NAME'])
                    if sh_n is not None:
                        rps.append(Share(sh_n, etp_n, **s))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal share holder raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            tel = etp.get_telephone_number()
            if tel is None:
                # self.to_logs('there is not valid telephone for'
                #              ' this enterprise.', 'ERROR', eb['name'])
                pass
            else:
                tel_n = tel.get_neo_node(primarykey=tel.primarykey)
                if tel_n is None:
                    self.to_logs('filed initialize telephone Neo node',
                                 'ERROR', etp['NAME'])
                else:
                    rps.append(Have(etp_n, tel_n))
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal telephone number raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            eml = etp.get_email()
            if eml is None:
                # self.to_logs('there is not valid email for'
                #              ' this enterprise.', 'ERROR', eb['name'])
                pass
            else:
                eml_n = eml.get_neo_node(primarykey=eml.primarykey)
                if eml_n is None:
                    self.to_logs('filed initialize email Neo node',
                                 'ERROR', etp['NAME'])
                else:
                    rps.append(Have(etp_n, eml_n))
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal email raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ivs = etp.get_invest_outer()
            if len(ivs):
                for iv in ivs:
                    iv_ = iv.pop('invested')
                    # 被投资企业可能是下面这些对象
                    iv_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            iv_['URL'], iv_['NAME'])
                    )
                    if iv_n is None:
                        iv_n = iv_.get_neo_node(primarykey=iv_.primarykey)
                        if iv_n is None:
                            self.to_logs('filed initialize unexpected invested '
                                         'Neo node', 'ERROR', etp['NAME'])
                            continue
                    rps.append(Investing(etp_n, iv_n, **iv))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal invest raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            brs = etp.get_branch()
            if len(brs):
                for b in brs:
                    b_ = b.pop('branch')
                    # 分支机构可能是下面这些对象
                    b_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            b_['URL'], b_['NAME'])
                    )
                    if b_n is None:
                        b_n = b_.get_neo_node(primarykey=b_.primarykey)
                        if b_n is None:
                            self.to_logs('filed initialize unexpected branch '
                                         'Neo node', 'ERROR', etp['NAME'])
                            continue
                        p_ = b['principal']
                        p_n = p_.get_neo_node(primarykey=p_.primarykey)
                        if p_n is not None:
                            rps.append(Principal(p_n, b_n))
                    b.pop('principal')
                    rps.append(BranchAgency(
                        etp_n, b_n, **b
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal branch raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            hcs = etp.get_head_company()
            if len(hcs):
                for h in hcs:
                    h_ = h.pop('head')
                    # 总公司可能是下面这些对象
                    h_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            h_['URL'], h_['NAME'])
                    )
                    if h_n is None:
                        h_n = h_.get_neo_node(primarykey=h_.primarykey)
                        if h_n is None:
                            self.to_logs('filed initialize unexpected head '
                                         'company Neo node', 'ERROR', etp['NAME'])
                            continue
                        p_ = h['principal']
                        p_n = p_.get_neo_node(primarykey=p_.primarykey)
                        if p_n is not None:
                            rps.append(Principal(p_n, h_n))
                    h.pop('principal')
                    rps.append(SuperiorAgency(
                        etp_n, h_n, **h
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal head company raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            cps = etp.get_construction_project()
            if len(cps):
                for c in cps:
                    c_ = c.pop('project')
                    c_n = c_.get_neo_node(primarykey=c_.primarykey)
                    if c_n is None:
                        self.to_logs('filed initialize unexpected construction '
                                     'project Neo node', 'ERROR', etp['NAME'])
                        continue
                    jsdw = c.pop('jsdw')
                    # 查询这个建设单位是否已经存在
                    j_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            jsdw['URL'], jsdw['NAME'])
                    )
                    if j_n is None:
                        j_n = jsdw.get_neo_node(primarykey=jsdw.primarykey)
                        if j_n is None:
                            self.to_logs('filed initialize unexpected construction '
                                         'agency Neo node', 'ERROR', etp['NAME'])
                            continue
                    # TODO(lj):需要考虑是否将承建、建设单独列为一种关系
                    rps.append(Have(
                        etp_n, c_n, **dict(角色='承建单位', **c)
                    ))
                    rps.append(Have(
                        j_n, c_n, **dict(角色='建设单位', **c)
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction project raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ccs = etp.get_construction_certificate()
            if len(ccs):
                for c in ccs:
                    c_ = c.pop('ctf')
                    c_n = c_.get_neo_node(primarykey=c_.primarykey)
                    if c_n is None:
                        self.to_logs('filed initialize unexpected construction '
                                     'certificate Neo node', 'ERROR', etp['NAME'])
                        continue
                    rps.append(Have(etp_n, c_n, **c))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction certificate raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
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
        enterprises = self.base.query(
            sql={
                'metaModel': '基本信息',
                # 'name': '重庆长安汽车股份有限公司'
            },
            limit=1000,
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        relationships = []
        for _ in enterprises:
            j += 1
            etp = Enterprise(_)
            rps = self.get_relationship_from_enterprise(etp)
            relationships += rps

            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                if not self.index_and_constraint_statue:
                    self.create_index_and_constraint()
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, j, etp_count, len(relationships)
                )))
                relationships.clear()
                # if i > 10:
                #     return
        if len(relationships):
            i += 1
            self.graph_merge_relationships(relationships)
            if not self.index_and_constraint_statue:
                self.create_index_and_constraint()
            print(SuccessMessage('{}:success merge relationships to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} relationships.'.format(
                dt.datetime.now(), i, j, etp_count, len(relationships)
            )))
            relationships.clear()

    def get_all_relationships(self):
        enterprises = self.base.query(
            sql={
                'metaModel': '基本信息',
                # 'name': '重庆长安汽车股份有限公司'
            },
            limit=10000,
            no_cursor_timeout=True)
        i, j = 0, 0
        etp_count = enterprises.count()
        # etp_count = 1000
        relationships = {}
        for ep in enterprises:
            i += 1
            etp = Enterprise(ep)
            rps = self.get_all_relationships_from_enterprise(etp)
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
                    ''.format(dt.datetime.now(), j, i, etp_count)
                ))
            pass
        return relationships

    def get_all_nodes_and_relationships_from_enterprise(self, etp):
        """
        创建从公司基本信息可以看出的关系：
        1.person-[lr]->enterprise
        2.person-[be_in_office]->enterprise
        3.enterprise-[located]->address
        4.person|enterprise-[holding]->enterprise
        5.enterprise-[have]->telephone
        6.enterprise-[have]->email
        :param :
        :return:
        """
        # 如果关系上的节点不存在，数据库同样会补充创建节点，这一点很重要
        nodes, rps = [], []
        etp_n = self.get_neo_node(etp)
        if etp_n is None:
            self.to_logs('filed initialize enterprise Neo node',
                         'ERROR', etp['NAME'])
            return nodes, rps
        nodes.append(etp_n)
        try:
            lr = etp.get_legal_representative()
            # 法定代表人有可能会是以下这些对象
            lr_n = self.match_node(
                *['Person'] + legal,
                cypher='_.URL = "{}"'.format(lr['URL'])
            )
            if lr_n is None:
                lr_n = self.get_neo_node(lr)
            if lr_n is None:
                self.to_logs('filed initialize legal representative Neo node',
                             'ERROR', etp['NAME'])
            else:
                nodes.append(lr_n)
                rps.append(LegalRep(lr_n, etp_n))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal legal representative raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ms = etp.get_manager()
            if len(ms):
                for m in ms:
                    # 主要人员 下面必然是人
                    m_n = m.pop('person')
                    m_n = self.get_neo_node(m_n)
                    if m_n is None:
                        self.to_logs('filed initialize major manager Neo node',
                                     'ERROR', etp['NAME'])
                    else:
                        nodes.append(m_n)
                        rps.append(BeInOffice(m_n, etp_n, **m))
        except Exception as e:
            self.to_logs('deal major managers raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            dz = etp.get_address()
            dz_n = self.get_neo_node(dz)
            if dz_n is None:
                self.to_logs('filed initialize address Neo node',
                             'ERROR', etp['NAME'])
            else:
                nodes.append(dz_n)
                rps.append(Located(etp_n, dz_n))
        except Exception as e:
            self.to_logs('deal address raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            sh = etp.get_share_holder()
            if len(sh):
                for s in sh:
                    s_ = s.pop('share_holder')
                    # 股东有可能会是以下这些对象
                    sh_n = self.match_node(
                        'Person',
                        cypher='_.URL = "{}"'.format(s_['URL'])
                    )
                    if sh_n is None:
                        sh_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                s_['URL'], s_['NAME'])
                        )
                    if sh_n is None:  # 在以有的对象里面没找到这个股东
                        # 创建这个意外的股东
                        sh_n = self.get_neo_node(s_)
                        if sh_n is None:
                            self.to_logs('filed initialize unexpected share '
                                         'holder Neo node', 'ERROR', etp['NAME'])
                    if sh_n is not None:
                        nodes.append(sh_n)
                        rps.append(Share(sh_n, etp_n, **s))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal share holder raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            tel = etp.get_telephone_number()
            if tel is None:
                # self.to_logs('there is not valid telephone for'
                #              ' this enterprise.', 'ERROR', eb['name'])
                pass
            else:
                tel_n = self.get_neo_node(tel)
                if tel_n is None:
                    self.to_logs('filed initialize telephone Neo node',
                                 'ERROR', etp['NAME'])
                else:
                    nodes.append(tel_n)
                    rps.append(Have(etp_n, tel_n))
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal telephone number raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])

        try:
            eml = etp.get_email()
            if eml is None:
                # self.to_logs('there is not valid email for'
                #              ' this enterprise.', 'ERROR', eb['name'])
                pass
            else:
                eml_n = self.get_neo_node(eml)
                if eml_n is None:
                    self.to_logs('filed initialize email Neo node',
                                 'ERROR', etp['NAME'])
                else:
                    nodes.append(eml_n)
                    rps.append(Have(etp_n, eml_n))
            pass
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal email raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ivs = etp.get_invest_outer()
            if len(ivs):
                for iv in ivs:
                    iv_ = iv.pop('invested')
                    # 被投资企业可能是下面这些对象
                    iv_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            iv_['URL'], iv_['NAME'])
                    )
                    if iv_n is None:
                        iv_n = self.get_neo_node(iv_)
                        if iv_n is None:
                            self.to_logs('filed initialize unexpected invested '
                                         'Neo node', 'ERROR', etp['NAME'])
                            continue
                    nodes.append(iv_n)
                    rps.append(Investing(etp_n, iv_n, **iv))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal invest raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            brs = etp.get_branch()
            if len(brs):
                for b in brs:
                    b_ = b.pop('branch')
                    # 分支机构可能是下面这些对象
                    b_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            b_['URL'], b_['NAME'])
                    )
                    if b_n is None:
                        b_n = self.get_neo_node(b_)
                        if b_n is None:
                            self.to_logs('filed initialize unexpected branch '
                                         'Neo node', 'ERROR', etp['NAME'])
                            continue
                        p_ = b['principal']
                        p_n = self.get_neo_node(p_)
                        if p_n is not None:
                            nodes.append(p_n)
                            rps.append(Principal(p_n, b_n))
                    b.pop('principal')
                    nodes.append(b_n)
                    rps.append(BranchAgency(
                        etp_n, b_n, **b
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal branch raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            hcs = etp.get_head_company()
            if len(hcs):
                for h in hcs:
                    h_ = h.pop('head')
                    # 总公司可能是下面这些对象
                    h_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            h_['URL'], h_['NAME'])
                    )
                    if h_n is None:
                        h_n = self.get_neo_node(h_)
                        if h_n is None:
                            self.to_logs('filed initialize unexpected head '
                                         'company Neo node', 'ERROR', etp['NAME'])
                            continue
                        p_ = h['principal']
                        p_n = self.get_neo_node(p_)
                        if p_n is not None:
                            nodes.append(p_n)
                            rps.append(Principal(p_n, h_n))
                    h.pop('principal')
                    nodes.append(h_n)
                    rps.append(SuperiorAgency(
                        etp_n, h_n, **h
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal head company raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            cps = etp.get_construction_project()
            if len(cps):
                for c in cps:
                    c_ = c.pop('project')
                    c_n = self.get_neo_node(c_)
                    if c_n is None:
                        self.to_logs('filed initialize unexpected construction '
                                     'project Neo node', 'ERROR', etp['NAME'])
                        continue
                    jsdw = c.pop('jsdw')
                    # 查询这个建设单位是否已经存在
                    j_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            jsdw['URL'], jsdw['NAME'])
                    )
                    if j_n is None:
                        j_n = self.get_neo_node(jsdw)
                        if j_n is None:
                            self.to_logs('filed initialize unexpected construction '
                                         'agency Neo node', 'ERROR', etp['NAME'])
                            continue
                    # TODO(lj):需要考虑是否将承建、建设单独列为一种关系
                    nodes.append(c_n)
                    rps.append(Have(
                        etp_n, c_n, **dict(角色='承建单位', **c)
                    ))
                    nodes.append(j_n)
                    rps.append(Have(
                        j_n, c_n, **dict(角色='建设单位', **c)
                    ))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction project raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        try:
            ccs = etp.get_construction_certificate()
            if len(ccs):
                for c in ccs:
                    c_ = c.pop('ctf')
                    c_n = self.get_neo_node(c_)
                    if c_n is None:
                        self.to_logs('filed initialize unexpected construction '
                                     'certificate Neo node', 'ERROR', etp['NAME'])
                        continue
                    nodes.append(c_n)
                    rps.append(Have(etp_n, c_n, **c))
        except Exception as e:
            ExceptionInfo(e)
            self.to_logs('deal construction certificate raise ({})'.format(e),
                         'EXCEPTION', etp['NAME'])
        return nodes, rps

    def get_all_nodes_and_relationships(
            self, save_folder=None, **kwargs):
        enterprises = self.base.query(
            sql={
                'metaModel': '基本信息',
                # 'name': '重庆长寿城乡商贸总公司'   # {'$in': ns['name'].tolist()}
            },
            limit=100000,
            no_cursor_timeout=True)
        i, j = 0, 0
        nc, rc = 0, 0
        etp_count = enterprises.count()
        # etp_count = 1000
        nodes, relationships = {}, {}
        for ep in enterprises:
            try:
                i += 1
                etp = Enterprise(ep)
                nds, rps = self.get_all_nodes_and_relationships_from_enterprise(etp)
                for _nds_ in nds:
                    if _nds_ is None:
                        continue
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
            except Exception as e:
                ExceptionInfo(e)
                print(ep['name'])
                continue
            if i % 10000 == 0:
                j += 1
                if save_folder is not None:
                    _nc_, _rc_ = self.save_graph(
                        save_folder, nodes,
                        relationships, **kwargs)
                    nc += _nc_
                    rc += _rc_
                    nodes.clear()
                    relationships.clear()
                print(SuccessMessage(
                    '{}:success trans data to csv '
                    'round {} and deal {}/{} enterprise'
                    ''.format(dt.datetime.now(), j, i, etp_count)
                ))
                pass
        if save_folder is not None:
            _nc_, _rc_ = self.save_graph(
                save_folder, nodes,
                relationships, **kwargs)
            nc += _nc_
            rc += _rc_
            nodes.clear()
            relationships.clear()
            print('Summary:')
            print(' save graph data:')
            print('   {} nodes'.format(nc))
            print('   {} relationships'.format(rc))
            pass
        return nodes, relationships
