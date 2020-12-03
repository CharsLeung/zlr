# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = cyphers
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020\6\3 0003 下午 16:10
@from = office desktop
"""
# match (e:Enterprise) where e.NAME=~".*数宜信.*" return e
# MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
# MATCH (e:Enterprise)-[r:HAVE]->(c:Check) delete r
# MATCH (p:Person)-[r]->() where p.URL="https:\\www.qichacha.com" delete p, r
# MATCH (n:Person) where size((n)-[:LEGAL_REPRESENTATIVE]->())>2 return n
# MATCH p=(e1:Enterprise)-[*..20]-(e2:Enterprise) where e1.NAME='重庆市龙井泡沫塑料有限公司' and e2.NAME='重庆玮兰床垫家具有限公司' RETURN p


def create_address():
    """
    USING PERIODIC COMMIT
    LOAD CSV WITH HEADERS FROM "file:\\\图数据\基本信息\实体\Address.csv" AS ROW
    CREATE (:Address {ADDRESS:ROW.ADDRESS});

    neo4j-admin import --database=graph.db --nodes=D:\neo4j-community-3.5.14\import\图数据\基本信息\实体\Person.csv --nodes=D:\neo4j-community-3.5.14\import\图数据\基本信息\实体\Enterprise.csv --relationships=D:\neo4j-community-3.5.14\import\图数据\基本信息\关系\BE_IN_OFFICE.csv --relationships=D:\neo4j-community-3.5.14\import\图数据\基本信息\关系\LEGAL_REP.csv --multiline-fields=true --ignore-duplicate-nodes=true --ignore-missing-nodes=true
    :return:
    """
    pass


def create_constraint():
    from Graph.entity import entities

    cst = {}
    used_entity = entities()
    for et in used_entity.values():
        pk = et.primarykey
        if pk is not None and len(pk):
            print(f"create constraint on (n:{et.label}) assert n.{pk} is unique")
        else:
            print(et.label)
        pass


# create_constraint()


def create_index():
    from Graph.entity import entities

    index = {}
    used_entity = entities()
    for et in used_entity.values():
        idx = et.index
        if len(idx):
            print('create index on: {}({})'.format(et.label, idx[0][0]))

        pass


# create_index()


"""
{
investorName: "重庆正大软件（集团）有限公司"
deep: 4
}
match p=(investor:Enterprise)-[:INVESTING*..4]->(invested:Enterprise) where investor.NAME = "重庆正大软件（集团）有限公司" return p

删除重复的关系，TAIL返回第一个以外的数据
MATCH (a)-[r:PRINCIPAL]->(b:Enterprise)
WITH a, b, TAIL(COLLECT (r)) as rr
WHERE size(rr)>0
FOREACH (r IN rr | DELETE r)

"""