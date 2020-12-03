# encoding: utf-8

"""
@project = zlr数据处理
@file_name = mc
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/8/31 0031 下午 13:58
@from = office desktop
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoClientPlus:
    """
    适用于主备模式的MongoDB小集群，一般情况下db1与db2的用户
    在两个数据库上拥有相同的权限，及db1与db2的用户可以互相访问

    :param db1:主服务器，主要用于写数据
    :param db2:从服务器，主要用于读数据
    """
    mcs = {}

    def __init__(self, db1=None, db2=None):
        self._db_info_ = {'write': db1, 'read': db2}
        if db1 is not None:
            try:
                mc_no = self.parse_uri(**db1)
                if mc_no in self.mcs.keys():
                    Mmc = self.mcs[mc_no]['mc']
                else:
                    Mmc = MongoClient(
                        host=db1['host'],
                        port=db1['port'],
                        connect=True,
                        connectTimeoutMS=3000,
                        serverSelectionTimeoutMS=3000
                    )
                    self.mcs[mc_no] = {'mc': Mmc, 'label': ['w']}
                # 验权
                if 'username' in db1.keys() and 'password' in db1.keys():
                    authSource = Mmc[db1.get('authSource', 'admin')]
                    ps = authSource.authenticate(
                        name=db1['username'],
                        password=db1['password']
                    )
                    assert ps, "账户授权失败"
                self.Mmc = Mmc
                pass
            except ConnectionFailure as e:
                self.Mmc = None
                print(e)
        if db2 is not None:
            try:
                mc_no = self.parse_uri(**db2)
                if mc_no in self.mcs.keys():
                    Smc = self.mcs[mc_no]['mc']
                else:
                    Smc = MongoClient(
                        host=db2['host'],
                        port=db2['port'],
                        connect=True,
                        connectTimeoutMS=3000,
                        serverSelectionTimeoutMS=3000
                    )
                    self.mcs[mc_no] = {'mc': Smc, 'label': ['r']}
                # 验权
                if 'username' in db2.keys() and 'password' in db2.keys():
                    authSource = Smc[db2.get('authSource', 'admin')]
                    ps = authSource.authenticate(
                        name=db2['username'],
                        password=db2['password']
                    )
                    assert ps, "账户授权失败"
                self.Smc = Smc
            except ConnectionFailure as e:
                self.Smc = None
                print(e)

    def __getattr__(self, item):
        """
        根据item获取一个mc
        mcp.r

        :param item: address or label
        :return:
        """
        item = item.upper()
        if item.startswith('R') or item.startswith('S'):  # read slave
            mc = self.__dict__.get('Smc')
            return self.__dict__.get('Mmc') if mc is None else mc
        elif item.startswith('W') or item.startswith('M'):  # write master
            mc = self.__dict__.get('Mmc')
            return self.__dict__.get('Smc') if mc is None else mc
        else:
            return None
        pass

    def __getitem__(self, item):
        item = item.upper()
        if item.startswith('R') or item.startswith('S'):  # read slave
            mc = self.__dict__.get('Smc')
            return self.__dict__.get('Mmc') if mc is None else mc
        elif item.startswith('W') or item.startswith('M'):  # write master
            mc = self.__dict__.get('Mmc')
            return self.__dict__.get('Smc') if mc is None else mc
        else:
            return None
        pass

    def get_db_info(self):
        info = {}
        if self._db_info_.get('write') is not None:
            info['write'] = {
                'host': self._db_info_.get('write').get('host'),
                'port': self._db_info_.get('write').get('port')
            }
        else:
            info['write'] = {
                'host': self._db_info_.get('read').get('host'),
                'port': self._db_info_.get('read').get('port')
            }
        if self._db_info_.get('read') is not None:
            info['read'] = {
                'host': self._db_info_.get('read').get('host'),
                'port': self._db_info_.get('read').get('port')
            }
        else:
            info['read'] = {
                'host': self._db_info_.get('write').get('host'),
                'port': self._db_info_.get('write').get('port')
            }
        return info

    def close(self):
        try:
            if self.Mmc is not None:
                self.Mmc.close()
        except Exception as e:
            pass
        try:
            if self.Smc is not None:
                self.Smc.close()
        except Exception as e:
            pass

    def close_all(self):
        for mc_no in self.mcs.keys():
            try:
                self.mcs.get(mc_no)['mc'].close()
            except Exception as e:
                pass

    @staticmethod
    def parse_uri(**db):
        uri = 'mongodb://'
        fields = db.keys()
        if 'username' in fields and 'password' in fields:
            uri += '{username}:{password}@'.format(
                username=db['username'],
                password=db['password'])
        # ip是必须的
        uri += f"{db.get('host', '127.0.0.1')}:{db.get('port', 27017)}"
        uri += f"/?connectTimeoutMS={db.get('connectTimeoutMS', 2000)}"
        if 'replicaSet' in fields:
            uri += ';replicaSet=%s' % db['replicaSet']
        if 'authSource' in fields:
            uri += ';authSource=%s' % db['authSource']
        return uri


# # 创建一个Mongo Client
# mcp = MongoClientPlus(
#     db1={
#         # 更新、写
#         "host": "10.255.57.80",
#         "port": 27017,
#         "username": "testUser",
#         "password": "12345",
#         "authSource": "admin"
#     }, db2={
#         # 读
#         "host": "10.255.57.81",
#         "port": 27017,
#         "username": "testUser",
#         "password": "12345",
#         "authSource": "admin"
#     })
#
# # 写入数据，mcp.write返回一个具体的Mongo Client，指向db1，后续的操作跟原始的MongoClient一样
# mcp.write.test.abc.insert_one({'a': 1, 'b': 2})
#
# # 查询数据，mcp.read Client，指向db2
# i = mcp.read.test.abc.find_one()
# print(i)
# pass
