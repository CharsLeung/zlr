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
from Graph.entity import entities, legal, person
from Graph.entity import Enterprise, License, Bidding
from Graph.entity import Check, RandomCheck, TaxCredit
from Graph.entity import IAE, Position, Client, Supplier
from Graph.entity import Related, Plot
from Graph.relationship import Have, TakePartIn
from Graph.relationship import SellTo, Purchase, Recruit
from Graph.relationship import Appraise, Sell, Buy
from Graph.enterprise_graph import EtpGraph


class OptGraph(BaseGraph):

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
        # 用到是实体对象
        used_entity = [
            'License',
            'Bidding',
            'Check',
            'RandomCheck',
            'TaxCredit',
            'IAE',
            'Position',
            'Client',
            'Supplier',
            # 'Possession',
            'Plot'
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
        1.enterprise -[have or x]->x
        :return:
        """
        ops = self.base.query(
            sql={
                'metaModel': '经营状况',
                # 'name': '重庆轩烽建材有限公司'
            },
            limit=1000,
            # skip=2000,
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp_count = ops.count()
        relationships = []
        # etp = Enterprise()
        for o in ops:
            k += 1
            # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            etp_n = self.match_node(
                *legal,
                cypher='_.NAME = "{}"'.format(o['name'])
            )
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': o['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = self.get_neo_node(etp)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那就创建一个信息不全的公司
                    # 如果在neo4j里面存着只有name,url的公司，意味着
                    # 这家公司没有“基本信息”
                    etp = Related()
                    etp['NAME'] = o['name']
                    etp['URL'] = o['url']
                    etp_n = self.get_neo_node(etp)
                    pass

            if '产权交易' in o['content'].keys():
                # data = self.get_format_dict(o['content']['产权交易'])
                # for d in data:
                #     bd = d.pop('标的')
                #     bd_n =
                pass

            if '行政许可' in o['content'].keys():
                data = o['content']['行政许可']
                if '工商局' in data.keys():
                    d1 = self.get_format_dict(data['工商局'])
                    ls = License.create_from_dict(d1, '工商局')
                    for l in ls:
                        l_ = l.pop('license')
                        l_n = self.get_neo_node(l_)
                        if l_n is None:
                            continue
                        relationships.append(
                            Have(etp_n, l_n, **l).get_relationship()
                        )
                    pass
                if '信用中国' in data.keys():
                    d2 = self.get_format_dict(data['信用中国'])
                    ls = License.create_from_dict(d2, '信用中国')
                    for l in ls:
                        l_ = l.pop('license')
                        l_n = self.get_neo_node(l_)
                        if l_n is None:
                            continue
                        relationships.append(
                            Have(etp_n, l_n, **l).get_relationship()
                        )
                    pass
                pass
            if '招投标信息' in o['content'].keys():
                # 公示的招投标信息一般都是结果，一般情况下是找不到
                # 共同投标的单位，除非是共同中标
                data = self.get_format_dict(
                    o['content']['招投标信息']
                )
                bs = Bidding.create_from_dict(data)
                for b in bs:
                    _ = b.pop('bidding')
                    b_n = self.get_neo_node(_)
                    if b_n is None:
                        continue
                    # TODO(leung):项目分类用作了招投标结果
                    relationships.append(
                        TakePartIn(
                            etp_n, b_n, **dict(b, **{'RESULT': b_n['TYPE']})
                        ).get_relationship()
                    )
                pass
            if '抽查检查' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['抽查检查'])
                cs = Check.create_from_dict(data)
                for c in cs:
                    _ = c.pop('check')
                    n = self.get_neo_node(_)
                    if n is None:
                        continue
                    relationships.append(
                        Have(
                            etp_n, n, **dict(c, **{'RESULT': n['RESULT']})
                        ).get_relationship()
                    )
                pass
            if '双随机抽查' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['双随机抽查'])
                rcs = RandomCheck.create_from_dict(data)
                # rcs_n = self.get_neo_node(rcs)
                for rc in rcs:
                    # TODO(leung):随机抽查没有结果
                    _ = rc.pop('check')
                    n = self.get_neo_node(_)
                    if n is None:
                        continue
                    relationships.append(
                        Have(
                            etp_n, n, **rc
                        ).get_relationship()
                    )
                pass
            if '税务信用' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['税务信用'])
                ts = TaxCredit.create_from_dict(data)
                # ts_n = self.get_neo_node(ts)
                for t in ts:
                    _ = t.pop('TaxCredit')
                    n = self.get_neo_node(_)
                    if n is None:
                        continue
                    # TODO(leung):纳税信用等级作为税务信用评级结果
                    relationships.append(
                        Have(
                            etp_n, n, **dict(RESULT=n['GRADE'], **t)
                        ).get_relationship()
                    )
                pass
            if '进出口信用' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['进出口信用'])
                ies = IAE.create_from_dict(data)
                # ies_n = self.get_neo_node(ies)
                for ie in ies:
                    _ = ie.pop('iae')
                    n = self.get_neo_node(_)
                    if n is None:
                        continue
                    relationships.append(
                        Have(
                            etp_n, n, **ie
                        ).get_relationship()
                    )
                pass
            if '招聘' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['招聘'])
                rs = Position.create_from_dict(data)
                for r in rs:
                    _ = r.pop('position')
                    n = self.get_neo_node(_)
                    if n is None:
                        continue
                    relationships.append(
                        Recruit(etp_n, n, **r).get_relationship()
                    )
                pass
            if '客户' in o['content'].keys():
                data = self.get_format_dict(
                    o['content']['客户'])
                cs = Client.create_from_dict(data)
                for c in cs:
                    _ = c.pop('client')
                    n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            _['URL'], _['NAME'])
                    )
                    if n is None:
                        n = self.get_neo_node(_)
                        if n is None:
                            continue
                    relationships.append(
                        SellTo(etp_n, n, **c).get_relationship()
                    )
                pass
            if '供应商' in o['content'].keys():
                data = self.get_format_dict(o['content']['供应商'])
                ss = Supplier.create_from_dict(data)
                for s in ss:
                    _ = s.pop('supplier')
                    n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            _['URL'], _['NAME'])
                    )
                    if n is None:
                        n = self.get_neo_node(_)
                        if n is None:
                            continue
                    relationships.append(
                        Purchase(etp_n, n, **s).get_relationship()
                    )
                pass
            if '信用评级' in o['content'].keys():
                data = self.get_format_dict(o['content']['信用评级'])
                for d in data:
                    _ = d.pop('评级公司')
                    n = self.match_node(
                        *legal,
                        cypher='_.URL = "{}" OR _.NAME = "{}"'.format(
                            _['链接'], _['名称'])
                    )
                    if n is None:
                        _ = Related()
                        _['NAME'] = o['name']
                        _['URL'] = o['url']
                        n = self.get_neo_node(_)
                        if n is None:
                            continue
                    __ = d.pop('内容')
                    d['评级内容'] = __['内容']
                    d['评级链接'] = __['链接']
                    relationships.append(
                        Appraise(n, etp_n, **d).get_relationship()
                    )
                pass
            if '土地转让' in o['content'].keys():
                data = self.get_format_dict(o['content']['土地转让'])
                for d in data:
                    e1 = d.pop('原土地使用权人')
                    e2 = d.pop('现有土地使用权人')
                    p = Plot(**d)
                    p_n = self.get_neo_node(p)
                    if p_n is None:
                        continue
                    if e1['名称'] == o['name'] or e1['链接'] == o['url']:
                        n1 = etp_n
                    else:
                        # 有可能是人
                        n1 = self.match_node(
                            *legal,
                            cypher='_.URL = "{}"'.format(
                                e1['链接'])
                        )
                        if n1 is None:
                            n1 = Related(**e1)
                            n1 = self.get_neo_node(n1)
                    if n1 is not None:
                        relationships.append(
                            Sell(n1, p_n).get_relationship()
                        )
                    if e2['名称'] == o['name'] or e2['链接'] == o['url']:
                        n2 = etp_n
                    else:
                        n2 = self.match_node(
                            *legal,
                            cypher='_.URL = "{}"'.format(
                                e2['链接'])
                        )
                        if n2 is None:
                            n2 = Related(**e2)
                            n2 = self.get_neo_node(n2)
                    if n2 is not None:
                        relationships.append(
                            Buy(n2, p_n).get_relationship()
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
