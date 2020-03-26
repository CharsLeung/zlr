# encoding: utf-8

"""
project = 'zlr'
file_name = 'base_graph'
author = 'Administrator'
datetime = '2020/3/24 0024 下午 14:28'
from = 'office desktop' 
"""
import pandas as pd
import datetime as dt
from py2neo import Graph, NodeMatcher, RelationshipMatcher


class BaseGraph:

    def __init__(self, db_uri='http://localhost:7474',
                 username='neo4j', password='12345'
                 ):
        self.graph = Graph(db_uri, username=username, password=password)
        self.NodeMatcher = NodeMatcher(self.graph)
        self.RelationshipMatcher = RelationshipMatcher(self.graph)
        self.logs = []
        pass

    def to_logs(self, info, tp='LOG', name=''):
        self.logs.append({
            'datetime': dt.datetime.now(),
            'info': info,
            'type': tp,
            'name': name
        })

    def save_logs(self, path):
        logs = pd.DataFrame(self.logs)
        logs.to_csv(path, index=False)

