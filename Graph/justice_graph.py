# encoding: utf-8

"""
project = 'zlr'
file_name = 'justice_graph'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 11:48'
from = 'office desktop' 
"""
import re
import datetime as dt

from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import legal, entities
from Graph.entity import JudicialCase, Judgment, Involveder
from Graph.entity import CourtAnnounce, OpenAnnounce, DeliveryAnnounce
from Graph.entity import RegisterCase, FinalCase
from Graph.entity import Enterprise, Person, Related
from Graph.entity import Enforcement, SXEnforcement
from Graph.entity import LimitOrder, StockFreeze
from Graph.exception import SuccessMessage
from Graph.relationship import InvolveCase
from Graph.enterprise_graph import EtpGraph


class JusGraph(BaseGraph):

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
        # 用到的实体对象
        used_entity = [
            # 'JusticeCase',
            'Ruling',
            'Involveder',
            'Executed',
            'SXExecuted',
            'LimitOrder',
            'StockFreeze'
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

    def create_relationship_from_justice_case(
            self, suspect, justice_case, **kwargs):
        """
        enterprise or person -[involve_case]->justice case
        :param suspect:
        :param justice_case:
        :param kwargs:
        :return:
        """
        rps = []
        for jc in justice_case:
            kwargs = dict(kwargs, **{'案件身份': jc.CASE_IDENTITY})
            jc_n = jc.get_neo_node(primarykey=jc.primarykey)
            if jc_n is None:
                self.to_logs('filed initialize justice case Neo node',
                             'ERROR')
            else:
                rps.append(InvolveCase(
                    suspect, jc_n, **kwargs
                ).get_relationship())
        return rps

    def create_all_relationship(self):
        """
        1.enterprise or person -[involve_case]->case
        :return:
        """
        justices = self.base.query(
            sql={
                'metaModel': '法律诉讼',
                # 'name': '重庆思途科技有限公司'
            },
            limit=100,
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = justices.count()
        relationships = []
        # prs = Person()
        # etp = Enterprise()
        for j in justices:
            # 每个公司的法律诉讼下的司法案件肯定跟这个案件有联系
            k += 1
            # if k < 4910:
            #     continue
            # TODO(leung): 这里要注意，法律诉讼模块中的url确定不了公司
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
                    etp = Involveder(**{'名称': j['name'], '链接': j['url']})
                    etp_n = self.get_neo_node(etp)
                    if etp_n is None:
                        continue
                    pass

            if '被执行人' in j['content'].keys():
                data = self.get_format_dict(j['content']['被执行人'])
                eps = Enforcement.create_from_dict(data)
                for ep in eps:
                    e = ep.pop('executed')
                    e_n = self.get_neo_node(e)
                    if e_n is not None:
                        relationships.append(
                            InvolveCase(etp_n, e_n, **ep).get_relationship()
                        )
                pass

            # if '司法案件' in j['content'].keys():
            #     justice_case_info = j['content']['司法案件']
            #     jcs = JusticeCase.create_from_dict(justice_case_info)
            #     rps = self.create_relationship_from_justice_case(
            #         etp_n, jcs)
            #     relationships += rps
            #     pass

            if '裁判文书' in j['content'].keys():
                data = self.get_format_dict(j['content']['裁判文书'])
                # 返回的是[[Ruling, 相关对象],[]...]
                rls = Judgment.create_from_dict(data)
                for ruling, involve in rls:
                    rul_n = self.get_neo_node(ruling)
                    if rul_n is None:
                        continue
                    for inv in involve:
                        # 案件相关主体
                        # 先判断是不是当前的企业
                        if j['name'] == inv[1] or j['url'] == inv[2]:
                            # 如果是，直接关联起来
                            inv_n = etp_n
                        else:
                            # 1.先在企业中匹配
                            # 2.匹配自然人
                            inv_n = self.match_node(
                                *['Person'] + legal,
                                cypher='_.URL = "{}"'.format(
                                    inv[2])
                            )
                            if inv_n is None:
                                ivl = Involveder()
                                ivl['NAME'] = inv[1]
                                ivl['URL'] = inv[2]
                                # if inv[2] is not None:
                                #     ivl['URL'] = inv[2]
                                # else:
                                #     ivl['URL'] = ivl.get_entity_unique_code(
                                #         j['name']+inv[1]
                                #     )
                                inv_n = self.get_neo_node(ivl)
                        # 3.以上两者都没匹配到的时候，创建这个案件参与者
                        # 实际上还可以到其他实体中去匹配，但那些可能是数据
                        # 集之外的对象了，可以先不去管他们

                        if inv_n is not None:
                            relationships.append(
                                InvolveCase(
                                    inv_n, rul_n, **{'案件身份': inv[0]}
                                ).get_relationship()
                            )
                pass

            if '失信被执行人' in j['content'].keys():
                data = self.get_format_dict(
                    j['content']['失信被执行人']
                )
                eps = SXEnforcement.create_from_dict(data)
                for ep in eps:
                    e = ep.pop('sxexecuted')
                    e_n = self.get_neo_node(e)
                    if e_n is not None:
                        relationships.append(
                            InvolveCase(etp_n, e_n, **ep).get_relationship()
                        )
                pass

            if '限制高消费' in j['content'].keys():
                data = self.get_format_dict(
                    j['content']['限制高消费']
                )
                for d in data:
                    sq = d.pop('申请人')
                    lh = d.pop('限消令对象')
                    xg = d.pop('关联对象')
                    _ = d.pop('案号')
                    lo = dict(案号=_['名称'], 案号链接=_['链接'], **d)
                    lo = LimitOrder(**lo)
                    lo_n = self.get_neo_node(lo)
                    if lo_n is None:
                        continue
                    if sq['名称'] == j['name'] or sq['链接'] == etp_n['URL']:
                        sq_n = etp_n
                    else:
                        sq_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                sq['链接'])
                        )
                        if sq_n is None:
                            # 创建这个对象
                            sq_n = Involveder(**sq)
                            sq_n = self.get_neo_node(sq_n)
                    if sq_n is not None:
                        relationships.append(
                            InvolveCase(sq_n, lo_n, **{'案件身份': '申请人'}
                                        ).get_relationship()
                        )
                    if lh['名称'] == j['name'] or lh['链接'] == etp_n['URL']:
                        lh_n = etp_n
                    else:
                        lh_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                lh['链接'])
                        )
                        if lh_n is None:
                            # 创建这个对象
                            lh_n = Involveder(**lh)
                            lh_n = self.get_neo_node(lh_n)
                    if lh_n is not None:
                        relationships.append(
                            InvolveCase(lo_n, lh_n, **{'案件身份': '限制对象'}
                                        ).get_relationship()
                        )
                    if xg['名称'] == j['name'] or xg['链接'] == etp_n['URL']:
                        xg_n = etp_n
                    else:
                        xg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                xg['链接'])
                        )
                        if xg_n is None:
                            # 创建这个对象
                            xg_n = Involveder(**xg)
                            xg_n = self.get_neo_node(xg_n)
                    if xg_n is not None:
                        relationships.append(
                            InvolveCase(lo_n, xg_n, **{'案件身份': '关联对象'}
                                        ).get_relationship()
                        )
                pass

            if '股权冻结' in j['content'].keys():
                data = self.get_format_dict(
                    j['content']['股权冻结']
                )
                for d in data:
                    bd = d.pop('标的企业')
                    zx = d.pop('被执行人')
                    _1 = d.pop('股权数额')
                    _2 = d.pop('类型|状态').split('|')
                    sf = dict(冻结数额=_1['金额'], 金额单位=_1['单位'],
                              类型=_2[0], 状态=_2[1] if len(_2) > 1 else None, **d
                              )
                    sf = StockFreeze(**sf)
                    sf_n = self.get_neo_node(sf)
                    if sf_n is None:
                        continue
                    if bd['名称'] == j['name'] or bd['链接'] == etp_n['URL']:
                        bd_n = etp_n
                    else:
                        bd_n = self.match_node(
                            *legal,
                            cypher='_.URL = "{}"'.format(
                                bd['链接'])
                        )
                        if bd_n is None:
                            bd_n = Involveder(**bd)
                            bd_n = self.get_neo_node(bd_n)
                    if bd_n is not None:
                        relationships.append(
                            InvolveCase(sf_n, bd_n, **{'案件身份': '标的企业'}
                                        ).get_relationship()
                        )
                    if zx['名称'] == j['name'] or zx['链接'] == etp_n['URL']:
                        zx_n = etp_n
                    else:
                        zx_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                zx['链接'])
                        )
                        if zx_n is None:
                            zx_n = Involveder(**zx)
                            zx_n = self.get_neo_node(zx_n)
                    if zx_n is not None:
                        relationships.append(
                            InvolveCase(sf_n, zx_n, **{'案件身份': '被执行人'}
                                        ).get_relationship()
                        )

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

        if '法院公告' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['法院公告']
            )
            cas = CourtAnnounce.create_from_dict(data)
            for ca in cas:
                a = ca.pop('announce')
                a_n = self.get_neo_node(a)
                if a_n is None:
                    continue
                nodes.append(a_n)
                bgs = ca.pop('defendant')
                for bg in bgs:
                    bg['链接'] = Enterprise.parser_url(bg['链接'])
                    if bg['名称'] == etp['name'] or bg['链接'] == etp_n['URL']:
                        bg_n = etp_n
                    else:
                        bg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                bg['链接'])
                        )
                        if bg_n is None:
                            # 创建这个对象
                            # sq_n = Involveder(**sq)
                            bg_n = Enterprise(**bg)
                            if not bg_n.isEnterprise():
                                bg_n = Person(**bg)
                                if not bg_n.isPerson():
                                    bg_n = Related(**bg)
                            bg_n = self.get_neo_node(bg_n)
                    if bg_n is not None:
                        nodes.append(bg_n)
                        relationships.append(
                            InvolveCase(bg_n, a_n, **{'案件身份': '被告'})
                        )
                ygs = ca.pop('plaintiff')
                for yg in ygs:
                    yg['链接'] = Enterprise.parser_url(yg['链接'])
                    if yg['名称'] == etp['name'] or yg['链接'] == etp_n['URL']:
                        yg_n = etp_n
                    else:
                        yg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                yg['链接'])
                        )
                        if yg_n is None:
                            # 创建这个对象
                            # lh_n = Involveder(**lh)
                            yg_n = Enterprise(**yg)
                            if not yg_n.isEnterprise():
                                yg_n = Person(**yg)
                                if not yg_n.isPerson():
                                    yg_n = Related(**yg)
                            yg_n = self.get_neo_node(yg_n)
                    if yg_n is not None:
                        nodes.append(yg_n)
                        relationships.append(
                            InvolveCase(yg_n, a_n, **{'案件身份': '原告'})
                        )
            pass

        if '开庭公告' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['开庭公告']
            )
            cas = OpenAnnounce.create_from_dict(data)
            for ca in cas:
                a = ca.pop('announce')
                a_n = self.get_neo_node(a)
                if a_n is None:
                    continue
                nodes.append(a_n)
                bgs = ca.pop('defendant')
                for bg in bgs:
                    bg['链接'] = Enterprise.parser_url(bg['链接'])
                    if bg['名称'] == etp['name'] or bg['链接'] == etp_n['URL']:
                        bg_n = etp_n
                    else:
                        bg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                bg['链接'])
                        )
                        if bg_n is None:
                            # 创建这个对象
                            # sq_n = Involveder(**sq)
                            bg_n = Enterprise(**bg)
                            if not bg_n.isEnterprise():
                                bg_n = Person(**bg)
                                if not bg_n.isPerson():
                                    bg_n = Related(**bg)
                            bg_n = self.get_neo_node(bg_n)
                    if bg_n is not None:
                        nodes.append(bg_n)
                        relationships.append(
                            InvolveCase(bg_n, a_n, **{'案件身份': '被告'})
                        )
                ygs = ca.pop('plaintiff')
                for yg in ygs:
                    yg['链接'] = Enterprise.parser_url(yg['链接'])
                    if yg['名称'] == etp['name'] or yg['链接'] == etp_n['URL']:
                        yg_n = etp_n
                    else:
                        yg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                yg['链接'])
                        )
                        if yg_n is None:
                            # 创建这个对象
                            # lh_n = Involveder(**lh)
                            yg_n = Enterprise(**yg)
                            if not yg_n.isEnterprise():
                                yg_n = Person(**yg)
                                if not yg_n.isPerson():
                                    yg_n = Related(**yg)
                            yg_n = self.get_neo_node(yg_n)
                    if yg_n is not None:
                        nodes.append(yg_n)
                        relationships.append(
                            InvolveCase(yg_n, a_n, **{'案件身份': '原告'})
                        )
            pass

        if '送达公告' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['送达公告']
            )
            cas = OpenAnnounce.create_from_dict(data)
            for ca in cas:
                a = ca.pop('announce')
                a_n = self.get_neo_node(a)
                if a_n is None:
                    continue
                nodes.append(a_n)
                bgs = ca.pop('defendant')
                for bg in bgs:
                    bg['链接'] = Enterprise.parser_url(bg['链接'])
                    if bg['名称'] == etp['name'] or bg['链接'] == etp_n['URL']:
                        bg_n = etp_n
                    else:
                        bg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                bg['链接'])
                        )
                        if bg_n is None:
                            # 创建这个对象
                            # sq_n = Involveder(**sq)
                            bg_n = Enterprise(**bg)
                            if not bg_n.isEnterprise():
                                bg_n = Person(**bg)
                                if not bg_n.isPerson():
                                    bg_n = Related(**bg)
                            bg_n = self.get_neo_node(bg_n)
                    if bg_n is not None:
                        nodes.append(bg_n)
                        relationships.append(
                            InvolveCase(bg_n, a_n, **{'案件身份': '被告'})
                        )
                ygs = ca.pop('plaintiff')
                for yg in ygs:
                    yg['链接'] = Enterprise.parser_url(yg['链接'])
                    if yg['名称'] == etp['name'] or yg['链接'] == etp_n['URL']:
                        yg_n = etp_n
                    else:
                        yg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                yg['链接'])
                        )
                        if yg_n is None:
                            # 创建这个对象
                            # lh_n = Involveder(**lh)
                            yg_n = Enterprise(**yg)
                            if not yg_n.isEnterprise():
                                yg_n = Person(**yg)
                                if not yg_n.isPerson():
                                    yg_n = Related(**yg)
                            yg_n = self.get_neo_node(yg_n)
                    if yg_n is not None:
                        nodes.append(yg_n)
                        relationships.append(
                            InvolveCase(yg_n, a_n, **{'案件身份': '原告'})
                        )
            pass

        if '立案信息' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['立案信息']
            )
            cas = RegisterCase.create_from_dict(data)
            for ca in cas:
                c = ca.pop('case')
                c_n = self.get_neo_node(c)
                if c_n is None:
                    continue
                nodes.append(c_n)
                bgs = ca.pop('defendant')
                for bg in bgs:
                    bg['链接'] = Enterprise.parser_url(bg['链接'])
                    if bg['名称'] == etp['name'] or bg['链接'] == etp_n['URL']:
                        bg_n = etp_n
                    else:
                        bg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                bg['链接'])
                        )
                        if bg_n is None:
                            # 创建这个对象
                            # sq_n = Involveder(**sq)
                            bg_n = Enterprise(**bg)
                            if not bg_n.isEnterprise():
                                bg_n = Person(**bg)
                                if not bg_n.isPerson():
                                    bg_n = Related(**bg)
                            bg_n = self.get_neo_node(bg_n)
                    if bg_n is not None:
                        nodes.append(bg_n)
                        relationships.append(
                            InvolveCase(bg_n, c_n, **{'案件身份': '被告'})
                        )
                ygs = ca.pop('plaintiff')
                for yg in ygs:
                    yg['链接'] = Enterprise.parser_url(yg['链接'])
                    if yg['名称'] == etp['name'] or yg['链接'] == etp_n['URL']:
                        yg_n = etp_n
                    else:
                        yg_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                yg['链接'])
                        )
                        if yg_n is None:
                            # 创建这个对象
                            # lh_n = Involveder(**lh)
                            yg_n = Enterprise(**yg)
                            if not yg_n.isEnterprise():
                                yg_n = Person(**yg)
                                if not yg_n.isPerson():
                                    yg_n = Related(**yg)
                            yg_n = self.get_neo_node(yg_n)
                    if yg_n is not None:
                        nodes.append(yg_n)
                        relationships.append(
                            InvolveCase(yg_n, c_n, **{'案件身份': '原告'})
                        )
            pass

        if '终本案件' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['终本案件']
            )
            cas = FinalCase.create_from_dict(data)
            for ca in cas:
                c = ca.pop('case')
                c_n = self.get_neo_node(c)
                if c_n is None:
                    continue
                nodes.append(c_n)
                relationships.append(
                    InvolveCase(etp_n, c_n)
                )

        if '裁判文书' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['裁判文书'])
            # 返回的是[[Ruling, 相关对象],[]...]
            rls = Judgment.create_from_dict(data)
            for ruling, involve in rls:
                rul_n = self.get_neo_node(ruling)
                if rul_n is None:
                    continue
                nodes.append(rul_n)
                for inv in involve:
                    # 案件相关主体
                    # 先判断是不是当前的企业
                    inv[2] = Enterprise.parser_url(inv[2])
                    if etp['name'] == inv[1] or etp['url'] == inv[2]:
                        # 如果是，直接关联起来
                        inv_n = etp_n
                    else:
                        # 1.先在企业中匹配
                        # 2.匹配自然人
                        inv_n = self.match_node(
                            *['Person'] + legal,
                            cypher='_.URL = "{}"'.format(
                                inv[2])
                        )
                        if inv_n is None:
                            # ivl = Involveder()
                            _ivl_ = {'名称': inv[1], '链接': inv[2]}
                            ivl = Enterprise(**_ivl_)
                            if not ivl.isEnterprise():
                                ivl = Person(**_ivl_)
                                if not ivl.isPerson():
                                    ivl = Related(**_ivl_)
                            inv_n = self.get_neo_node(ivl)
                    # 3.以上两者都没匹配到的时候，创建这个案件参与者
                    # 实际上还可以到其他实体中去匹配，但那些可能是数据
                    # 集之外的对象了，可以先不去管他们

                    if inv_n is not None:
                        nodes.append(inv_n)
                        relationships.append(
                            InvolveCase(
                                inv_n, rul_n, **{'案件身份': inv[0]}
                            )
                        )
            pass

        if '被执行人' in etp['content'].keys():
            data = self.get_format_dict(etp['content']['被执行人'])
            eps = Enforcement.create_from_dict(data)
            for ep in eps:
                e = ep.pop('executed')
                e_n = self.get_neo_node(e)
                if e_n is not None:
                    nodes.append(e_n)
                    relationships.append(
                        InvolveCase(etp_n, e_n, **ep)
                    )
            pass

        if '失信被执行人' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['失信被执行人']
            )
            eps = SXEnforcement.create_from_dict(data)
            for ep in eps:
                e = ep.pop('sxexecuted')
                e_n = self.get_neo_node(e)
                if e_n is not None:
                    nodes.append(e_n)
                    relationships.append(
                        InvolveCase(etp_n, e_n, **ep)
                    )
            pass

        if '限制高消费' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['限制高消费']
            )
            for d in data:
                sq = d.pop('申请人')
                lh = d.pop('限消令对象')
                xg = d.pop('关联对象')
                sq['链接'] = Enterprise.parser_url(sq['链接'])
                lh['链接'] = Enterprise.parser_url(lh['链接'])
                xg['链接'] = Enterprise.parser_url(xg['链接'])
                _ = d.pop('案号')
                lo = dict(案号=_['名称'], 案号链接=_['链接'], **d)
                lo = LimitOrder(**lo)
                lo_n = self.get_neo_node(lo)
                if lo_n is None:
                    continue
                nodes.append(lo_n)
                if sq['名称'] == etp['name'] or sq['链接'] == etp_n['URL']:
                    sq_n = etp_n
                else:
                    sq_n = self.match_node(
                        *['Person'] + legal,
                        cypher='_.URL = "{}"'.format(
                            sq['链接'])
                    )
                    if sq_n is None:
                        # 创建这个对象
                        # sq_n = Involveder(**sq)
                        sq_n = Enterprise(**sq)
                        if not sq_n.isEnterprise():
                            sq_n = Person(**sq)
                            if not sq_n.isPerson():
                                sq_n = Related(**sq)
                        sq_n = self.get_neo_node(sq_n)
                if sq_n is not None:
                    nodes.append(sq_n)
                    relationships.append(
                        InvolveCase(sq_n, lo_n, **{'案件身份': '申请人'})
                    )
                if lh['名称'] == etp['name'] or lh['链接'] == etp_n['URL']:
                    lh_n = etp_n
                else:
                    lh_n = self.match_node(
                        *['Person'] + legal,
                        cypher='_.URL = "{}"'.format(
                            lh['链接'])
                    )
                    if lh_n is None:
                        # 创建这个对象
                        # lh_n = Involveder(**lh)
                        lh_n = Enterprise(**lh)
                        if not lh_n.isEnterprise():
                            lh_n = Person(**lh)
                            if not lh_n.isPerson():
                                lh_n = Related(**lh)
                        lh_n = self.get_neo_node(lh_n)
                if lh_n is not None:
                    nodes.append(lh_n)
                    relationships.append(
                        InvolveCase(lo_n, lh_n, **{'案件身份': '限制对象'})
                    )
                if xg['名称'] == etp['name'] or xg['链接'] == etp_n['URL']:
                    xg_n = etp_n
                else:
                    xg_n = self.match_node(
                        *['Person'] + legal,
                        cypher='_.URL = "{}"'.format(
                            xg['链接'])
                    )
                    if xg_n is None:
                        # 创建这个对象
                        # xg_n = Involveder(**xg)
                        xg_n = Enterprise(**xg)
                        if not xg_n.isEnterprise():
                            xg_n = Person(**xg)
                            if not xg_n.isPerson():
                                xg_n = Related(**xg)
                        xg_n = self.get_neo_node(xg_n)
                if xg_n is not None:
                    nodes.append(xg_n)
                    relationships.append(
                        InvolveCase(lo_n, xg_n, **{'案件身份': '关联对象'})
                    )
            pass

        if '股权冻结' in etp['content'].keys():
            data = self.get_format_dict(
                etp['content']['股权冻结']
            )
            for d in data:
                bd = d.pop('标的企业')
                zx = d.pop('被执行人')
                bd['链接'] = Enterprise.parser_url(bd['链接'])
                zx['链接'] = Enterprise.parser_url(zx['链接'])
                _1 = d.pop('股权数额')
                _2 = d.pop('类型|状态').split('|')
                sf = dict(冻结数额=_1['金额'], 金额单位=_1['单位'],
                          类型=_2[0], 状态=_2[1] if len(_2) > 1 else None, **d
                          )
                sf = StockFreeze(**sf)
                sf_n = self.get_neo_node(sf)
                if sf_n is None:
                    continue
                nodes.append(sf_n)
                if bd['名称'] == etp['name'] or bd['链接'] == etp_n['URL']:
                    bd_n = etp_n
                else:
                    bd_n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}"'.format(
                            bd['链接'])
                    )
                    if bd_n is None:
                        # bd_n = Involveder(**bd)
                        bd_n = Enterprise(**bd)
                        if not bd_n.isEnterprise():
                            bd_n = Person(**bd)
                            if not bd_n.isPerson():
                                bd_n = Related(**bd)
                        bd_n = self.get_neo_node(bd_n)
                if bd_n is not None:
                    nodes.append(bd_n)
                    relationships.append(
                        InvolveCase(sf_n, bd_n, **{'案件身份': '标的企业'})
                    )
                if zx['名称'] == etp['name'] or zx['链接'] == etp_n['URL']:
                    zx_n = etp_n
                else:
                    zx_n = self.match_node(
                        *['Person'] + legal,
                        cypher='_.URL = "{}"'.format(
                            zx['链接'])
                    )
                    if zx_n is None:
                        # zx_n = Involveder(**zx)
                        zx_n = Enterprise(**zx)
                        if not zx_n.isEnterprise():
                            zx_n = Person(**zx)
                            if not zx_n.isPerson():
                                zx_n = Related(**zx)
                        zx_n = self.get_neo_node(zx_n)
                if zx_n is not None:
                    nodes.append(zx_n)
                    relationships.append(
                        InvolveCase(sf_n, zx_n, **{'案件身份': '被执行人'})
                    )
            pass

        return nodes, relationships

    def get_all_nodes_and_relationships(
            self, save_folder=None, **kwargs):
        enterprises = self.base.query(
            sql={
                'metaModel': '法律诉讼',
                # 'name': '重庆合文贸易有限公司'
            },
            limit=10000,
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

# jg = JusGraph()
# jg.create_all_nodes()
# jg.create_all_relationship()
