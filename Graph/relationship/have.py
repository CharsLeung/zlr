# encoding: utf-8

"""
project = zlr
file_name = have
author = Administrator
datetime = 2020/3/27 0027 上午 10:53
from = office desktop
"""
from Graph.relationship import Base


class Have(Base):
    """
    囊括的关系包括：有、具有、拥有、具备、有着、
    带有、含有、抱有、所有、占有等
    """

    def __init__(self, owner=None, object=None, **kwargs):
        Base.__init__(self, owner, object, **kwargs)
        pass

    def to_dict(self):
        return dict({
            'label': self.label,
            'from': self.start[self.start.__primarykey__],
            'from_label': list(self.start.labels)[0],
            'to': self.end[self.end.__primarykey__],
            'to_label': list(self.end.labels)[0],
        }, **self.properties)

    def getImportCSV(self, rps):
        dtypes = dict(rps.dtypes)
        for k, v in rps.groupby(['label', 'from_label', 'to_label']):
            pass
        names = {'from': ':START_ID', 'to': ':END_ID', 'label': ':TYPE'}
        for k, v in zip(dtypes.keys(), dtypes.values()):
            if k in names.keys():
                continue
            if 'int' in v.name:
                names[k] = '{}:{}'.format(k, 'int')
            elif 'float' in v.name:
                names[k] = '{}:{}'.format(k, 'float')
            else:
                pass
        rps = rps.rename(columns=names)
        return rps
        pass