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
        self.base = BaseModel(tn='qcc_cq_new')
        pass

    def create_nodes_from_website(self, website):
        """
        创建知识产权下的网站节点对象，website参数是Website类的
        实例。
        1.网站
        :param website:
        :return:
        """
        nodes = []
        if len(website):
            for wb in website:
                wb_n = wb.get_neo_node(primarykey=wb.primarykey)
                if wb_n is None:
                    self.to_logs('filed initialize website Neo node',
                                 'ERROR')
                else:
                    nodes.append(wb_n)
        return nodes

    def create_nodes_from_certificate(self, ctf):
        """
        创建知识产权下的证书节点对象，ctf参数是Certificate类的
        实例。
        1.证书
        :param ctf:
        :return:
        """
        nodes = []
        if len(ctf):
            for _ in ctf:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize certificate Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_patent(self, patent):
        """
        创建知识产权下的证书专利对象，patent参数是patent类的
        实例。
        1.证书
        :param patent:
        :return:
        """
        nodes = []
        if len(patent):
            for _ in patent:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize patent Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_trademark(self, trademark):
        """
        创建知识产权下的商标节点对象，trademark参数是Trademark类的
        实例。
        1.商标
        :param trademark:
        :return:
        """
        nodes = []
        if len(trademark):
            for _ in trademark:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize trademark Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_softcopyright(self, softcopyright):
        """
        创建知识产权下的软件著作权节点对象，softcopyright参数是Softcopyright类的
        实例。
        1.软件著作权
        :param softcopyright:
        :return:
        """
        nodes = []
        if len(softcopyright):
            for _ in softcopyright:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize softcopyright Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_workcopyright(self, workcopyright):
        """
        创建知识产权下的软件著作权节点对象，workcopyright参数是workcopyright类的
        实例。
        1.作品著作权
        :param workcopyright:
        :return:
        """
        nodes = []
        if len(workcopyright):
            for _ in workcopyright:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize workcopyright Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_weibo(self, weibo):
        """
        创建知识产权下的微博节点对象，weibo参数是weibo类的
        实例。
        1.微博
        :param weibo:
        :return:
        """
        nodes = []
        if len(weibo):
            for _ in weibo:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize weibo Neo node',
                                 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_official_account(self, official_account):
        """
        创建知识产权下的微信公众号节点对象，official_account参数是
        OfficialAccount类的实例。
        1.微信公众号
        :param official_account:
        :return:
        """
        nodes = []
        if len(official_account):
            for _ in official_account:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize official_account'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_applets(self, applets):
        """
        创建知识产权下的小程序节点对象，applets参数是
        applets类的实例。
        1.小程序
        :param applets:
        :return:
        """
        nodes = []
        if len(applets):
            for _ in applets:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize applets'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_nodes_from_app(self, app):
        """
        创建知识产权下的小程序节点对象，app参数是
        app类的实例。
        1.程序
        :param app:
        :return:
        """
        nodes = []
        if len(app):
            for _ in app:
                _n = _.get_neo_node(primarykey=_.primarykey)
                if _n is None:
                    self.to_logs('filed initialize app'
                                 ' Neo node', 'ERROR')
                else:
                    nodes.append(_n)
        return nodes

    def create_all_relationship(self):
        """
        1.enterprise -[have]->x
        :return:
        """
        rts = self.base.query(
            sql={'metaModel': '知识产权'},
            no_cursor_timeout=True)
        i, k = 0, 0
        eg = EtpGraph()
        etp = Enterprise()
        etp_count = rts.count()
        relationships = []
        for r in rts:
            k += 1
            # if k < 43500:
            #     continue
            etp_n = self.NodeMatcher.match(
                etp.label,
                NAME=r['name']  # TODO(leung): 这里要注意，基本信息以外的模块中的url确定不了公司
            ).first()
            if etp_n is None:
                # 如果这个公司还没在数据库里面，那么应该创建这个公司
                _ = self.base.query_one(
                    sql={'metaModel': '基本信息', 'name': r['name']}
                )
                if _ is not None:
                    etp = Enterprise(_)
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    # 虽然在创建司法关系的时候会创建未在库中的企业，但不会创建
                    # 这个企业的基本关系，因此需要添加其基本关系
                    relationships += eg.create_relationship_from_enterprise_baseinfo(_)
                    pass
                else:
                    # 没有这个公司的信息，那就创建一个信息不全的公司
                    etp = Enterprise(**{'名称': r['name']})
                    etp_n = etp.get_neo_node(primarykey=etp.primarykey)
                    pass
                pass
            if '网站信息' in r['content'].keys():
                web_info = r['content']['网站信息']
                webs = Website.create_from_dict(web_info)
                webs_n = self.create_nodes_from_website(webs)
                for wb_n in webs_n:
                    relationships.append(
                        Have(etp_n, wb_n).get_relationship()
                    )
                pass
            if '证书信息' in r['content'].keys():
                ctf_info = r['content']['证书信息']
                ctfs = Certificate.create_from_dict(ctf_info)
                ctfs_n = self.create_nodes_from_certificate(ctfs)
                for ctf_n in ctfs_n:
                    relationships.append(
                        Have(etp_n, ctf_n).get_relationship()
                    )
                pass
            if '专利信息' in r['content'].keys():
                pat_info = r['content']['专利信息']
                pats = Patent.create_from_dict(pat_info)
                pats_n = self.create_nodes_from_patent(pats)
                for pat_n in pats_n:
                    relationships.append(
                        Have(etp_n, pat_n).get_relationship()
                    )
                pass
            if '商标信息' in r['content'].keys():
                tm_info = r['content']['商标信息']
                tms = Trademark.create_from_dict(tm_info)
                tms_n = self.create_nodes_from_trademark(tms)
                for tm_n in tms_n:
                    relationships.append(
                        Have(etp_n, tm_n).get_relationship()
                    )
                pass
            if '软件著作权' in r['content'].keys():
                scr_info = r['content']['软件著作权']
                scrs = SoftCopyRight.create_from_dict(scr_info)
                scrs_n = self.create_nodes_from_softcopyright(scrs)
                for scr_n in scrs_n:
                    relationships.append(
                        Have(etp_n, scr_n).get_relationship()
                    )
                pass
            if '作品著作权' in r['content'].keys():
                wcr_info = r['content']['作品著作权']
                wcrs = WorkCopyRight.create_from_dict(wcr_info)
                wcrs_n = self.create_nodes_from_workcopyright(wcrs)
                for wcr_n in wcrs_n:
                    relationships.append(
                        Have(etp_n, wcr_n).get_relationship()
                    )
                pass
            if '微博' in r['content'].keys():
                wb_info = r['content']['微博']
                wbs = Weibo.create_from_dict(wb_info)
                wbs_n = self.create_nodes_from_weibo(wbs)
                for wb_n in wbs_n:
                    relationships.append(
                        Have(etp_n, wb_n).get_relationship()
                    )
                pass
            if '微信公众号' in r['content'].keys():
                oa_info = r['content']['微信公众号']
                oas = OfficialAccount.create_from_dict(oa_info)
                oas_n = self.create_nodes_from_official_account(oas)
                for oa_n in oas_n:
                    relationships.append(
                        Have(etp_n, oa_n).get_relationship()
                    )
                pass
            if '小程序' in r['content'].keys():
                alt_info = r['content']['小程序']
                alts = Applets.create_from_dict(alt_info)
                alts_n = self.create_nodes_from_applets(alts)
                for alt_n in alts_n:
                    relationships.append(
                        Have(etp_n, alt_n).get_relationship()
                    )
                pass
            if 'APP' in r['content'].keys():
                aps_info = r['content']['APP']
                aps = App.create_from_dict(aps_info)
                aps_n = self.create_nodes_from_applets(aps)
                for ap_n in aps_n:
                    relationships.append(
                        Have(etp_n, ap_n).get_relationship()
                    )
                pass
            if len(relationships) > 1000:
                i += 1
                # self.graph_merge_relationships(relationships)
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                return
        if len(relationships):
            i += 1
            # self.graph_merge_relationships(relationships)
            print(SuccessMessage('{}:success merge relationships to database '
                                 'round {} and deal {}/{} enterprise,and'
                                 ' merge {} relationships.'.format(
                dt.datetime.now(), i, k, etp_count, len(relationships)
            )))
            relationships.clear()
            pass


rg = RightsGraph()
rg.create_all_relationship()