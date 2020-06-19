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
log_save_dir = r'D:\neo4j-community-3.5.14\import\\'


def runEtpGraph():
    gp = EtpGraph(log_save_path=log_save_dir + 'EtpGraph_log.txt')

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
    pass


# runEtpGraph()


def runOptGraph():
    og = OptGraph(log_save_path=log_save_dir + 'OptGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = og.get_all_nodes_and_relationships(
            import_path, mode='a')
        # og.save_graph(import_path, nodes, rps, 'append')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runOptGraph()


def runOptRiskGraph():
    gp = OptRiskGraph(log_save_path=log_save_dir + 'OptRiskGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runOptRiskGraph()


def runDvpGraph():
    gp = DvpGraph(log_save_path=log_save_dir + 'DvpGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runDvpGraph()


def runRightsGraph():
    gp = RightsGraph(log_save_path=log_save_dir + 'RightsGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runRightsGraph()


def runJusGraph():
    gp = JusGraph(log_save_path=log_save_dir + 'JusGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runJusGraph()


def runNewsGraph():
    gp = NewsGraph(log_save_path=log_save_dir + 'NewsGraph_log.txt')

    def getNodesAndRelations():
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a')
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


# runNewsGraph()


def runIdsGraph():
    gp = IndGraph()

    def getNodesAndRelations():
        etps = pd.read_csv(
            r'D:\neo4j-community-3.5.14\import\图数据\EtpGraph\nodes\Enterprise.csv',
            header=None,
            usecols=[10, 26]
        )
        etps = etps.rename(columns=dict(zip(list(etps.columns), ['name', 'url'])))
        etps.drop_duplicates(subset=['url'], inplace=True)
        # etps = etps.head(100000)
        etps = etps.to_dict('record')
        nodes, rps = gp.get_all_nodes_and_relationships(
            import_path, mode='a', enterprises=etps)
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    pass


runIdsGraph()


def f3():
    jtg = JusRulingTextGraph()
    jtg.create_all_relationship()
    pass


# f3()

def drop_duplicates_rps():
    from Graph.relationship import Principal

    pp = Principal()
    data = pp.read_csv(
        r'D:\neo4j-community-3.5.14\import\图数据\EtpGraph\relationships\Person_PRINCIPAL_Enterprise.csv',
        r'D:\neo4j-community-3.5.14\import\图数据\EtpGraph\relationships\Person_PRINCIPAL_Enterprise_Header.csv'
    )
    data = pp.drop_duplicates(data)
    data = {'Person_PRINCIPAL_Enterprise': data}
    # pp.to_csv(data, folder=r'D:\neo4j-community-3.5.14\import\图数据\EtpGraph', split_header=True)
    pass


# drop_duplicates_rps()


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
        # etp_data.drop(['exist'], axis=1)
        etp.to_csv(etp_data, import_path, split_header=True)
        pass

    # func1()

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

    func2()
    pass


# check()


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
                print(p[len(import_path):])
    for np in n_fps:
        if 'Header' in np:
            print(np[len(import_path):])
            # dst = np.replace(import_path, 'D:\G')
            # File.move_file(np, )
    print('-' * 60)
    for np in n_fps:
        if 'Header' not in np:
            print(np[len(import_path):])
    print('-'*60)
    for rp in r_fps:
        if 'Header' in rp:
            print(rp[len(import_path):])
    print('-' * 60)
    for rp in r_fps:
        if 'Header' not in rp:
            print(rp[len(import_path):])
    pass


# getImportCSV()


def mapping():
    ns = pd.read_excel(r'D:\neo4j-community-3.5.14\import\neo4j-admin-import.xlsx',
                       sheet_name='实体')
    mis = []
    for i, r in ns.iterrows():
        if r['头文件路径'].replace('_Header', '') != r['数据文件路径']:
            print('error')
            print(r['数据文件路径'])
            mis.append(r['数据文件路径'])
    rs = pd.read_excel(r'D:\neo4j-community-3.5.14\import\neo4j-admin-import.xlsx',
                       sheet_name='关系')
    for i, r in rs.iterrows():
        if r['头文件路径'].replace('_Header', '') != r['数据文件路径']:
            print('error')
            print(r['数据文件路径'])
            mis.append(r['数据文件路径'])
    if len(mis):
        return

    for i, r in ns.iterrows():
        File.copy_file(import_path + r['头文件路径'], r['头文件映射路径'])
        File.copy_file(import_path + r['数据文件路径'], r['数据文件映射路径'])
        pass

    for i, r in rs.iterrows():
        File.copy_file(import_path + r['头文件路径'], r['头文件映射路径'])
        File.copy_file(import_path + r['数据文件路径'], r['数据文件映射路径'])
        pass
    pass


# mapping()