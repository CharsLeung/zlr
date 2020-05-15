# encoding: utf-8

"""
project = 'Spider'
file_name = 'baseinfo'
author = 'Administrator'
datetime = '2020-03-16 18:47'
IDE = PyCharm
"""
import warnings

from py2neo import Node as NeoNode
from Graph.entity import QccRequest, Person, Address, \
    ShareHolder, Invested, Telephone, Email, Branch, \
    HeadCompany, ConstructionProject, Related, Certificate

# from pyecharts.options import GraphNode as EchartsGraphNode
from Graph.exception import ExceptionInfo


class Enterprise(QccRequest):
    """
    公司，主要列示了工商信息和最基本的信息
    """

    # 属性对照表
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['电话', 'TELEPHONE'],
        ['官网', 'WEBSITE'],
        ['邮箱', 'EMAIL'],
        ['地址', 'ADDRESS'],
        ['简介', 'INTRODUCTION'],
        ['经营状态', 'OPERATING_STATUS'],
        ['统一社会信用代码', 'UNIFORM_SOCIAL_CREDIT_CODE'],
        ['注册资本(金额)', 'REGISTERED_CAPITAL_AMOUNT'],
        ['注册资本(单位)', 'REGISTERED_CAPITAL_UNIT'],
        ['实缴资本(金额)', 'PAID_UP_CAPITAL_AMOUNT'],
        ['实缴资本(单位)', 'PAID_UP_CAPITAL_UNIT'],
        ['成立日期', 'ESTABLISHMENT_DATE'],
        ['纳税人识别号', 'TAXPAYER_NUMBER'],
        ['工商注册号', 'REGISTRATION_NUMBER'],
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

    synonyms = {}

    primarykey = 'URL'

    index = [('NAME',)]

    def __init__(self, ReturnString=None, **kwargs):
        QccRequest.__init__(self, ReturnString)
        if ReturnString is None:
            pass
        else:
            if self.metaModel != '基本信息':
                raise TypeError('')
            self.BaseAttributes['URL'] = self.parser_url(self.url)
            self.BaseAttributes['NAME'] = self.name.strip()
            self.BaseAttributes['UPDATE_DATE'] = self.update_date
            if 'content' in ReturnString.keys():
                self._certifications()
                self._business()
                # if
        if len(kwargs):
            sks = self.synonyms.keys()
            cad = self.chineseAttributeDict()
            for k, v in zip(kwargs.keys(), kwargs.values()):
                if k in cad.keys():
                    self.BaseAttributes[cad[k]] = v
                elif k in sks:
                    self.BaseAttributes[cad[self.synonyms[k]]] = v
                else:
                    warnings.warn('Undefined key for dict of enterprise.')
                    self.BaseAttributes[k] = v
            if 'URL' in self.BaseAttributes.keys():
                self.BaseAttributes['URL'] = self.parser_url(
                    self.BaseAttributes['URL'])
        pass

    def _certifications(self):
        """
        处理->认证信息
        :return:
        """
        ctf = self.get_format_dict(
            self.content['注册信息']
        )
        try:
            if len(ctf):
                for k, v in zip(ctf.keys(), ctf.values()):
                    _ = self.get_englishAttribute_by_chinese(k)
                    if _ is not None:
                        self.BaseAttributes[_] = v
                    else:
                        self.BaseAttributes[k] = v
        except Exception as e:
            ExceptionInfo(e)
            print(self.name, ctf)

    def _business(self):
        """

        :return:
        """
        bs = self.get_format_dict(
            self.content['工商信息']
        )
        try:
            del bs['法定代表人']
            if '注册资本' in bs.keys():
                bs = dict(bs, **self.get_format_amount(
                    '注册资本', bs.pop('注册资本')))
            if '实缴资本' in bs.keys():
                bs = dict(bs, **self.get_format_amount(
                    '实缴资本', bs.pop('实缴资本')))
            for k, v in zip(bs.keys(), bs.values()):
                _ = self.get_englishAttribute_by_chinese(k)
                if _ is not None:
                    self.BaseAttributes[_] = v
                else:
                    self.BaseAttributes[k] = v
            pass
        except Exception as e:
            ExceptionInfo(e)
            print(self.name, bs)

    def get_neo_node(self, primarylabel=None, primarykey=None):
        n = NeoNode(
            self.label,
            # URL=self.url,
            # NAME=self.name,
            # UPDATE_DATE=self.update_date,
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
        bs = self.get_format_dict(self.content['工商信息'])
        lr = bs['法定代表人']
        if isinstance(lr, dict):
            p = Person(**lr)
        elif isinstance(lr, list):
            warnings.warn('Generally, there is only one legal '
                          'representative, but multiple.')
            p = Person(**lr[0])
        else:
            warnings.warn('Unusual legal representative '
                          'information.')
            p = Person(**{Person.primarykey: lr})
        return p
        pass

    def get_manager(self):
        mgs = []
        ms = self.get_format_dict(self.content['主要人员'])

        def f(c):
            p = dict(person=Person(
                NAME=c.pop('姓名'), URL=c.pop('链接')), **c
            )
            return p

        if isinstance(ms, dict):
            mgs.append(f(ms))
        elif isinstance(ms, list):
            for m in ms:
                mgs.append(f(m))
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
        if '股东信息' in self.content.keys():
            shs = self.get_format_dict(self.content['股东信息'])

            def f(s):
                _ = s.pop('股东')
                if '实缴出资额' in s.keys():
                    s = dict(s, **self.get_format_amount(
                        '实缴出资额', s.pop('实缴出资额')
                    ))
                if '认缴出资额' in s.keys():
                    s = dict(s, **self.get_format_amount(
                        '认缴出资额', s.pop('认缴出资额')
                    ))
                s = dict(share_holder=ShareHolder(**_), **s)
                return s

            if isinstance(shs, list):
                for s in shs:
                    sh.append(f(s))
            elif isinstance(shs, dict):
                sh.append(f(shs))
            else:
                warnings.warn('Generally, the type of share holders is '
                              'in (dict, list).')
        return sh
        pass

    def get_invest_outer(self):
        # 对外投资的肯定是企业，但是对外投资这个字段下面很可能确定不到具体的公司
        iv = []
        if '对外投资' in self.content.keys():
            ivs = self.get_format_dict(self.content['对外投资'])

            def f(_):
                e = _.pop('被投资企业')
                if '注册资本' in _.keys():
                    e = dict(e, **self.get_format_amount(
                        '注册资本', _.pop('注册资本')
                    ))
                if '法定代表人' in _.keys():
                    e = dict(e, **self.get_format_amount(
                        '法定代表人', _.pop('法定代表人')
                    ))
                if '成立日期' in _.keys():
                    e = dict(e, **{'成立日期': _.pop('成立日期')})
                if '投资数额' in _.keys():
                    _ = dict(_, **self.get_format_amount(
                        '投资数额', _.pop('投资数额')
                    ))
                return dict(invested=Invested(**e), **_)

            if isinstance(ivs, list):
                for i in ivs:
                    iv.append(f(i))
                    pass
            elif isinstance(ivs, dict):
                iv.append(f(ivs))
            else:
                warnings.warn('Generally, this type is '
                              'in (dict, list).')
        return iv

    def get_telephone_number(self):
        if 'TELEPHONE' in self.BaseAttributes.keys():
            tel = self.BaseAttributes['TELEPHONE']
            if tel is not None and len(tel):
                return Telephone(telephone=tel)
            else:
                return None
        else:
            return None

    def get_email(self):
        if 'EMAIL' in self.BaseAttributes.keys():
            em = self.BaseAttributes['EMAIL']
            if em is not None and len(em):
                return Email(email=em)
            else:
                return None
        else:
            return None

    def get_branch(self):
        brs = []
        if '分支机构' in self.content.keys():
            bs = self.get_format_dict(self.content['分支机构'])

            def f(_):
                return dict(
                    branch=Branch(**_.pop('企业')),
                    principal=Person(**_.pop('负责人')),
                    **_
                )

            if isinstance(bs, list):
                brs += [f(b) for b in bs]
            elif isinstance(bs, dict):
                brs.append(f(bs))
            else:
                warnings.warn('Generally, this type is '
                              'in (dict, list).')
        return brs

    def get_head_company(self):
        hcs = []
        if '总公司' in self.content.keys():
            hs = self.get_format_dict(self.content['总公司'])

            def f(_):
                zgs = _.pop('企业')
                if '注册资本' in _.keys():
                    zgs = dict(zgs, **self.get_format_amount(
                        '注册资本', _.pop('注册资本')
                    ))
                if '成立日期' in _.keys():
                    zgs['成立日期'] = _.pop('成立日期')
                return dict(
                    head=HeadCompany(**zgs),
                    principal=Person(**_.pop('法定代表人')),
                    **_
                )

            if isinstance(hs, list):
                hcs += [f(b) for b in hs]
            elif isinstance(hs, dict):
                hcs.append(f(hs))
            else:
                warnings.warn('Generally, this type is '
                              'in (dict, list).')
        return hcs

    def get_construction_project(self):
        cps = []
        if '建筑工程项目' in self.content.keys():
            cp = self.get_format_dict(self.content['建筑工程项目'])

            def f(_):
                return dict(
                    jsdw=Related(**_.pop('建设单位')),
                    project=ConstructionProject(**_)
                )

            if isinstance(cp, list):
                cps += [f(b) for b in cp]
            elif isinstance(cp, dict):
                cps.append(f(cp))
            else:
                warnings.warn('Generally, this type is '
                              'in (dict, list).')
        return cps

    def get_construction_certificate(self):
        ccs = []
        if '建筑资质资格' in self.content.keys():
            cc = self.get_format_dict(self.content['建筑资质资格'])

            def f(_):
                return {'ctf': Certificate(**_)}

            if isinstance(cc, list):
                ccs += [f(b) for b in cc]
            elif isinstance(cc, dict):
                ccs.append(f(cc))
            else:
                warnings.warn('Generally, this type is '
                              'in (dict, list).')
        return ccs
