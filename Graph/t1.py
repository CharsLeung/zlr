# # encoding: utf-8
# # from Calf.data import BaseModel
# #
# #
# # bm = BaseModel(location='server', tn='PKR')
# # bm.add_index([('label', 1)], name='index1')
# #
# from Graph.entity import entities
# from Graph.relationship import relationships
#
#
# ets = entities()
# for k, v in zip(ets.keys(), ets.values()):
#     ats = v.ATTRIBUTES
#     # print('{}({})'.format(k, str(v.__doc__).strip().replace('\n', '')))
#     # print('"{}()":'.format(k), '{')
#     # print('"{}":"{}",'.format(str(v.__doc__)
#     #                           .replace('\n', '')
#     #                           .replace(' ', '')
#     #                           .split('，')[0], k))
#     # for a in ats:
#     #     # if 'DATE' in a[1]:
#     #         print('     |_ {}: {}'.format(a[1], a[0]))
#
#     # print('"{}": '.format(k), '{')
#     # for a in ats:
#     #     print('     "{}": "{}",'.format(a[1], a[0]))
#     # print('},')
#     pass
# rsp = relationships()
# for k, v in zip(rsp.keys(), rsp.values()):
#     # print('{}({})'.format(v.name, str(v.__doc__).strip().replace('\n', '')).replace(' ', ''))
#     try:
#         # ats = v.ATTRIBUTES
#         # for a in ats:
#         #     # if 'DATE' in a[1]:
#         #         print('     |_ {}: {}'.format(a[1], a[0]))
#         print('"{}": "{}",'.format(v.name, str(v.__doc__).strip().replace('\n', '')).replace(' ', ''))
#     except Exception:
#         pass
ds = [{'A': 1, 'B': 2}, {'A': 2}]