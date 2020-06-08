# encoding: utf-8

"""
project = zlr
file_name = graph_run
author = Administrator
datetime = 2020/3/27 0027 下午 14:03
from = office desktop
"""
import pandas as pd

from Calf.utils import File
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


# def getEntityUniqueCodeSYX(data, flag):
#     data['URL'] = data.URL.map(
#         lambda x: BaseEntity.getEntityUniqueCodeSYX(x, flag))
#     return data
#
#
# prs = pd.read_csv('D:\graph_data\图数据\基本信息\实体\Person.csv', engine='python', encoding='utf-8')
# prs = getEntityUniqueCodeSYX(prs, 'prs')
import_path = r'D:\neo4j-community-3.5.14\import'


def runEtpGraph():
    eg = EtpGraph()
    # eg.create_index_and_constraint()
    # eg.create_all_nodes()
    # eg.create_all_relationship()

    def getNodes():
        save_path = '图数据\基本信息\实体\\'
        File.check_file(save_path)
        nodes = eg.get_all_nodes()
        cp = []

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)

            # cp.append('// create {} nodes.\n'.format(k))
            # cp.append('USING PERIODIC COMMIT\n')
            # cp.append('LOAD CSV WITH HEADERS FROM "file:///{}{}.csv" AS ROW\n'.format(
            #     '\\\\'.join(save_path.split('\\')), k
            # ))
            # columns = list(_nds_.columns)
            # # columns.remove('label')
            # _cp_ = ['{}: ROW.{}'.format(col, col) for col in columns]
            # cp.append('CREATE (:{}'.format(k) + '{' + ', '.join(_cp_) + '});\n')
            # cp.append('\n\n')
            pass

        # with open(import_path + save_path + 'cyphers.txt', 'w+',
        #           encoding='utf-8') as f:
        #     f.writelines(cp)

        pass

    def getRelations():
        save_path = '图数据\基本信息\关系\\'
        File.check_file(save_path)
        rps = eg.get_all_relationships()

        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
        pass

    # getNodes()
    getRelations()

    if len(eg.logs):
        eg.save_logs('D:\graph_data\graph_run_logs_for_enterprise.csv')
    pass


# runEtpGraph()


def runOptGraph():
    og = OptGraph()

    def getNodesAndRelations():
        save_path = '\图数据\经营状况\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\经营状况\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_og.csv')
    pass


# runOptGraph()


def runOptRiskGraph():
    og = OptRiskGraph()

    def getNodesAndRelations():
        save_path = '\图数据\经营风险\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\经营风险\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_org.csv')
    pass


# runOptRiskGraph()


def runDvpGraph():
    og = DvpGraph()

    def getNodesAndRelations():
        save_path = '\图数据\企业发展\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\企业发展\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_dvp.csv')
    pass


# runDvpGraph()


def runRightsGraph():
    og = RightsGraph()

    def getNodesAndRelations():
        save_path = '\图数据\知识产权\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\知识产权\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_rights.csv')
    pass


# runRightsGraph()


def runJusGraph():
    og = JusGraph()

    def getNodesAndRelations():
        save_path = '\图数据\知识产权\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\知识产权\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_justice.csv')
    pass


# runJusGraph()


def runNewsGraph():
    og = NewsGraph()

    def getNodesAndRelations():
        save_path = '\图数据\知识产权\实体\\'
        File.check_file(import_path + save_path)
        nodes, rps = og.get_all_nodes_and_relationships()

        for k, v in zip(nodes.keys(), nodes.values()):
            primarykey = entities(k).primarykey
            _nds_ = pd.DataFrame(v)
            _nds_.dropna(subset=[primarykey], inplace=True)
            _nds_.drop_duplicates(subset=[primarykey], inplace=True)
            _nds_ = entities(k).getImportCSV(_nds_)
            _nds_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        save_path = '\图数据\知识产权\关系\\'
        File.check_file(import_path + save_path)
        for k, v in zip(rps.keys(), rps.values()):
            _rps_ = pd.DataFrame(v)
            _rps_.dropna(subset=['from', 'to'], inplace=True)
            _rps_ = relationships(k).getImportCSV(_rps_)
            _rps_.to_csv(import_path + save_path + '{}.csv'.format(k), index=False)
            pass
        pass

    getNodesAndRelations()
    # og.create_all_relationship()
    if len(og.logs):
        og.save_logs('D:\graph_data\graph_run_logs_for_news.csv')
    pass


runNewsGraph()


def f3():
    jtg = JusRulingTextGraph()
    jtg.create_all_relationship()
    if len(jtg.logs):
        jtg.save_logs('D:\graph_data\graph_run_logs_for_justice_text.csv')
    pass


# f3()


