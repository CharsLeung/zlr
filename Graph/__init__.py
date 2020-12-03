# encoding: utf-8

"""
project = 'zlr'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-23 11:09'
IDE = PyCharm
"""
from Graph.settings import *

config = source_config[Env]
for n, p in zip(config['workspace'].keys(), config['workspace'].values()):
    if not os.path.exists(p):
        os.makedirs(p)

_version_ = '0.1.0'
workspace = config['workspace']
print(f'* Graph({_version_}): start')
print('* Environment:', Env)

from loguru import logger
from Graph.core.mongo_log_handler import getMongoLogHandler

logger.add(
        os.path.join(workspace['logs'], 'Graph.log'),
        level='DEBUG',
        format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {file} - {line} - {message}',
        rotation="10 MB", encoding="utf-8", enqueue=True,
)
try:
    # logger.add(
    #     getMongoLogHandler('Graph', **config['MONGODB_LOG']),
    #     level='DEBUG',
    #     format='{message}',
    # )
    pass
except Exception as e:
    print(e)

workspace = 'D:\graph_data\\'
desktop = 'C:\\Users\Administrator\Desktop\\'


from Graph.base_graph import BaseGraph
from Graph.enterprise_graph import EtpGraph
from Graph.operating_graph import OptGraph
from Graph.operating_risk_graph import OptRiskGraph
from Graph.develop_graph import DvpGraph
from Graph.rights_graph import RightsGraph
from Graph.justice_graph import JusGraph
from Graph.news_graph import NewsGraph


def graphs(name=None):
    gps = {
        'BaseGraph': BaseGraph(),
        'EtpGraph': EtpGraph(),
        'OptGraph': OptGraph(),
        'OptRiskGraph': OptRiskGraph(),
        'DvpGraph': DvpGraph(),
        'RightsGraph': RightsGraph(),
        'JusGraph': JusGraph(),
        'NewsGraph': NewsGraph(),
    }
    if name is not None:
        return gps[name]
    else:
        return gps
