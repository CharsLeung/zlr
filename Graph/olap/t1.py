# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = t1
author = Administrator
datetime = 2020/5/15 0015 下午 17:33
from = office desktop
"""
from py2neo import Graph


graph = Graph('http://localhost:7474', username='neo4j', password='12345')


def read_paid_up_capital_amount():
    # 读取注册资本
    cp = 'match (n:Enterprise) return ' \
         'n.PAID_UP_CAPITAL_AMOUNT, ' \
         'n.PAID_UP_CAPITAL_UNIT'
    data = graph.run(cp).to_data_frame()
    # 1.统计有注册资本金的公司所占比例
    r = sum(data.PAID_UP_CAPITAL_AMOUNT > 0) / len(data)
    # 2.统计注册资本金的单位有哪些，便于统一单位
    units = data.PAID_UP_CAPITAL_UNIT.unique().tolist()
    conver = {'万元人民币': 10000, '万日元': 200, '万美元': 70000}
    data.drop('PAID_UP_CAPITAL_AMOUNT', inplace=True)
    data['amount'] = data.apply(
        lambda r: r.PAID_UP_CAPITAL_AMOUNT * conver[
            r.PAID_UP_CAPITAL_UNIT], axis=1
    )
    pass


def investing():
    # 看对外投资的企业的地域分布
    cp = 'MATCH p=(n1:Enterprise)-[r]->(n2:Enterprise) RETURN n2.ADDRESS'