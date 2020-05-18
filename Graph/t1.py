# encoding: utf-8
# from Calf.data import BaseModel
#
#
# bm = BaseModel(location='server', tn='PKR')
# bm.add_index([('label', 1)], name='index1')
#
from Graph.entity import entities
from Graph.relationship import relationships


# ets = entities()
# for k, v in zip(ets.keys(), ets.values()):
#     ats = v.ATTRIBUTES
#     print('{}({})'.format(k, str(v.__doc__).strip().replace('\n', '')))
#     # print('"{}()":'.format(k), '{')
#     # print('"{}":"{}",'.format(k, str(v.__doc__).replace('\n', '')).replace(' ', ''))
#     for a in ats:
#         # if 'DATE' in a[1]:
#             print('     |_ {}: {}'.format(a[1], a[0]))
#     # print('},')
#     pass
rsp = relationships()
for k, v in zip(rsp.keys(), rsp.values()):
    print('{}({})'.format(v.name, str(v.__doc__).strip().replace('\n', '')).replace(' ', ''))
    try:
        ats = v.ATTRIBUTES
        for a in ats:
            # if 'DATE' in a[1]:
                print('     |_ {}: {}'.format(a[1], a[0]))
    except Exception:
        pass
nds = {
    "Address":"地址",
    "Email":"邮箱",
    "Telephone":"电话",
    "Website":"网站",
    "Person":"自然人",
    "ShareHolder":"股东",
    "JusticeCase":"司法案件",
    "Ruling":"裁决文书",
    "RulingText":"裁决文书全文",
    "Punishment":"行政处罚",
    "Involveder":"案件参与者",
    "Possession":"股权出质标的",
    "ExecutedPerson":"失信被执行人",
    "Invested":"被投资对象",
    "Enterprise":"公司",
    "Industry":"行业",
    "Certificate":"资质证书",
    "Patent":"专利",
    "Trademark":"商标",
    "App":"app",
    "WorkCopyRight":"作品著作权",
    "SoftCopyRight":"软件著作权",
    "OfficialAccount":"公众号",
    "Applets":"小程序",
    "Weibo":"微博",
    "Bidding":"招投标信息",
    "Check":"抽查检查",
    "RandomCheck":"双随机抽查",
    "Client":"客户",
    "IAE":"进出口信息",
    "License":"行政许可",
    "Recruitment":"招聘信息",
    "Supplier":"供应商",
    "TaxCredit":"税务信用",
    "News":"新闻",
}
# for k, v in zip(nds.keys(), nds.values()):
#     print('"{}":"{}",'.format(v, k))
