# encoding: utf-8

"""
project = 'Spider'
file_name = 'address'
author = 'Administrator'
datetime = '2020-03-17 11:21'
IDE = PyCharm
"""

class Address:

    def __init__(self, name):
        self.name = name
        pass

    def get_level_1(self):
        """
        获取一级省、直辖市、自治区、特区
        :return:
        """
        if '省' in self.name:
            return self.name.split('省')[0] + '省'


