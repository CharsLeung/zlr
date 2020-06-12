# encoding: utf-8

"""
@project = zlr(20200403备份)
@file_name = middle
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/6/11 0011 下午 13:38
@from = office desktop
"""
import pandas as pd


class MiddleEntity:

    primarykey = None  # 唯一键

    index = []  # 索引

    ATTRIBUTES = []

    synonyms = {}

    # cipher = Prpcrypt('syxsyx')
    # unique_code_pattern = re.compile('[a-zA-Z]+_\w{32}')  # (?<=/)(?=\.)

    def __init__(self, **kwargs):
        self.BaseAttributes = kwargs
        pass

    def to_pandas(self, nodes):
        #
        nodes = pd.DataFrame(nodes)
        drop = nodes.groupby([self.primarykey], as_index=False).agg({
            self.primarykey: 'count'
        })
        drop = drop[drop[self.primarykey] > 3][self.primarykey]
        # drop = drop.tolist()
        if len(drop):
            nodes = nodes[~nodes[self.primarykey].isin(drop)]
        nodes.dropna(subset=[self.primarykey], inplace=True)
        nodes.drop_duplicates(subset=[self.primarykey], inplace=True)
        nodes.dropna(axis=1, how='all', inplace=True)
        return nodes
        pass