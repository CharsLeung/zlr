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

from Graph.entity import BaseEntity

warnings.filterwarnings('ignore')

pca = {
    '重庆市': [
        '渝中区',
        '万州区',
        '涪陵区',
        '大渡口区',
        '江北区',
        '沙坪坝区',
        '九龙坡区',
        '南岸区',
        '北碚区',
        '綦江区',
        '大足区',
        '渝北区',
        '巴南区',
        '黔江区',
        '长寿区',
        '江津区',
        '合川区',
        '永川区',
        '南川区',
        '璧山区',
        '铜梁区',
        '潼南区',
        '荣昌区',
        '开州区',
        '梁平区',
        '武隆区',
        '城口县',
        '丰都县',
        '垫江县',
        '忠县',
        '云阳县',
        '奉节县',
        '巫山县',
        '巫溪县',
        '石柱土家族自治县',
        '秀山土家族苗族自治县',
        '酉阳土家族苗族自治县',
        '彭水苗族土家族自治县',
        '石柱',
        '秀山',
        '酉阳',
        '彭水',
    ]
}


class Address(BaseEntity):
    """
    地址
    """

    ATTRIBUTES = [
        ['地址', 'ADDRESS'],
        ['省', 'PROVINCE'],
        ['市', 'CITY'],
        ['区', 'COUNTY'],
        ['详细地址', 'DETAIL']
    ]

    primarykey = 'ADDRESS'

    def __init__(self, address=''):
        BaseEntity.__init__(self)
        address = str(address).replace(' ', '')
        if len(address) > 1:
            self.BaseAttributes = {'ADDRESS': address}
        # self.__split_levels__()
        pass

    def __split_levels__(self):
        """
        获取一级省、直辖市、自治区、特区
        :return:
        """
        # cpca 还带有绘图功能
        if len(self.BaseAttributes['ADDRESS']):
            _ = cpca.transform([self.BaseAttributes['ADDRESS']])
            _ = _.to_dict(orient='index')[0]
            self.BaseAttributes['PROVINCE'] = _['省']
            self.BaseAttributes['CITY'] = _['市']
            self.BaseAttributes['COUNTY'] = _['区']
            self.BaseAttributes['DETAIL'] = _['地址']
        pass

    @classmethod
    def complete(cls, data):
        """
        把导出的地址节点信息加工完善，
        :return:
        """
        data = cpca.transform(data['ADDRESS'])
        pass

# Address('重庆市渝中区上清寺路9号环球广场7楼')
# pass
# import pandas as pd
#
#
# ads = pd.read_csv('D:\graph_data\图数据\基本信息\实体\Address.csv',
#                   engine='python', encoding='utf-8')
# Address.complete(ads)
