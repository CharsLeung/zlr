# encoding: utf-8

"""
project = 'zlr'
file_name = 'industry'
author = 'Administrator'
datetime = '2020/3/25 0025 下午 15:07'
from = 'office desktop' 
"""
import re
import time
import datetime as dt

from Graph import BaseGraph
from Graph.entity import Enterprise
from Graph.entity import Industry
from Graph.relationship import Belong
from Calf.data import BaseModel
from Graph.exception import SuccessMessage


class IndGraph(BaseGraph):

    def __init__(self, **kwargs):
        BaseGraph.__init__(self, **kwargs)
        self.base = BaseModel(
            tn='cq_api',
            # tn='relationsDetail.1.0',
            # location='gcxy',
            # dbname='data'
        )
        pass

    def get_all_nodes_and_relationships_from_api(self, etp):
        """
        创建所有的行业实体，实体对象从外部传进来，因为行业可能
        会作为一个相对独立的研究领域，与数据库中企业基本信息中的
        行业可能不完全匹配
        :return:
        """
        etp_n = self.match_node(
            'Enterprise',
            cypher='_.URL = "{}" OR _.NAME = "{}"'
                   ''.format(Enterprise.parser_url(etp['url']),
                             etp['name']))
        if etp_n is None:
            etp_n = Enterprise(URL=etp['url'], NAME=etp['name'])
            etp_n = self.get_neo_node(etp_n)
        if etp_n is None:
            return [], []
        nodes, relationships = [], []
        nodes.append(etp_n)
        ind = etp['IndustryV3']
        if ind is None:
            return nodes, relationships
        ind1 = self.get_neo_node(Industry(**{
            'name': ind['Industry'],
            'code': ind['IndustryCode'],
            '类别': '一级'
        }))
        ind2 = self.get_neo_node(Industry(**{
            'name': ind['SubIndustry'],
            'code': ind['SubIndustryCode'],
            '类别': '二级'
        }))
        ind3 = self.get_neo_node(Industry(**{
            'name': ind['MiddleCategory'],
            'code': ind['MiddleCategoryCode'],
            '类别': '三级'
        }))
        ind4 = self.get_neo_node(Industry(**{
            'name': ind['SmallCategory'],
            'code': ind['SmallCategoryCode'],
            '类别': '四级'
        }))
        _ids_ = [ind4, ind3, ind2, ind1]
        ids = []
        for i in _ids_:
            if i is not None:
                ids.append(i)
                nodes.append(i)
        if len(ids):
            relationships.append(Belong(etp_n, ids[0]))
            for i in range(len(ids) - 1):
                relationships.append(Belong(ids[i], ids[i + 1]))
            pass
        return nodes, relationships
        pass

    def merge_all_nodes_and_relationships(self):
        enterprises = self.base.query(
            # sql={'metaModel': '企业发展'},
            field={
                '_id': 0,
                'value.Result.Name': 1,
                'value.Result.KeyNo': 1,
                'value.Result.IndustryV3': 1
            },
            limit=10000,
            # skip=2000,
            no_cursor_timeout=True)
        i, j = 0, 0
        nc, rc = 0, 0
        etp_count = 10000
        # etp_count = enterprises.count()
        nodes, relationships = {}, {}
        unique_code_pattern = re.compile('(?<=unique=)\w{32}')

        def getUniqueCode(url):
            _uc_ = re.search(unique_code_pattern, url)
            if _uc_ is not None:
                return _uc_.group(0)
            else:
                return None

        _st_ = time.time()
        for ep in enterprises:
            i += 1
            ep = ep['value']['Result']
            uc = ep['KeyNo']  # getUniqueCode(ep['url'])
            ep['name'] = ep.pop('Name')
            if uc is None:
                self.logger.info('{}:mismatch url'.format(ep['name']))
                continue
            ep['url'] = '/firm_' + uc + '.html'
            nds, rps = self.get_all_nodes_and_relationships_from_api(ep)

    def get_all_nodes_and_relationships(
            self, save_folder=None, enterprises=None, **kwargs):
        if enterprises is None:
            enterprises_data = self.base.query(
                # sql={'metaModel': '企业发展'},
                field={
                    '_id': 0,
                    'value.Result.Name': 1,
                    'value.Result.KeyNo': 1,
                    'value.Result.IndustryV3': 1
                },
                limit=10000,
                # skip=2000,
                no_cursor_timeout=True)
            etp_count = 10000
            # etp_count = enterprises_data.count()
        else:
            enterprises_data = enterprises
            etp_count = len(enterprises)
        i, j = 0, 0
        nc, rc = 0, 0
        nodes, relationships = {}, {}
        unique_code_pattern = re.compile('(?<=unique=)\w{32}')

        def getUniqueCode(url):
            _uc_ = re.search(unique_code_pattern, url)
            if _uc_ is not None:
                return _uc_.group(0)
            else:
                return None

        _st_ = time.time()
        for ep in enterprises_data:
            i += 1
            if enterprises is not None:
                ep = self.base.query_one(
                    sql={'value.Result.Name': ep['name']},
                    field={
                        '_id': 0,
                        'value.Result.Name': 1,
                        'value.Result.KeyNo': 1,
                        'value.Result.IndustryV3': 1
                    },
                )
                if ep is None:
                    continue

            ep = ep['value']['Result']
            uc = ep['KeyNo']  # getUniqueCode(ep['url'])
            ep['name'] = ep.pop('Name')
            if uc is None:
                self.logger.info('{}:mismatch url'.format(ep['name']))
                continue
            ep['url'] = '/firm_' + uc + '.html'
            nds, rps = self.get_all_nodes_and_relationships_from_api(ep)
            for _nds_ in nds:
                if _nds_ is None:
                    continue
                # _nds_ = _nds_.to_dict()
                label = list(_nds_.labels)[0]
                _nds_ = dict(label=label, **_nds_)
                if _nds_['label'] in nodes.keys():
                    nodes[_nds_['label']].append(_nds_)
                else:
                    nodes[_nds_['label']] = [_nds_]
                pass
            for _rps_ in rps:
                _rps_ = _rps_.to_dict()
                if _rps_['label'] in relationships.keys():
                    relationships[_rps_['label']].append(_rps_)
                else:
                    relationships[_rps_['label']] = [_rps_]
                pass
            if i % 10000 == 0:
                j += 1
                if save_folder is not None:
                    _nc_, _rc_ = self.save_graph(
                        save_folder, nodes,
                        relationships, **kwargs)
                    nc += _nc_
                    rc += _rc_
                    nodes.clear()
                    relationships.clear()
                self.logger.info(SuccessMessage(
                    'success trans data to csv round {} and '
                    'deal {}/{} enterprise spend {} seconds.'
                    ''.format(j, i, etp_count, int(time.time() - _st_))
                ))
                _st_ = time.time()
                pass
        if save_folder is not None:
            _nc_, _rc_ = self.save_graph(
                save_folder, nodes,
                relationships, **kwargs)
            nc += _nc_
            rc += _rc_
            nodes.clear()
            relationships.clear()
            self.logger.info('Summary:')
            self.logger.info(' save graph data:')
            self.logger.info('   {} nodes'.format(nc))
            self.logger.info('   {} relationships'.format(rc))
            pass
        return nodes, relationships
