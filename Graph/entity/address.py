# encoding: utf-8

"""
project = 'Spider'
file_name = 'address'
author = 'Administrator'
datetime = '2020-03-17 11:21'
IDE = PyCharm
"""
import cpca
import warnings

from Graph.entity import QccRequest

warnings.filterwarnings('ignore')


class Address(QccRequest):

    ATTRIBUTES = [
        ['ADDRESS', '地址'],
        ['PROVINCE', '省'],
        ['CITY', '市'],
        ['COUNTY', '区'],
        ['DETAIL', '详细地址']
    ]

    primarykey = 'ADDRESS'

    def __init__(self, address):
        QccRequest.__init__(self)
        self.BaseAttributes = {'ADDRESS': str(address).replace(' ', '')}
        self.__split_levels__()
        pass

    def __split_levels__(self):
        """
        获取一级省、直辖市、自治区、特区
        :return:
        """
        # cpca 还带有绘图功能
        _ = cpca.transform([self.BaseAttributes['ADDRESS']])
        _ = _.to_dict(orient='index')[0]
        self.BaseAttributes['PROVINCE'] = _['省']
        self.BaseAttributes['CITY'] = _['市']
        self.BaseAttributes['COUNTY'] = _['区']
        self.BaseAttributes['DETAIL'] = _['地址']
        pass


# Address('重庆市渝中区上清寺路9号环球广场7楼')
# pass

