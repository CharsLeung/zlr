# encoding: utf-8

"""
project = 'Spider'
file_name = 'baseinfo'
author = 'Administrator'
datetime = '2020-03-16 18:47'
IDE = PyCharm
"""

from Graph import logger
from py2neo import Node as NeoNode
from Graph.entity import BaseEntity, Person, Address, \
    ShareHolder, Invested, Telephone, Email, Branch, \
    HeadCompany, ConstructionProject, Related, Certificate

# from pyecharts.options import GraphNode as EchartsGraphNode
from Graph.exception import ExceptionInfo


class Enterprise(BaseEntity):
    """
    公司，主要列示了工商信息和最基本的信息
    """

    # 属性对照表
    ATTRIBUTES = [
        ['名称', 'NAME'],
        ['链接', 'URL'],
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

    def __init__(self, data=None, **kwargs):
        BaseEntity.__init__(self, data, **kwargs)
        if data is None:
            pass
        else:
            if self.metaModel != '基本信息':
                raise TypeError('')
            self['URL'] = self.url
            self['NAME'] = self.name.strip()
            self['UPDATE_DATE'] = self.update_date
            if 'content' in data.keys():
                self._certifications()
                self._business()
                # if
        if 'URL' in self.BaseAttributes.keys():
            self['URL'] = self.parser_url(
                self['URL'])
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
                        self[_] = v
                    else:
                        self[k] = v
        except Exception as e:
            ExceptionInfo(e)
            logger.error(f"{self.name}, {ctf}")

    def _business(self):
        """

        :return:
        """
        try:
            bs = self.get_format_dict(
                self.content['工商信息']
            )
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
                    self[_] = v
                else:
                    self[k] = v
            pass
        except Exception as e:
            ExceptionInfo(e)
            logger.error(f"{self.name}, {bs}")

    def get_legal_representative(self):
        bs = self.get_format_dict(self.content['工商信息'])
        lr = bs['法定代表人']
        if isinstance(lr, dict):
            p = Person(**lr)
            if not p.isPerson():
                p = Enterprise(**lr)
                if not p.isEnterprise():
                    p = Related(**lr)
        elif isinstance(lr, list):
            logger.warning('Generally, there is only one legal '
                           'representative, but multiple.')
            lr = lr[0]
            p = Person(**lr)
            if not p.isPerson():
                p = Enterprise(**lr)
                if not p.isEnterprise():
                    p = Related(**lr)
        else:
            logger.warning('Unusual legal representative '
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
            logger.warning('Generally, the type of major managers is '
                           'in (dict, list).')
        return mgs
        pass

    def get_address(self):
        return Address(
            self['ADDRESS']
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
                if self.isPerson(_['链接']):
                    _sh_ = Person(**_)
                elif self.isEnterprise(_['链接']):
                    _sh_ = Enterprise(**_)
                else:
                    _sh_ = ShareHolder(**_)
                return dict(share_holder=_sh_, **s)

            if isinstance(shs, list):
                for s in shs:
                    sh.append(f(s))
            elif isinstance(shs, dict):
                sh.append(f(shs))
            else:
                logger.warning('Generally, the type of share holders is '
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
                inv = Enterprise(**e)
                if not inv.isEnterprise():
                    inv = Invested(**e)
                return dict(invested=inv, **_)

            if isinstance(ivs, list):
                for i in ivs:
                    iv.append(f(i))
                    pass
            elif isinstance(ivs, dict):
                iv.append(f(ivs))
            else:
                logger.warning('Generally, this type is '
                               'in (dict, list).')
        return iv

    def get_telephone_number(self):
        if 'TELEPHONE' in self.BaseAttributes.keys():
            tel = self['TELEPHONE']
            if tel is not None and len(tel):
                return Telephone(telephone=tel)
            else:
                return None
        else:
            return None

    def get_email(self):
        if 'EMAIL' in self.BaseAttributes.keys():
            em = self['EMAIL']
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
                b = _.pop('企业')
                bn = Enterprise(**b)
                if not bn.isEnterprise():
                    bn = Branch(**b)
                return dict(
                    branch=bn,
                    principal=Person(**_.pop('负责人')),
                    **_
                )

            if isinstance(bs, list):
                brs += [f(b) for b in bs]
            elif isinstance(bs, dict):
                brs.append(f(bs))
            else:
                logger.warning('Generally, this type is '
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
                zgs_n = Enterprise(**zgs)
                if not zgs_n.isEnterprise():
                    zgs_n = HeadCompany(**zgs)
                lr = _.pop('法定代表人')
                p = Person(**lr)
                if not p.isPerson():
                    p = Enterprise(**lr)
                    if not p.isEnterprise():
                        p = Related(**lr)
                return dict(
                    head=zgs_n,
                    principal=p,
                    **_
                )

            if isinstance(hs, list):
                hcs += [f(b) for b in hs]
            elif isinstance(hs, dict):
                hcs.append(f(hs))
            else:
                logger.warning('Generally, this type is '
                               'in (dict, list).')
        return hcs

    def get_construction_project(self):
        cps = []
        if '建筑工程项目' in self.content.keys():
            cp = self.get_format_dict(self.content['建筑工程项目'])

            def f(_):
                _js_ = _.pop('建设单位')
                jsdw = Enterprise(**_js_)
                if not jsdw.isEnterprise():
                    jsdw = Related(**_js_)
                return dict(
                    jsdw=jsdw,
                    project=ConstructionProject(**_)
                )

            if isinstance(cp, list):
                cps += [f(b) for b in cp]
            elif isinstance(cp, dict):
                cps.append(f(cp))
            else:
                logger.warning('Generally, this type is '
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
                logger.warning('Generally, this type is '
                               'in (dict, list).')
        return ccs
