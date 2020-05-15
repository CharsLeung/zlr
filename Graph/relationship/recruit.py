# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = recruite
author = Administrator
datetime = 2020/5/9 0009 下午 17:19
from = office desktop
"""
from py2neo import Relationship


class Recruit:

    """
    招聘
    """

    name = 'RECRUIT'

    ATTRIBUTES = [
        ['月薪', 'SALARY'],
        ['学历', 'EDUCATION'],
        ['经验', 'EXPERIENCE'],
        ['所在城市', 'CITY'],
        ['发布日期', 'RELEASE_DATE']
    ]

    def __init__(self, enterprise, position, **kwargs):
        self.position = position
        self.enterprise = enterprise
        self.properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                self.properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                self.properties[a[1]] = kwargs.pop(a[1])
            else:
                if a[0] in position.keys():
                    self.properties[a[1]] = position[a[0]]
                elif a[1] in position.keys():
                    self.properties[a[1]] = position[a[1]]
                else:
                    pass
        self.properties = dict(self.properties, **kwargs)
        pass

    def get_relationship(self):
        return Relationship(
            self.enterprise,
            self.name,
            self.position,
            **self.properties
        )