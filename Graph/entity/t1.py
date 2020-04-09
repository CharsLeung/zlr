# encoding: utf-8

"""
project = 'Spider'
file_name = 't1'
author = 'Administrator'
datetime = '2020-03-17 11:14'
IDE = PyCharm
"""
import re


_ = 'https://www.qichacha.com/firm_5e08be8bbd063743652e9280f75a04ac.html'
d = re.search('/[a-zA-Z_]+_\w{32}', _).group(0)
print(d)

