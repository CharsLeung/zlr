# encoding: utf-8

"""
project = zlr
file_name = have
author = Administrator
datetime = 2020/3/27 0027 上午 10:53
from = office desktop
"""
from py2neo import Relationship


class Have:

    """
    囊括的关系包括：有、具有、拥有、具备、有着、
    带有、含有、抱有、所有、占有等
    """

    name = 'HAVE'

    def __init__(self, owner, object, **kwargs):
        self.owner = owner
        self.object = object
        self.properties = kwargs

    def get_relationship(self):
        return Relationship(
            self.owner,
            self.name,
            self.object,
            **self.properties
        )
        pass