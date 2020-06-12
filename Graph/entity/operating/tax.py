# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = tax
author = Administrator
datetime = 2020/4/7 0007 下午 16:56
from = office desktop
"""
import warnings
from Graph.entity import BaseEntity


class TaxCredit(BaseEntity):

    """
    税务信用
    """

    ATTRIBUTES = [
        ['纳税人识别号', 'TAXPAYER_NUMBER'],
        ['纳税信用等级', 'GRADE'],
        ['评价单位', 'APPRAISAL_AGENCY'],
        ['评价年度', 'APPRAISAL_YEAR'],
    ]

    synonyms = {
        # '企业': '标的名称',
        # '链接': '标的链接'
    }

    primarykey = 'HASH_ID'

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        # self['HASH_ID'] = hash(str(self.BaseAttributes))
        self[self.primarykey] = '%s_%s' % (
            self.label,
            self.getHashValue(str(self.BaseAttributes))
        )
        # if 'URL' in self.BaseAttributes.keys():
        #     self['URL'] = self.parser_url(
        #         self['URL'])
        pass

    @classmethod
    def create_from_dict(cls, content):
        """

        :param content:
        :return:
        """
        obj = []

        def f(c):
            # del c['序号']
            # _ = c.pop('内容')
            # c['专利名称'] = _['名称']
            # c['内容链接'] = _['post链接']
            return dict(TaxCredit=TaxCredit(**c))

        if isinstance(content, dict):
            obj.append(f(content))
        elif isinstance(content, list):
            obj += [f(c) for c in content]
        else:
            warnings.warn('invalid type for tax-credit content.')
        return obj