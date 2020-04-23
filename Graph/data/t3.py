# encoding: utf-8

"""
project = zlr
file_name = t3
author = Administrator
datetime = 2020/4/2 0002 下午 14:04
from = office desktop
"""
import datetime as dt

from Calf.utils import trading


# 交易日计算
d = dt.datetime.today()     # 基准日期
days = 1    # offset 负数
# trading.trade_period(d, days)

d = [
    [1, 2, 3],
    [1, 2],
    [1]
]
d.sort(key=lambda x: len(x))