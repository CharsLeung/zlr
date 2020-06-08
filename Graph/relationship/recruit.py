# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = recruite
author = Administrator
datetime = 2020/5/9 0009 下午 17:19
from = office desktop
"""
from Graph.relationship import Base


class Recruit(Base):

    """
    招聘
    """

    ATTRIBUTES = [
        ['月薪', 'SALARY'],
        ['学历', 'EDUCATION'],
        ['经验', 'EXPERIENCE'],
        ['所在城市', 'CITY'],
        ['发布日期', 'RELEASE_DATE']
    ]

    def __init__(self, enterprise=None, position=None, **kwargs):
        properties = {}
        ks = kwargs.keys()
        for a in self.ATTRIBUTES:
            if a[0] in ks:
                properties[a[1]] = kwargs.pop(a[0])
            elif a[1] in ks:
                properties[a[1]] = kwargs.pop(a[1])
            else:
                if position is None:
                    continue
                if a[0] in position.keys():
                    properties[a[1]] = position[a[0]]
                elif a[1] in position.keys():
                    properties[a[1]] = position[a[1]]
                else:
                    pass
        properties = dict(properties, **kwargs)
        Base.__init__(self, enterprise, position, **properties)
        pass