# encoding: utf-8

"""
project = 'zlr'
file_name = 't2'
author = 'Administrator'
datetime = '2020/3/23 0023 下午 14:14'
from = 'office desktop' 
"""
from pyecharts import options as opts
from pyecharts.charts import Graph

nodes = [
    opts.GraphNode(
        name='企业/团体', symbol_size=40,
        # label_opts=opts.LabelOpts(background_color='rgb(123,78, 91)')
    ),
    opts.GraphNode(name='企业2', symbol_size=40),
    opts.GraphNode(name='法人代表', symbol_size=20),
    opts.GraphNode(name='董事长', symbol_size=20),
    opts.GraphNode(name='X地址', symbol_size=15),
    opts.GraphNode(name='一级行业(能源)', symbol_size=20),
    opts.GraphNode(name='二级行业(火力发电)', symbol_size=20),
    opts.GraphNode(name='一级行业(采矿)', symbol_size=20),
    opts.GraphNode(name='二级行业(煤炭发掘)', symbol_size=20),
]

links = [
    opts.GraphLink(source='法人代表', target='企业/团体'),
    opts.GraphLink(source='董事长', target='企业/团体'),
    opts.GraphLink(source='X地址', target='企业/团体'),
    opts.GraphLink(source='X地址', target='企业2'),
    opts.GraphLink(source='企业/团体', target='企业2'),
    opts.GraphLink(source='二级行业(火力发电)', target='一级行业(能源)'),
    opts.GraphLink(source='二级行业(煤炭发掘)', target='一级行业(采矿)'),
    opts.GraphLink(source='二级行业(煤炭发掘)', target='二级行业(火力发电)'),
    opts.GraphLink(source='企业/团体', target='二级行业(火力发电)'),
    opts.GraphLink(source='企业2', target='二级行业(煤炭发掘)'),

]

c = (Graph(init_opts=opts.InitOpts(width='1600px', height='800px')).add(
    series_name='',
    nodes=nodes,
    links=links,
    # layout='none',
    # is_roam=True,
    # is_focusnode=True,
    edge_label=opts.LabelOpts(
        is_show=True, position="middle", formatter="{b}"
    ),
    # label_opts=opts.LabelOpts(is_show=False),
    linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7)
).set_global_opts(
    title_opts=opts.TitleOpts(title="Enterprise Dependencies")
).render('demo.html')
     )

# c = (
#     Graph()
#     .add(
#         "",
#         nodes,
#         links,
#         repulsion=4000,
#         edge_label=opts.LabelOpts(
#             is_show=True, position="middle", formatter="{b} 的数据 {c}"
#         ),
#     )
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
#     )
#     .render("demo.html")
# )

pass
