# encoding: utf-8

"""
project = zlr
file_name = graph_run
author = Administrator
datetime = 2020/3/27 0027 下午 14:03
from = office desktop
"""
import os
import pandas as pd

from Calf.utils import File, progress_bar
from Graph.entity import entities, BaseEntity
from Graph.relationship import relationships
from Graph.enterprise_graph import EtpGraph
from Graph.justice_graph import JusGraph
from Graph.justice_rulingtext_graph import JusRulingTextGraph
from Graph.operating_risk_graph import OptRiskGraph
from Graph.operating_graph import OptGraph
from Graph.news_graph import NewsGraph
from Graph.develop_graph import DvpGraph
from Graph.rights_graph import RightsGraph
from Graph.industry_graph import IndGraph

# def getEntityUniqueCodeSYX(data, flag):
#     data['URL'] = data.URL.map(
#         lambda x: BaseEntity.getEntityUniqueCodeSYX(x, flag))
#     return data
#
#
# prs = pd.read_csv('D:\graph_data\图数据\基本信息\实体\Person.csv', engine='python', encoding='utf-8')
# prs = getEntityUniqueCodeSYX(prs, 'prs')
import_path = r'D:\neo4j-community-3.5.14\import\图数据'


def runEtpGraph():
    gp = EtpGraph()

    # eg.create_index_and_constraint()
    # eg.create_all_nodes()
    # eg.create_all_relationship()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    # getNodes()
    # getRelations()
    getNodesAndRelations()

    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_enterprise.csv')
    pass


# runEtpGraph()


def runOptGraph():
    og = OptGraph()

    def getNodesAndRelations():
        nodes, rps = og.get_all_nodes_and_relationships(
            import_path, mode='a')
        # og.save_graph(import_path, nodes, rps, 'append')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_og.csv')
    pass


# runOptGraph()


def runOptRiskGraph():
    gp = OptRiskGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_org.csv')
    pass


# runOptRiskGraph()


def runDvpGraph():
    gp = DvpGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_dvp.csv')
    pass


# runDvpGraph()


def runRightsGraph():
    gp = RightsGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_rights.csv')
    pass


# runRightsGraph()


def runJusGraph():
    gp = JusGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_justice.csv')
    pass


# runJusGraph()


def runNewsGraph():
    gp = NewsGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_news.csv')
    pass


# runNewsGraph()


def runIdsGraph():
    gp = IndGraph()

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(gp.logs):
        gp.save_logs('D:\graph_data\graph_run_logs_for_ids.csv')
    pass


# runIdsGraph()


def f3():
    jtg = JusRulingTextGraph()
    jtg.create_all_relationship()
    if len(jtg.logs):
        jtg.save_logs('D:\graph_data\graph_run_logs_for_justice_text.csv')
    pass


# f3()


def check():
    fps = File.get_all_file(import_path)
    n_fps = []
    r_fps = []
    for p in fps:
        if 'nodes' in p:
            n_fps.append(p)
        if 'relationships':
            r_fps.append(p)
        pass

    from Calf.data import BaseModel
    base = BaseModel(
        tn='cq_all',
        # tn='qcc.1.1',
        # location='gcxy',
        # dbname='data'
    )

    def func1():
        # 处理非基本信息模块下的Enterprise
        etp_fps = []
        for p in n_fps:
            if 'Enterprise' in p and 'EtpGraph' not in p:
                etp_fps.append(p)
        etp_fps = set([os.path.join(*p.split('\\')[:-1]) for p in etp_fps])
        etp = entities('Enterprise')
        etp_data = []
        for ep in etp_fps:
            ed = etp.read_csv(ep, ep)
            etp_data.append(ed)
        etp_data = pd.concat(etp_data)
        etp_data.drop_duplicates(['URL:ID(Enterprise)'], inplace=True)
        etp_data.reset_index(drop=True, inplace=True)
        total = len(etp_data)

        etp_data['exist'] = False
        for i, r in etp_data.iterrows():
            try:
                _ = base.query_one(sql={'name': r['NAME'], 'metaModel': '基本信息'},
                                   field={'name': 1, '_id': 0})
                if _ is not None:
                    etp_data.loc[i, ['exist']] = True
                if i % 100 == 0:
                    progress_bar(total, i, 'check')
            except Exception as e:
                print(e)
        etp_data = etp_data[~etp_data['exist']]
        etp_data.drop(['exist'], axis=1)
        etp.to_csv(etp_data, import_path, split_header=True)
        pass

    func1()

    def func2():
        # 处理Related
        rel_fps = []
        for p in n_fps:
            if 'Related' in p:
                rel_fps.append(p)
        rel_fps = set([os.path.join(*p.split('\\')[:-1]) for p in rel_fps])
        rel = entities('Related')
        rel_data = []
        for ep in rel_fps:
            ed = rel.read_csv(ep, ep)
            rel_data.append(ed)
        rel_data = pd.concat(rel_data)
        # rel_data.drop_duplicates(['URL:ID'], inplace=True)

        drop = rel_data.loc[:, ['URL:ID(Related)', 'NAME']]
        drop['count'] = 1
        drop = drop.groupby(['URL:ID(Related)'], as_index=False).agg({
            'count': 'count', 'NAME': 'first'
        })
        drop = drop[(drop['count'] > 3) & (drop['NAME'].str.len() < 4)]
        drop = drop['URL:ID(Related)']
        # drop = drop.tolist()
        if len(drop):
            rel_data = rel_data[~rel_data['URL:ID(Related)'].isin(drop)]
        rel.to_csv(rel_data, import_path, split_header=True)
        pass

    # func2()
    pass


check()


def getImportCSV():
    fps = File.get_all_file(import_path)
    fps = reversed(fps)
    n_fps = []
    r_fps = []

    for p in fps:
        if '.csv' in p:
            if 'nodes' in p:
                n_fps.append(p)
            elif 'relationships' in p:
                r_fps.append(p)
                # File.rename(p, p.replace('(', '_').replace(')', ''))
            else:
                print(p)
    for np in n_fps:
        if 'Header' in np:
            print(np)
            dst = np.replace(import_path, 'D:\G')
            File.move_file(np, )
    print('-' * 60)
    for np in n_fps:
        if 'Header' not in np:
            print(np)
    # print('-'*60)
    # for rp in r_fps:
    #     if 'Header' in rp:
    #         print(rp)
    # print('-' * 60)
    # for rp in r_fps:
    #     if 'Header' not in rp:
    #         print(rp)
    pass


# getImportCSV()


def mapping():
    ns = pd.read_excel(r'D:\neo4j-community-3.5.14\import\neo4j-admin-import.xlsx',
                       sheet_name='实体')
    for i, r in ns.iterrows():
        File.copy_file(r['头文件路径'], r['头文件映射路径'])
        File.copy_file(r['数据文件路径'], r['数据文件映射路径'])
        pass
    rs = pd.read_excel(r'D:\neo4j-community-3.5.14\import\neo4j-admin-import.xlsx',
                       sheet_name='关系')
    for i, r in rs.iterrows():
        File.copy_file(r['头文件路径'], r['头文件映射路径'])
        File.copy_file(r['数据文件路径'], r['数据文件映射路径'])
        pass
    pass


# mapping()