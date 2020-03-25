# encoding: utf-8

"""
project = 'zlr'
file_name = '__init__.py'
author = 'Administrator'
datetime = '2020-03-23 11:09'
IDE = PyCharm
"""
from os.path import abspath, dirname

project_dir = dirname(dirname(abspath(__file__)))

workspace = 'D:\graph_data\\'
desktop = 'C:\\Users\Administrator\Desktop\\'


from Graph.base_graph import BaseGraph
