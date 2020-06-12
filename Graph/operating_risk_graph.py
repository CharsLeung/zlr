# encoding: utf-8

"""
project = zlr
file_name = operating_risk_graph
author = Administrator
datetime = 2020/4/1 0001 下午 13:58
from = office desktop
"""
import re
import datetime as dt

from Graph import BaseGraph
from py2neo import Relationship
from Calf.data import BaseModel
from Graph.entity import entities, legal, person
from Graph.entity import Punishment, Involveder
from Graph.entity import Enterprise, Possession
from Graph.entity import Debt, Related, Banknote
from Graph.entity import Plot, Person
from Graph.exception import SuccessMessage
from Graph.relationship import Guaranty, Have, ApplyBankrupt
from Graph.enterprise_graph import EtpGraph


class OptRiskGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(
            tn='cq_all',
            # tn='qcc.1.1',
            # location='gcxy',
            # dbname='data'
        )
        pass

    def create_index_and_constraint(self):
        """
        为涉及到的实体创建唯一性约束跟索引，唯一键自动带有索引
        不比再单独创建索引
        :return:
        """
        # TODO(leung): 要随时确保label的准确性
        used_entity = [
            'Punishment',
            'Possession',
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

    def create_all_relationship(self):
        """
        1.enterprise -[have]->punishment
        :return:
        """
        ors = self.base.query(
            sql={
                'metaModel': '经营风险',
                # 'name': '重庆铭悦机械设备有限公司'
            },
            limit=1000,
            # skip=2000,
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
            # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            etp_n = self.match_node(
                *legal,
                cypher='_.NAME = "{}"'.format(j['name'])
            )
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': j['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = self.get_neo_node(etp)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那么就简单的把这个公司理解成一个涉案者
                    # 这里就相当于把一个公司当做了一个风险提示的涉及者
                    # etp = Related(**{'名称': j['name'], '链接': j['url']})
                    etp = Related()
                    etp['NAME'] = j['name']
                    etp['URL'] = j['url']
                    etp_n = self.get_neo_node(etp)
                    pass

            if '动产抵押' in j['content'].keys():
                data = self.get_format_dict(j['content']['动产抵押'])
                for d in data:
                    _ = d.pop('被担保主债权数额')
                    debt = Debt(**{'债务(金额)': _['金额'],
                                   '债务(单位)': _['单位'],
                                   '履行期限': d.pop('债务人履行债务的期限')
                                   })
                    debt_n = self.get_neo_node(debt)
                    dy = d.pop('抵押权人')
                    zw = d.pop('债务人')
                    sy = d.pop('所有权或使用权归属')
                    if dy['名称'] == j['name'] or dy['链接'] == j['url']:
                        dy_n = etp_n
                    else:
                        dy_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                dy['链接'], dy['名称'])
                        )
                        if dy_n is None and len(dy['名称']) > 1:
                            dy_n = Related(**dy)
                            dy_n = self.get_neo_node(dy_n)
                    if dy_n is not None:
                        relationships.append(Have(
                            dy_n, debt_n, **dict(角色='抵押权人', **d)
                        ).get_relationship())

                    if zw['名称'] == j['name'] or zw['链接'] == j['url']:
                        zw_n = etp_n
                    else:
                        zw_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                zw['链接'], zw['名称'])
                        )
                        if zw_n is None and len(zw['名称']) > 1:
                            zw_n = Related(**zw)
                            zw_n = self.get_neo_node(zw_n)
                    if zw_n is not None:
                        relationships.append(Have(
                            zw_n, debt_n, **dict(角色='债务人', **d)
                        ).get_relationship())

                    if sy['名称'] == j['name'] or sy['链接'] == j['url']:
                        sy_n = etp_n
                    else:
                        sy_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                sy['链接'], sy['名称'])
                        )
                        if sy_n is None and len(sy['名称']) > 1:
                            sy_n = Related(**sy)
                            sy_n = self.get_neo_node(sy_n)
                    if sy_n is not None:
                        relationships.append(Have(
                            sy_n, debt_n, **dict(角色='所有权或使用权人', **d)
                        ).get_relationship())
                    pass

            if '公示催告' in j['content'].keys():
                data = self.get_format_dict(j['content']['公示催告'])
                for d in data:
                    _ = d.pop('票面金额')
                    bn = Banknote(**{'票据号': d.pop('票据号'),
                                     '票据类型': d.pop('票据类型'),
                                     '票面金额(金额)': _['金额'],
                                     '票面金额(单位)': _['单位']
                                     })
                    bn_n = self.get_neo_node(bn)
                    sq = d.pop('申请人')
                    cp = d.pop('持票人')
                    if sq['名称'] == j['name'] or sq['链接'] == j['url']:
                        sq_n = etp_n
                    else:
                        sq_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                sq['链接'], sq['名称'])
                        )
                        if sq_n is None:
                            sq_n = Related(**sq)
                            sq_n = self.get_neo_node(sq_n)
                    if sq_n is not None:
                        relationships.append(Have(
                            sq_n, bn_n, **dict(角色='申请人', **d)
                        ).get_relationship())

                    if cp['名称'] == j['name'] or cp['链接'] == j['url']:
                        cp_n = etp_n
                    else:
                        cp_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                cp['链接'], cp['名称'])
                        )
                        if cp_n is None:
                            cp_n = Related(**cp)
                            cp_n = self.get_neo_node(cp_n)
                    if cp_n is not None:
                        relationships.append(Have(
                            cp_n, bn_n, **dict(角色='持票人', **d)
                        ).get_relationship())
                    relationships.append(Have(
                        etp_n, bn_n, **dict(角色='出票人', **d)
                    ).get_relationship())
                    pass

            if '行政处罚' in j['content'].keys():
                data = j['content']['行政处罚']
                d1 = self.get_format_dict(data['工商局'])
                ps = Punishment.create_from_dict(d1, '工商局')
                for p in ps:
                    _ = p.pop('punishment')
                    n = self.get_neo_node(_)
                    if n is not None:
                        relationships.append(
                            Have(
                                etp_n, n, **p
                            ).get_relationship()
                        )

                d2 = self.get_format_dict(data['税务局'])
                ps = Punishment.create_from_dict(d2, '税务局')
                for p in ps:
                    _ = p.pop('punishment')
                    n = self.get_neo_node(_)
                    if n is not None:
                        relationships.append(
                            Have(
                                etp_n, n, **p
                            ).get_relationship()
                        )

                d3 = self.get_format_dict(data['信用中国'])
                ps = Punishment.create_from_dict(d3, '信用中国')
                for p in ps:
                    _ = p.pop('punishment')
                    n = self.get_neo_node(_)
                    if n is not None:
                        relationships.append(
                            Have(
                                etp_n, n, **p
                            ).get_relationship()
                        )

                d4 = self.get_format_dict(data['其他'])
                ps = Punishment.create_from_dict(d4, '其他')
                for p in ps:
                    _ = p.pop('punishment')
                    n = self.get_neo_node(_)
                    if n is not None:
                        relationships.append(
                            Have(
                                etp_n, n, **p
                            ).get_relationship()
                        )
                pass

            if '环保处罚' in j['content'].keys():
                data = self.get_format_dict(j['content']['环保处罚'])
                ps = Punishment.create_from_dict(data, '环保局')
                for p in ps:
                    _ = p.pop('punishment')
                    n = self.get_neo_node(_)
                    if n is not None:
                        relationships.append(
                            Have(
                                etp_n, n, **p
                            ).get_relationship()
                        )

            if '股权出质' in j['content'].keys():
                sh_info = j['content']['股权出质']
                sh_info = self.get_format_dict(sh_info)
                for sh in sh_info:
                    sh = dict(sh, **self.get_format_amount(
                        '出质数额', sh.pop('出质数额')
                    ))
                    # 确定出质人
                    cz = sh.pop('出质人')
                    cz['链接'] = etp.parser_url(cz['链接'])
                    # 判断出质人是不是当前公司
                    if j['name'] == cz['名称'] or cz['链接'] == etp_n['URL']:
                        cz_n = etp_n
                    else:
                        # 确定出质人，先在法人主体中找
                        cz_n = self.match_node(
                            *legal,
                            cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                                cz['名称'], cz['链接']
                            )
                        )
                        if cz_n is None:
                            # 在法人中没找到，就通过url在自然人中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            # TODO(leung):在所有实体中去找开销很大，需要注意
                            cz_n = self.match_node(
                                'Person',
                                cypher='_.URL = "{}"'.format(cz['链接'])
                            )
                            if cz_n is None:
                                # 创建这个股权出质人
                                if len(cz['名称']) > 1:
                                    cz_n = Involveder(**cz)
                                    cz_n = self.get_neo_node(cz_n)
                        pass
                    # 确定质权人
                    zq = sh.pop('质权人')
                    zq['链接'] = etp.parser_url(zq['链接'])
                    # 判断质权人是不是当前公司
                    if j['name'] == zq['名称'] or zq['链接'] == etp_n['URL']:
                        zq_n = etp_n
                    else:
                        # 确定质权人，先在企业中找
                        zq_n = self.match_node(
                            *legal,
                            cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                                zq['名称'], zq['链接']
                            )
                        )
                        if zq_n is None:
                            # 在企业中没找到，就通过url在所有对象中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            # TODO(leung):在所有实体中去找开销很大，需要注意
                            zq_n = self.match_node(
                                'Person',
                                cypher='_.URL = "{}"'.format(zq['链接'])
                            )
                            if zq_n is None:
                                # 创建这个股权出质人
                                if len(zq['名称']) > 1:
                                    zq_n = Involveder(**zq)
                                    zq_n = self.get_neo_node(zq_n)
                        pass
                    # 确定出质标的企业
                    bd = sh.pop('标的企业')
                    bd['链接'] = etp.parser_url(bd['链接'])
                    # 判断出质标的是不是当前公司
                    if j['name'] == bd['名称'] or bd['链接'] == etp_n['URL']:
                        bd_n = etp_n
                    else:
                        # 确定出质标的，先在企业中找
                        bd_n = self.match_node(
                            *legal,
                            cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                                bd['名称'], bd['链接']
                            )
                        )
                        if bd_n is None:
                            # 在企业中没找到，就通过url在所有对象中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            # TODO(leung):在所有实体中去找开销很大，需要注意
                            bd_n = self.match_node(
                                'Person',
                                cypher='_.URL = "{}"'.format(bd['链接'])
                            )
                            if bd_n is None:
                                # 创建这个出质标的
                                if len(bd['名称']) > 1:
                                    bd_n = Possession(**bd)
                                    bd_n = self.get_neo_node(bd_n)
                        pass
                    # 创建关系
                    # 1. 抵押
                    if cz_n is not None and bd_n is not None:
                        relationships.append(
                            Guaranty(cz_n, bd_n, **sh).get_relationship()
                        )
                    # 2. 质权
                    if zq_n is not None and bd_n is not None:
                        relationships.append(
                            Have(zq_n, bd_n, **sh).get_relationship()
                        )

            if '破产重组' in j['content'].keys():
                data = self.get_format_dict(j['content']['破产重组'])
                for d in data:
                    sq = d.pop('申请人')
                    if sq['名称'] == j['name'] or sq['链接'] == etp_n['URL']:
                        sq_n = etp_n
                    else:
                        sq_n = self.match_node(
                            *['person'] + legal,
                            cypher='_.URL = "{}"'.format(sq['链接'])
                        )
                        if sq_n is None:
                            sq_n = Involveder(**sq)
                            sq_n = self.get_neo_node(sq_n)
                    bsq = d.pop('被申请人')
                    if bsq['名称'] == j['name'] or bsq['链接'] == etp_n['URL']:
                        bsq_n = etp_n
                    else:
                        # 被申请破产的一般是法人
                        bsq_n = self.match_node(
                            *['person'] + legal,
                            cypher='_.URL = "{}"'.format(bsq['链接'])
                        )
                        if bsq_n is None:
                            bsq_n = Involveder(**bsq)
                            bsq_n = self.get_neo_node(bsq_n)
                    if sq_n is not None and bsq_n is not None:
                        relationships.append(
                            Relationship(sq_n, '申请破产', bsq_n, **d)
                        )
                pass

            if '土地抵押' in j['content'].keys():
                data = self.get_format_dict(j['content']['土地抵押'])
                for d in data:
                    _ = d.pop('抵押面积')
                    p = Plot(**{'位置': d.pop('位置'),
                                '面积(数量)': _['数额'],
                                '面积(单位)': _['单位'],
                                })
                    p_n = self.get_neo_node(p)
                    d = dict(d, **self.get_format_amount(
                        '抵押金额', d.pop('抵押金额')
                    ))
                    dy = d.pop('抵押人')
                    dyq = d.pop('抵押权人')

                    if dy['名称'] == j['name'] or dy['链接'] == etp_n['URL']:
                        dy_n = etp_n
                    else:
                        dy_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                dy['链接'], dy['名称'])
                        )
                        if dy_n is None:
                            dy_n = Related(**dy)
                            dy_n = self.get_neo_node(dy_n)
                    if dy_n is not None:
                        relationships.append(
                            Guaranty(dy_n, p_n, **d).get_relationship()
                        )
                    if dyq['名称'] == j['name'] or dyq['链接'] == etp_n['URL']:
                        dyq_n = etp_n
                    else:
                        dyq_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                                dyq['链接'], dyq['名称'])
                        )
                        if dyq_n is None:
                            dyq_n = Related(**dyq)
                            dyq_n = self.get_neo_node(dyq_n)
                    if dyq_n is not None:
                        relationships.append(
                            Have(dyq_n, p_n, **d).get_relationship()
                        )
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
                pass
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

    def get_all_nodes_and_relationships_from_enterprise(self, etp):
        etp_n = Enterprise(URL=etp['url'], NAME=etp['name'])
        etp_n = self.get_neo_node(etp_n)
        if etp_n is None:
            return [], []
        nodes, relationships = [], []
        nodes.append(etp_n)
        if '动产抵押' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['动产抵押'])
            for d in data:
                _ = d.pop('被担保主债权数额')
                debt = Debt(**{'债务(金额)': _['金额'],
                               '债务(单位)': _['单位'],
                               '履行期限': d.pop('债务人履行债务的期限')
                               })
                debt_n = self.get_neo_node(debt)
                nodes.append(debt_n)
                dy = d.pop('抵押权人')
                zw = d.pop('债务人')
                sy = d.pop('所有权或使用权归属')
                dy['链接'] = Enterprise.parser_url(dy['链接'])
                zw['链接'] = Enterprise.parser_url(zw['链接'])
                sy['链接'] = Enterprise.parser_url(sy['链接'])
                if dy['名称'] == etp['name'] or dy['链接'] == etp['url']:
                    dy_n = etp_n
                else:
                    dy_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            dy['链接'], dy['名称'])
                    )
                    if dy_n is None:
                        # dy_n = Related(**dy)
                        dy_n = Enterprise(**dy)
                        if not dy_n.isEnterprise():
                            dy_n = Person(**dy)
                            if not dy_n.isPerson():
                                dy_n = Related(**dy)
                        dy_n = self.get_neo_node(dy_n)
                if dy_n is not None:
                    nodes.append(dy_n)
                    relationships.append(Have(
                        dy_n, debt_n, **dict(角色='抵押权人', **d)
                    ))

                if zw['名称'] == etp['name'] or zw['链接'] == etp['url']:
                    zw_n = etp_n
                else:
                    zw_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            zw['链接'], zw['名称'])
                    )
                    if zw_n is None and len(zw['名称']) > 1:
                        # zw_n = Related(**zw)
                        zw_n = Enterprise(**zw)
                        if not zw_n.isEnterprise():
                            zw_n = Person(**zw)
                            if not zw_n.isPerson():
                                zw_n = Related(**zw)
                        zw_n = self.get_neo_node(zw_n)
                if zw_n is not None:
                    nodes.append(zw_n)
                    relationships.append(Have(
                        zw_n, debt_n, **dict(角色='债务人', **d)
                    ))

                if sy['名称'] == etp['name'] or sy['链接'] == etp['url']:
                    sy_n = etp_n
                else:
                    sy_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            sy['链接'], sy['名称'])
                    )
                    if sy_n is None and len(sy['名称']) > 1:
                        # sy_n = Related(**sy)
                        sy_n = Enterprise(**sy)
                        if not sy_n.isEnterprise():
                            sy_n = Person(**sy)
                            if not sy_n.isPerson():
                                sy_n = Related(**sy)
                        sy_n = self.get_neo_node(sy_n)
                if sy_n is not None:
                    nodes.append(sy_n)
                    relationships.append(Have(
                        sy_n, debt_n, **dict(角色='所有权或使用权人', **d)
                    ))
                pass

        if '公示催告' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['公示催告'])
            for d in data:
                _ = d.pop('票面金额')
                bn = Banknote(**{'票据号': d.pop('票据号'),
                                 '票据类型': d.pop('票据类型'),
                                 '票面金额(金额)': _['金额'],
                                 '票面金额(单位)': _['单位']
                                 })
                bn_n = self.get_neo_node(bn)
                nodes.append(bn_n)
                sq = d.pop('申请人')
                cp = d.pop('持票人')
                sq['链接'] = Enterprise.parser_url(sq['链接'])
                cp['链接'] = Enterprise.parser_url(cp['链接'])
                if sq['名称'] == etp['name'] or sq['链接'] == etp['url']:
                    sq_n = etp_n
                else:
                    sq_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            sq['链接'], sq['名称'])
                    )
                    if sq_n is None:
                        # sq_n = Related(**sq)
                        sq_n = Enterprise(**sq)
                        if not sq_n.isEnterprise():
                            sq_n = Person(**sq)
                            if not sq_n.isPerson():
                                sq_n = Related(**sq)
                        sq_n = self.get_neo_node(sq_n)
                if sq_n is not None:
                    nodes.append(sq_n)
                    relationships.append(Have(
                        sq_n, bn_n, **dict(角色='申请人', **d)
                    ))

                if cp['名称'] == etp['name'] or cp['链接'] == etp['url']:
                    cp_n = etp_n
                else:
                    cp_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            cp['链接'], cp['名称'])
                    )
                    if cp_n is None:
                        # cp_n = Related(**cp)
                        cp_n = Enterprise(**cp)
                        if not cp_n.isEnterprise():
                            cp_n = Person(**cp)
                            if not cp_n.isPerson():
                                cp_n = Related(**cp)
                        cp_n = self.get_neo_node(cp_n)
                if cp_n is not None:
                    nodes.append(cp_n)
                    relationships.append(Have(
                        cp_n, bn_n, **dict(角色='持票人', **d)
                    ))
                relationships.append(Have(
                    etp_n, bn_n, **dict(角色='出票人', **d)
                ))
                pass

        if '行政处罚' in etp['content'].keys():
            data = etp['content']['行政处罚']
            d1 = self.get_format_dict(data['工商局'])
            ps = Punishment.create_from_dict(d1, '工商局')
            for p in ps:
                _ = p.pop('punishment')
                n = self.get_neo_node(_)
                if n is not None:
                    nodes.append(n)
                    relationships.append(
                        Have(etp_n, n, **p)
                    )

            d2 = self.get_format_dict(data['税务局'])
            ps = Punishment.create_from_dict(d2, '税务局')
            for p in ps:
                _ = p.pop('punishment')
                n = self.get_neo_node(_)
                if n is not None:
                    nodes.append(n)
                    relationships.append(
                        Have(etp_n, n, **p)
                    )

            d3 = self.get_format_dict(data['信用中国'])
            ps = Punishment.create_from_dict(d3, '信用中国')
            for p in ps:
                _ = p.pop('punishment')
                n = self.get_neo_node(_)
                if n is not None:
                    nodes.append(n)
                    relationships.append(
                        Have(etp_n, n, **p)
                    )

            d4 = self.get_format_dict(data['其他'])
            ps = Punishment.create_from_dict(d4, '其他')
            for p in ps:
                _ = p.pop('punishment')
                n = self.get_neo_node(_)
                if n is not None:
                    nodes.append(n)
                    relationships.append(
                        Have(etp_n, n, **p)
                    )
            pass

        if '环保处罚' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['环保处罚'])
            ps = Punishment.create_from_dict(data, '环保局')
            for p in ps:
                _ = p.pop('punishment')
                n = self.get_neo_node(_)
                if n is not None:
                    nodes.append(n)
                    relationships.append(
                        Have(etp_n, n, **p)
                    )

        if '股权出质' in etp['content'].keys():
            sh_info = etp['content']['股权出质']
            sh_info = self.get_format_dict(sh_info)
            for sh in sh_info:
                sh = dict(sh, **self.get_format_amount(
                    '出质数额', sh.pop('出质数额')
                ))
                # 确定出质人
                cz = sh.pop('出质人')
                cz['链接'] = Enterprise.parser_url(cz['链接'])
                # 判断出质人是不是当前公司
                if etp['name'] == cz['名称'] or cz['链接'] == etp_n['URL']:
                    cz_n = etp_n
                else:
                    # 确定出质人，先在法人主体中找
                    cz_n = self.match_node(
                        *legal,
                        cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                            cz['名称'], cz['链接']
                        )
                    )
                    if cz_n is None:
                        # 在法人中没找到，就通过url在自然人中找
                        # 这里最好不要通过名称找了，除公司以外出现
                        # 同名的几率很大
                        # TODO(leung):在所有实体中去找开销很大，需要注意
                        cz_n = self.match_node(
                            'Person',
                            cypher='_.URL = "{}"'.format(cz['链接'])
                        )
                        if cz_n is None:
                            # 创建这个股权出质人
                            if len(cz['名称']) > 1:
                                # cz_n = Involveder(**cz)
                                cz_n = Enterprise(**cz)
                                if not cz_n.isEnterprise():
                                    cz_n = Person(**cz)
                                    if not cz_n.isPerson():
                                        cz_n = Related(**cz)
                                cz_n = self.get_neo_node(cz_n)
                    pass
                # 确定质权人
                zq = sh.pop('质权人')
                zq['链接'] = Enterprise.parser_url(zq['链接'])
                # 判断质权人是不是当前公司
                if etp['name'] == zq['名称'] or zq['链接'] == etp_n['URL']:
                    zq_n = etp_n
                else:
                    # 确定质权人，先在企业中找
                    zq_n = self.match_node(
                        *legal,
                        cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                            zq['名称'], zq['链接']
                        )
                    )
                    if zq_n is None:
                        # 在企业中没找到，就通过url在所有对象中找
                        # 这里最好不要通过名称找了，除公司以外出现
                        # 同名的几率很大
                        # TODO(leung):在所有实体中去找开销很大，需要注意
                        zq_n = self.match_node(
                            'Person',
                            cypher='_.URL = "{}"'.format(zq['链接'])
                        )
                        if zq_n is None:
                            # 创建这个股权出质人
                            if len(zq['名称']) > 1:
                                # zq_n = Involveder(**zq)
                                zq_n = Enterprise(**zq)
                                if not zq_n.isEnterprise():
                                    zq_n = Person(**zq)
                                    if not zq_n.isPerson():
                                        zq_n = Related(**zq)
                                zq_n = self.get_neo_node(zq_n)
                    pass
                # 确定出质标的企业
                bd = sh.pop('标的企业')
                bd['链接'] = Enterprise.parser_url(bd['链接'])
                # 判断出质标的是不是当前公司
                if etp['name'] == bd['名称'] or bd['链接'] == etp_n['URL']:
                    bd_n = etp_n
                else:
                    # 确定出质标的，先在企业中找，不会是人
                    bd_n = self.match_node(
                        *legal,
                        cypher='_.NAME = "{}" OR _.URL = "{}"'.format(
                            bd['名称'], bd['链接']
                        )
                    )
                    if bd_n is None:
                        # 创建这个出质标的
                        if len(bd['名称']) > 1:
                            bd_n = Enterprise(**bd)
                            if not bd_n.isEnterprise():
                                bd_n = Possession(**bd)
                            bd_n = self.get_neo_node(bd_n)
                    pass
                # 创建关系
                if bd_n is None:
                    continue
                nodes.append(bd_n)
                # 1. 抵押
                if cz_n is not None:
                    nodes.append(cz_n)
                    relationships.append(
                        Guaranty(cz_n, bd_n, **sh)
                    )
                # 2. 质权
                if zq_n is not None:
                    nodes.append(zq_n)
                    relationships.append(
                        Have(zq_n, bd_n, **sh)
                    )

        if '破产重组' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['破产重组'])
            for d in data:
                sq = d.pop('申请人')
                sq['链接'] = Enterprise.parser_url(sq['链接'])
                if sq['名称'] == etp['name'] or sq['链接'] == etp_n['URL']:
                    sq_n = etp_n
                else:
                    sq_n = self.match_node(
                        *['person'] + legal,
                        cypher='_.URL = "{}"'.format(sq['链接'])
                    )
                    if sq_n is None:
                        # sq_n = Involveder(**sq)
                        sq_n = Enterprise(**sq)
                        if not sq_n.isEnterprise():
                            sq_n = Person(**sq)
                            if not sq_n.isPerson():
                                sq_n = Related(**sq)
                        sq_n = self.get_neo_node(sq_n)
                bsq = d.pop('被申请人')
                bsq['链接'] = Enterprise.parser_url(bsq['链接'])
                if bsq['名称'] == etp['name'] or bsq['链接'] == etp_n['URL']:
                    bsq_n = etp_n
                else:
                    # 被申请破产的一般是法人
                    bsq_n = self.match_node(
                        *['person'] + legal,
                        cypher='_.URL = "{}"'.format(bsq['链接'])
                    )
                    if bsq_n is None:
                        # bsq_n = Involveder(**bsq)
                        bsq_n = Enterprise(**bsq)
                        if not bsq_n.isEnterprise():
                            bsq_n = Person(**bsq)
                            if not bsq_n.isPerson():
                                bsq_n = Related(**bsq)
                        bsq_n = self.get_neo_node(bsq_n)
                if sq_n is not None and bsq_n is not None:
                    nodes += [sq_n, bsq_n]
                    relationships.append(
                        ApplyBankrupt(sq_n, bsq_n, **d)
                    )
            pass

        if '土地抵押' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['土地抵押'])
            for d in data:
                _ = d.pop('抵押面积')
                p = Plot(**{'位置': d.pop('位置'),
                            '面积(数量)': _['数额'],
                            '面积(单位)': _['单位'],
                            })
                p_n = self.get_neo_node(p)
                nodes.append(p_n)
                d = dict(d, **self.get_format_amount(
                    '抵押金额', d.pop('抵押金额')
                ))
                dy = d.pop('抵押人')
                dyq = d.pop('抵押权人')
                dy['链接'] = Enterprise.parser_url(dy['链接'])
                dyq['链接'] = Enterprise.parser_url(dyq['链接'])
                if dy['名称'] == etp['name'] or dy['链接'] == etp_n['URL']:
                    dy_n = etp_n
                else:
                    dy_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            dy['链接'], dy['名称'])
                    )
                    if dy_n is None:
                        # dy_n = Related(**dy)
                        dy_n = Enterprise(**dy)
                        if not dy_n.isEnterprise():
                            dy_n = Person(**dy)
                            if not dy_n.isPerson():
                                dy_n = Related(**dy)
                        dy_n = self.get_neo_node(dy_n)
                if dy_n is not None:
                    nodes.append(dy_n)
                    relationships.append(
                        Guaranty(dy_n, p_n, **d)
                    )
                if dyq['名称'] == etp['name'] or dyq['链接'] == etp_n['URL']:
                    dyq_n = etp_n
                else:
                    dyq_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            dyq['链接'], dyq['名称'])
                    )
                    if dyq_n is None:
                        # dyq_n = Related(**dyq)
                        dyq_n = Enterprise(**dyq)
                        if not dyq_n.isEnterprise():
                            dyq_n = Person(**dyq)
                            if not dyq_n.isPerson():
                                dyq_n = Related(**dyq)
                        dyq_n = self.get_neo_node(dyq_n)
                if dyq_n is not None:
                    nodes.append(dyq_n)
                    relationships.append(
                        Have(dyq_n, p_n, **d)
                    )
            pass

        return nodes, relationships

    def get_all_nodes_and_relationships(
            self, save_folder=None, **kwargs):
        enterprises = self.base.query(
            sql={
                'metaModel': '经营风险',
                # 'name': '重庆轩烽建材有限公司'
            },
            limit=100000,
            # skip=2000,
            no_cursor_timeout=True)
        i, j = 0, 0
        nc, rc = 0, 0
        etp_count = enterprises.count()
        nodes, relationships = {}, {}
        unique_code_pattern = re.compile('(?<=unique=)\w{32}')

        def getUniqueCode(url):
            _uc_ = re.search(unique_code_pattern, url)
            if _uc_ is not None:
                return _uc_.group(0)
            else:
                return None

        for ep in enterprises:
            i += 1
            uc = getUniqueCode(ep['url'])
            if uc is None:
                print('{}:mismatch url'.format(ep['name']))
                continue
            ep['url'] = '/firm_' + uc + '.html'
            nds, rps = self.get_all_nodes_and_relationships_from_enterprise(ep)
            for _nds_ in nds:
                if _nds_ is None:
                    continue
                # _nds_ = _nds_.to_dict()
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
