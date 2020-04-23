
# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = base_info
author = Administrator
datetime = 2020/4/20 0020 下午 18:24
from = office desktop
"""
import re
import pandas as pd

from Graph import workspace
from Graph.etl import QccRequest


class Enterprise(QccRequest):

    def __init__(self, ReturnString=None, **kwargs):
        QccRequest.__init__(self, ReturnString)
        if len(self.patterns) == 0:
            self.patterns = self.load_regular_expression('基本信息')
        pass

    def pattern_to_function(self):
        """
        组装针对每个字段目录的函数族
        :return:
        """
        ps = self.load_regular_expression('基本信息').values()
        patterns = []

        def search(x, exp, ):
            _ = re.search(exp, x).group()
            if _ is not None:
                pass

        for p in ps:
            _ = []
            if p[1][0:5] == 'func:':
                # 说明这是一个函数名，调用即可
                _.append(getattr(self, p[1][5:]))
            elif p[1] is None:
                _.append(lambda x: x)
            else:  # 当做一个正则表达式
                pass

    def transform(self):
        pass


from Calf.data import BaseModel

bm = BaseModel(tn='qcc_cq_new')

metaModel = '基本信息'

enterprises = bm.query(
        sql={'metaModel': metaModel,
             # 'name': 'MANDO（重庆）汽车零部件有限公司'
             },
        # field={'content': 1, '_id': 0},
        no_cursor_timeout=True)
i = 0
etp = Enterprise()
etp.compile_regular_pattern()
for e in enterprises:
    if i > 5:
        break
    etp.reload_content(e)
    etp.get_source_dim_2_content()
    etp.replace_keys(print_process=True)
    etp.replace_values(print_process=True)
    j = etp.to_json()
    pass