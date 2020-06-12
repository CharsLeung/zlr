# encoding: utf-8

"""
project = 'Spider'
file_name = 't1'
author = 'Administrator'
datetime = '2020-03-17 11:14'
IDE = PyCharm
"""
# import re
import pandas as pd

# _ = 'https://www.qichacha.com/firm_5e08be8bbd063743652e9280f75a04ac.html'
# d = re.search('/[a-zA-Z_]+_\w{32}', _).group(0)
# print(d)
d = pd.DataFrame([{'B': 1, 'C': 1, 'D': 1, 'E': 1}, {'B': 1, 'C': 1, 'D': 1, 'E': 1}])
d.to_csv('tt.csv', index=False, mode='a')
d2 = pd.DataFrame([{'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2}, {'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2}])
d2.to_csv('tt.csv', index=False, mode='a', header=False)
pass
