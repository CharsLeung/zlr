# encoding: utf-8

"""
@project = zlr(20200403备份)

@file_name = settings

@author = liang jian

@email = leungjain@qq.com

@datetime = 2020/11/17 0017 上午 10:40

@from = office desktop
"""
import os

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
Env = "debug"

source_config = {
    "debug": {
        "workspace": {
            # "content": os.path.join(BASE_PATH, "temp", "ContentSession"),
            "logs": os.path.join(BASE_PATH, "temp", "logs"),
            # "index": os.path.join(BASE_PATH, "temp", "index"),
            # "demo": os.path.join(BASE_PATH, "temp", "demo"),
            # "reports": os.path.join(BASE_PATH, "temp", "reports")
        },
        "MONGODB_LOG": {
            # "host": "222.178.152.79",
            # "port": 4316,
            "database_name": "origin",
            "collection": "org_logs",
            # "username": "rwOriginLogs",
            # "password": "DqLSdYKQ*849",
            # "authSource": "admin",

            "host": "192.168.34.126",
            "port": 6123,
            "username": "admin",
            "password": "uWNSnhtS%989",
            "authSource": "admin"
        },
        "neo4j": {
            "uri": "http://localhost:7474",
            "username": "neo4j", 
            "password": "12345"
        }
    }
}
