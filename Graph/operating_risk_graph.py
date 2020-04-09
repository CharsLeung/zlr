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
from Graph.entity import Enterprise, Possession
from Graph.exception import SuccessMessage
from Graph.relationship import Guaranty, Have
from Graph.enterprise_graph import EtpGraph


class OptRiskGraph(BaseGraph):

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
            'Punishment': [Punishment.primarykey],
            'Possession': [Possession.primarykey],
            # 'Involveder': ['HASH_ID'],
        }
        index = {
            # 'Enterprise': [('NAME',)]
        }
        self.add_index_and_constraint(index, constraint)
        pass

    def create_relationships_from_punishment(self):
        pass

    def create_all_relationship(self):
        """
        1.enterprise -[have]->punishment
        :return:
        """
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

            if '股权出质' in j['content'].keys():
                sh_info = j['content']['股权出质']
                for sh in sh_info:
                    # 确定出质人
                    del sh['序号']
                    cz = sh.pop('出质人')
                    cz['链接'] = etp.parser_url(cz['链接'])
                    # 判断出质人是不是当前公司
                    if j['name'] == cz['出质人'] or cz['链接'] == etp_n['URL']:
                        cz_n = etp_n
                    else:
                        # 确定出质人，先在企业中找
                        cz_n = self.NodeMatcher.match(etp.label).where(
                            '_.NAME = "{}" OR _.URL = "{}"'.format(
                                cz['出质人'], cz['链接']
                            )
                        ).first()
                        if cz_n is None:
                            # 在企业中没找到，就通过url在所有对象中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            cz_n = self.NodeMatcher.match().where(
                                '_.URL = "{}"'.format(cz['链接'])
                            ).first()
                            if cz_n is None:
                                # 创建这个股权出质人
                                if len(cz['出质人']):
                                    cz_n = Involveder(**{'名称': cz['出质人'],
                                                         '链接': cz['链接']})
                                    cz_n = cz_n.get_neo_node(primarykey=cz_n.primarykey)
                                else:
                                    cz_n = None
                        pass
                    # 确定质权人
                    zq = sh.pop('质权人')
                    zq['链接'] = etp.parser_url(zq['链接'])
                    # 判断质权人是不是当前公司
                    if j['name'] == zq['质权人'] or zq['链接'] == etp_n['URL']:
                        zq_n = etp_n
                    else:
                        # 确定质权人，先在企业中找
                        zq_n = self.NodeMatcher.match(etp.label).where(
                            '_.NAME = "{}" OR _.URL = "{}"'.format(
                                zq['质权人'], zq['链接']
                            )
                        ).first()
                        if zq_n is None:
                            # 在企业中没找到，就通过url在所有对象中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            zq_n = self.NodeMatcher.match().where(
                                '_.URL = "{}"'.format(zq['链接'])
                            ).first()
                            if zq_n is None:
                                # 创建这个股权出质人
                                if len(zq['质权人']):
                                    zq_n = Involveder(**{'名称': zq['质权人'],
                                                         '链接': zq['链接']})
                                    zq_n = zq_n.get_neo_node(primarykey=zq_n.primarykey)
                                else:
                                    zq_n = None
                        pass
                    # 确定出质标的企业
                    bd = sh.pop('出质股权标的企业')
                    bd['链接'] = etp.parser_url(bd['链接'])
                    # 判断出质标的是不是当前公司
                    if j['name'] == bd['企业'] or bd['链接'] == etp_n['URL']:
                        bd_n = etp_n
                    else:
                        # 确定出质标的，先在企业中找
                        bd_n = self.NodeMatcher.match(etp.label).where(
                            '_.NAME = "{}" OR _.URL = "{}"'.format(
                                bd['企业'], bd['链接']
                            )
                        ).first()
                        if bd_n is None:
                            # 在企业中没找到，就通过url在所有对象中找
                            # 这里最好不要通过名称找了，除公司以外出现
                            # 同名的几率很大
                            bd_n = self.NodeMatcher.match().where(
                                '_.URL = "{}"'.format(bd['链接'])
                            ).first()
                            if bd_n is None:
                                # 创建这个出质标的
                                if len(bd['企业']):
                                    bd_n = Possession(**{'名称': bd['企业'],
                                                         '链接': bd['链接']})
                                    bd_n = bd_n.get_neo_node(primarykey=bd_n.primarykey)
                                else:
                                    bd_n = None
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

            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                if i == 1:
                    # 第一轮创建索引
                    self.create_index_and_constraint()
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                return
                pass
        if len(relationships):
            i += 1
            self.graph_merge_relationships(relationships)
            print(SuccessMessage('{}:success merge relationships to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} relationships.'.format(
                dt.datetime.now(), i, k, etp_count, len(relationships)
            )))
            relationships.clear()
            pass


# org = OptRiskGraph()
# org.create_all_relationship()
