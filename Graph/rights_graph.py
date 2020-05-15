# encoding: utf-8

"""
project = zlr
file_name = rights_graph
author = Administrator
datetime = 2020/4/3 0003 上午 10:27
from = office desktop
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import entities, legal, Related
from Graph.entity import Enterprise
from Graph.entity import Website, Certificate
from Graph.entity import Patent, Trademark, App
from Graph.entity import WorkCopyRight, SoftCopyRight
from Graph.entity import Weibo, OfficialAccount, Applets
from Graph.exception import SuccessMessage
from Graph.relationship import Have
from Graph.enterprise_graph import EtpGraph


class RightsGraph(BaseGraph):

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
        不必再单独创建索引
        :return:
        """
        # 用到是实体对象
        used_entity = [
            'Website',
            'Certificate',
            'Patent',
            'Trademark',
            'App',
            'WorkCopyRight',
            'SoftCopyRight',
            'Weibo',
            'OfficialAccount',
            'Applets',
        ]
        constraint = {}
        index = {}
        for l in used_entity:
            constraint[l] = [entities(l).primarykey]
            # idx = entities(l).index
            # if len(idx):
            #     index[l] = idx
        self.add_index_and_constraint(index, constraint)
        pass

    def create_all_relationship(self):
        """
        1.enterprise -[have]->x
        :return:
        """
        rts = self.base.query(
            sql={'metaModel': '知识产权'},
            limit=100,
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        # etp = Enterprise()
        etp_count = rts.count()
        relationships = []
        for r in rts:
            k += 1
            # if k < 43500:
            #     continue
            # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            etp_n = self.match_node(
                *legal,
                cypher='_.NAME = "{}"'.format(r['name'])
            )
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': r['name']}
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
                    etp = Related()
                    etp['NAME'] = r['name']
                    etp['URL'] = r['url']
                    etp_n = self.get_neo_node(etp)
                    pass
                pass

            if '网站信息' in r['content'].keys():
                data = self.get_format_dict(r['content']['网站信息'])
                webs = Website.create_from_dict(data)
                for web in webs:
                    w = web.pop('website')
                    w_n = self.get_neo_node(w)
                    if w_n is not None:
                        relationships.append(
                            Have(etp_n, w_n, **web).get_relationship()
                        )
                pass

            if '证书信息' in r['content'].keys():
                data = self.get_format_dict(r['content']['证书信息'])
                ctfs = Certificate.create_from_dict(data)
                for ctf in ctfs:
                    c = ctf.pop('certificate')
                    c_n = self.get_neo_node(c)
                    if c_n is not None:
                        relationships.append(
                            Have(etp_n, c_n, **ctf).get_relationship()
                        )
                pass

            if '专利信息' in r['content'].keys():
                data = self.get_format_dict(r['content']['专利信息'])
                pats = Patent.create_from_dict(data)
                for pat in pats:
                    p = pat.pop('patent')
                    p_n = self.get_neo_node(p)
                    if p_n is not None:
                        relationships.append(
                            Have(etp_n, p_n, **pat).get_relationship()
                        )
                pass

            if '商标信息' in r['content'].keys():
                data = self.get_format_dict(r['content']['商标信息'])
                tms = Trademark.create_from_dict(data)
                for tm in tms:
                    t = tm.pop('trademark')
                    t_n = self.get_neo_node(t)
                    if t_n is not None:
                        relationships.append(
                            Have(etp_n, t_n, **tm).get_relationship()
                        )
                pass

            if '软件著作权' in r['content'].keys():
                data = self.get_format_dict(r['content']['软件著作权'])
                scrs = SoftCopyRight.create_from_dict(data)
                for scr in scrs:
                    s = scr.pop('softcopyright')
                    s_n = self.get_neo_node(s)
                    if s_n is not None:
                        relationships.append(
                            Have(etp_n, s_n, **scr).get_relationship()
                        )
                pass

            if '作品著作权' in r['content'].keys():
                data = self.get_format_dict(r['content']['作品著作权'])
                wcrs = WorkCopyRight.create_from_dict(data)
                for wcr in wcrs:
                    w = wcr.pop('workcopyright')
                    w_n = self.get_neo_node(w)
                    if w_n is not None:
                        relationships.append(
                            Have(etp_n, w_n, **wcr).get_relationship()
                        )
                pass

            if '微博' in r['content'].keys():
                data = self.get_format_dict(r['content']['微博'])
                wbs = Weibo.create_from_dict(data)
                for wb in wbs:
                    w = wb.pop('weibo')
                    w_n = self.get_neo_node(w)
                    if w_n is not None:
                        relationships.append(
                            Have(etp_n, w_n, **wb).get_relationship()
                        )
                pass

            if '微信公众号' in r['content'].keys():
                data = self.get_format_dict(r['content']['微信公众号'])
                oas = OfficialAccount.create_from_dict(data)
                for oa in oas:
                    woa = oa.pop('WeChat')
                    woa_n = self.get_neo_node(woa)
                    if woa_n is not None:
                        relationships.append(
                            Have(etp_n, woa_n, **oa).get_relationship()
                        )
                pass

            if '小程序' in r['content'].keys():
                data = self.get_format_dict(r['content']['小程序'])
                alts = Applets.create_from_dict(data)
                for alt in alts:
                    a = alt.pop('applets')
                    a_n = self.get_neo_node(a)
                    if a_n is not None:
                        relationships.append(
                            Have(etp_n, a_n, **alt).get_relationship()
                        )
                pass

            if 'APP' in r['content'].keys():
                data = self.get_format_dict(r['content']['APP'])
                aps = App.create_from_dict(data)
                for ap in aps:
                    a = ap.pop('app')
                    a_n = self.get_neo_node(a)
                    if a_n is not None:
                        relationships.append(
                            Have(etp_n, a_n, **ap).get_relationship()
                        )
                pass
            if len(relationships) > 1000:
                i += 1
                self.graph_merge_relationships(relationships)
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                return
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


# rg = RightsGraph()
# rg.create_all_relationship()