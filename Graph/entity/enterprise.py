# encoding: utf-8

"""
project = 'Spider'
file_name = 'baseinfo'
author = 'Administrator'
datetime = '2020-03-16 18:47'
IDE = PyCharm
"""
import re
import warnings

from py2neo import Node as NeoNode
from Graph.entity import QccRequest, Person, Address, \
    ShareHolder, Invested, Telephone, Email


# from pyecharts.options import GraphNode as EchartsGraphNode


class Enterprise(QccRequest):
    entity_category_index = 1

    # 属性对照表
    ATTRIBUTES = [
        ['电话', 'TELEPHONE'],
        ['官网', 'WEBSITE'],
        ['邮箱', 'EMAIL'],
        ['地址', 'ADDRESS'],
        ['简介', 'INTRODUCTION'],
        ['经营状态', 'OPERATING_STATUS'],
        ['统一社会信用代码', 'UNIFORM_SOCIAL_CREDIT_CODE'],
        ['注册资本', 'REGISTERED_CAPITAL'],
        ['实缴资本', 'PAID_UP_CAPITAL'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['纳税人识别号', 'TAXPAYER_NUMBER'],
        ['注册号', 'REGISTRATION_NUMBER'],
        ['组织机构代码', 'ORGANIZATION_CODE'],
        ['企业类型', 'ENTERPRISE_TYPE'],
        ['所属行业', 'INDUSTRY'],
        ['核准日期', 'APPROVAL_DATE'],
        ['登记机关', 'REGISTRATION_AUTHORITY'],
        ['所属地区', 'DISTRICT_BELONG'],
        ['英文名', 'ENGLISH_NAME'],
        ['曾用名', 'USED_NAME'],
        ['参保人数', 'NUMBER_OF_PARTICIPANTS'],
        ['营业期限', 'OPERATING_PERIOD'],
        ['人员规模', 'STAFF_SIZE'],
        ['企业地址', 'ENTERPRISE_ADDRESS'],
        ['经营范围', 'BUSINESS_SCOPE'],
    ]

    primarykey = 'URL'

    def __init__(self, ReturnString=None):
        QccRequest.__init__(self, ReturnString)
        if ReturnString is None:
            pass
        else:
            if self.metaModel != '基本信息':
                raise TypeError('')

            self._certifications()
            self._business()
        pass

    def _certifications(self):
        """
        处理->认证信息
        :return:
        """
        ctf = self.content['认证信息']
        # ctf_keys = ctf.keys()
        # ks = ['电话', '官网', '邮箱', '地址', '简介']
        for k, v in zip(ctf.keys(), ctf.values()):
            _ = self.get_englishAttribute_by_chinese(k)
            if _ is not None:
                self.BaseAttributes[_] = v

    def _business(self):
        """

        :return:
        """
        bs = self.content['工商信息']

        for k, v in zip(bs.keys(), bs.values()):
            _ = self.get_englishAttribute_by_chinese(k)
            if _ is not None:
                self.BaseAttributes[_] = v
        pass

    def get_echarts_node(self):
        # return EchartsGraphNode(
        #     name=self.name,
        #     category=self.entity_category_index,
        #
        # )
        pass

    def get_neo_node(self, primarylabel=None, primarykey=None):
        n = NeoNode(
            self.label,
            URL=self.url,
            NAME=self.name,
            UPDATE_DATE=self.update_date,
            **self.BaseAttributes
        )
        if primarylabel is not None:
            n.__primarylabel__ = primarylabel
        else:
            n.__primarylabel__ = self.label
        if primarykey is not None:
            n.__primarykey__ = primarykey
        return n

    def get_legal_representative(self):
        lr = self.content['工商信息']['法定代表人']
        if isinstance(lr, dict):
            p = Person(**lr)
        elif isinstance(lr, list):
            warnings.warn('Generally, there is only one legal '
                          'representative, but multiple.')
            p = Person(**lr[0])
        else:
            warnings.warn('Unusual legal representative information.')
            p = Person(**{Person.primarykey: lr})
        return p
        pass

    def get_manager(self):
        mgs = []
        if '主要人员' in self.content.keys():
            ms = self.content['主要人员']  # 可能分为工商登记、上市公示两类
            if isinstance(ms, dict):
                for k, v in zip(ms.keys(), ms.values()):
                    for m in v:
                        mgs.append({
                            'person': Person(**m['人员']),
                            'position': m['职务'],
                            'category': k
                        })
            elif isinstance(ms, list):
                for m in ms:
                    mgs.append({
                        'person': Person(**m['人员']),
                        'position': m['职务']
                    })
            else:
                warnings.warn('Generally, the type of major managers is '
                              'in (dict, list).')
        return mgs
        pass

    def get_address(self):
        return Address(
            self.BaseAttributes['ADDRESS']
        )

    def get_share_holder(self):
        sh = []
        if '工商股东' in self.content.keys():
            shs = self.content['工商股东']
            if isinstance(shs, list):
                for s in shs:
                    _ = s.pop('股东')
                    sh.append({
                        'share_holder': ShareHolder(**dict(s, **_))
                    })
            elif isinstance(shs, dict):
                _ = shs.pop('股东')
                sh.append({
                    'share_holder': ShareHolder(**dict(shs, **_))
                })
            else:
                warnings.warn('Generally, the type of share holders is '
                              'in (dict, list).')
        return sh
        pass

    def invest_outer(self):
        # 对外投资的肯定是企业，但是对外投资这个字段下面很可能确定不到具体的公司
        iv = []
        if '对外投资' in self.content.keys():
            ivs = self.content['对外投资']
            if isinstance(ivs, list):
                for i in ivs:
                    iv.append({
                        'invested': Invested(**{
                            '名称': i['被投资企业']['名称'],
                            '链接': i['被投资企业']['链接'],
                            '注册资本': i['注册资本'],
                            '成立日期': i['成立日期'],
                            '状态': i['状态']
                        }),
                        '投资比例': i['投资']['比例'],
                        '投资数额': i['投资']['数额'],
                    })
                    pass
            if isinstance(ivs, dict):
                iv.append({
                    'invested': Invested(**{
                        '名称': ivs['被投资企业']['名称'],
                        '链接': ivs['被投资企业']['链接'],
                        '注册资本': ivs['注册资本'],
                        '成立日期': ivs['成立日期'],
                        '状态': ivs['状态']
                    }),
                    '投资比例': ivs['投资']['比例'],
                    '投资数额': ivs['投资']['数额'],
                })

    def get_telephone_number(self):
        tel = self.BaseAttributes['TELEPHONE']
        # tel = re.search('\d+[-]\d+', tel)
        # tel = tel.group(0) if tel is not None else None
        if tel is not None and len(tel):
            return Telephone(telephone=tel)
        else:
            return None

    def get_email(self):
        em = self.BaseAttributes['EMAIL']
        # em = re.search('[1]+@([0-9a-z]+.)+[a-z]+$', em, re.I)
        # em = em.group(0) if em is not None else None
        if em is not None and len(em):
            return Email(email=em)
        else:
            return None

