# encoding: utf-8

"""
project = zlr(20200403备份)
file_name = head_company
author = Administrator
datetime = 2020/5/8 0008 下午 16:32
from = office desktop
"""
from Graph.entity import BaseEntity


class HeadCompany(BaseEntity):

    """
    # TODO(leung):这个可能会被抛弃
    总公司，总公司对象不是某个已存在的企业时，新建一个总公司实体
    """

    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
        ['注册资本(金额)', 'REGISTERED_CAPITAL_AMOUNT'],
        ['注册资本(单位)', 'REGISTERED_CAPITAL_UNIT'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['经营状态', 'OPERATING_STATUS']
    ]

    synonyms = {
        '状态': '经营状态',
        # '认缴出资额_万元': '认缴出资额',
        # '链接': '股东链接'
    }

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(self['URL'])
            if self['URL'] is None:
                if len(self['NAME']) < 2:
                    self['NAME'] = None
                else:
                    self['URL'] = '%s_%s' % (
                        self.label,
                        self.getHashValue(self['NAME'])
                    )
        pass