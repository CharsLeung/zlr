# encoding: utf-8

"""
project = 'Spider'
file_name = 't1'
author = 'Administrator'
datetime = '2020-03-17 11:14'
IDE = PyCharm
"""

from pyecharts.charts import Graph
from pyecharts.options import GraphNode
from data.basemodel import read_json
from entity.baseinfo import BaseInfo

# js = read_json('D:\SYR\\20200301_public\demo3.json')
# bi = BaseInfo(js[7])
# # n1 = bi.get_echarts_node()
# # n1 = GraphNode(name='A', category=1, symbol_size=10)
# # n2 = GraphNode(name='B', category=2, symbol_size=10)
# n1 = {'name': 'A', 'symbolSize': 10, 'value': {'s': 1, 'm': 2}}
# n2 = {'name': 'B', 'symbolSize': 10}
#
# g1 = Graph()
# g1.add(
#     series_name='',
#     nodes=[n1, n2],
#     links=[{'source': n1.get('name'), 'target': n2.get('name')}],
#     repulsion=8000
# ).set_global_opts()
# g1.render('ss.html')

# from pyecharts import options as opts
# from pyecharts.charts import Graph
#
# nodes = [
#     {"name": "结点1", "symbolSize": 10},
#     {"name": "结点2", "symbolSize": 20},
#     {"name": "结点3", "symbolSize": 30},
#     {"name": "结点4", "symbolSize": 40},
#     {"name": "结点5", "symbolSize": 50},
#     {"name": "结点6", "symbolSize": 40},
#     {"name": "结点7", "symbolSize": 30},
#     {"name": "结点8", "symbolSize": 20},
# ]
# links = []
# for i in nodes:
#     for j in nodes:
#         links.append({"source": i.get("name"), "target": j.get("name")})
# c = (
#     Graph()
#     .add("", nodes, links, repulsion=8000)
#     .set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
#     .render("graph_base.html")
# )
from utils import File

fs = File.get_all_file('D:\SYR\\20200220\\20200211\\')
fs = fs[:100]
for p in fs:
    js = read_json(p)
    for d in js:
        if d['metaModel'] == '基本信息':
            bi = BaseInfo(d)
            # n1 = bi.get_neo_node()
            # n2 = bi.get_legal_representative().get_neo_node()
            pass



