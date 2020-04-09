# encoding: utf-8
from Calf.data import BaseModel
from pymongo import IndexModel, ASCENDING, DESCENDING


bm = BaseModel(location='server', tn='PKR')
bm.add_index([('label', 1)], name='index1')


