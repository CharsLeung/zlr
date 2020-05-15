# encoding: utf-8

"""
project = 'zlr'
file_name = 'justice_graph'
author = 'Administrator'
datetime = '2020/3/26 0026 上午 11:48'
from = 'office desktop' 
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import legal, entities
from Graph.entity import JusticeCase, Ruling, Involveder
from Graph.entity import Enterprise
from Graph.entity import Executed, SXExecuted
from Graph.entity import LimitOrder, StockFreeze
from Graph.exception import SuccessMessage
from Graph.relationship import InvolveCase
from Graph.enterprise_graph import EtpGraph


class JusGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(
            tn='qcc.1.1',
            location='gcxy',
            dbname='data')
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

    def create_all_nodes(self):
        """
        创建法律诉讼相关的实体对象，这些对象可以直接在
        数据库中“法律诉讼”一栏中获取
        1.司法案件
        2.某个司法案件涉及的公司没在数据中，那么应该创建这个公司
        :return:
        """
        justices = self.base.query(
            sql={'metaModel': '法律诉讼'},
            no_cursor_timeout=True)
        i, k = 0, 0
        nodes = []
        etp_count = justices.count()
        eg = EtpGraph()
        for j in justices:
            # 每个公司的法律诉讼下的司法案件肯定跟这个案件有联系
            # 一般情况下司法案件只会涉及到人或法人，法律诉讼这一
            # 板块是依存在企业信息下面的，所有自然跟这个被依存的
            # 企业有联系，我们先不考究这个依存的逻辑正确性，虽然
            # 案件本身里面的信息也能反映出涉案方，后期可能会需要
            k += 1
            etp_n = self.NodeMatcher.match(
                str(Enterprise.label),
                # TODO(leung): 这里要注意，法律诉讼模块中的url确定不了公司
                NAME=j['name']
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                # 不然这个司法案件存在就没有意义
                etp = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': j['name']}
                )
                if etp is not None:
                    etp_n = eg.create_nodes_from_enterprise_baseinfo(etp)
                    nodes += etp_n
                    # etp = Enterprise(etp)
                    # etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    # nodes.append(etp_n)

            if '司法案件' in j['content'].keys():
                justice_case_info = j['content']['司法案件']
                jcs = JusticeCase.create_from_dict(justice_case_info)
                jcs_n = self.create_nodes_from_justice_case(jcs)
                nodes += jcs_n
            if '裁决文书' in j['content'].keys():
                ruling_info = j['content']['裁决文书']
                # 返回的是[[Ruling, 相关对象],[]...]
                rls = Ruling.create_from_dict(ruling_info)
                rls_n = self.create_nodes_from_justice_case([r[0] for r in rls])
                nodes += rls_n
            if len(nodes) > 1000:
                i += 1
                self.graph_merge_nodes(nodes)
                print(SuccessMessage('{}:success merge nodes to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} nodes.'.format(
                    dt.datetime.now(), i, k, etp_count, len(nodes)
                )))
                nodes.clear()
        if len(nodes):
            i += 1
            self.graph_merge_nodes(nodes)
            print(SuccessMessage('{}:success merge nodes to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} nodes.'.format(
                dt.datetime.now(), i, k, etp_count, len(nodes)
            )))
            nodes.clear()
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
                eps = Executed.create_from_dict(data)
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
                rls = Ruling.create_from_dict(data)
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
                eps = SXExecuted.create_from_dict(data)
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

# jg = JusGraph()
# jg.create_all_nodes()
# jg.create_all_relationship()
