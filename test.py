# import json
# from source_loader import *
# from info_decoder import *
#
#
# def check_loader_interpreter(sql_f, conf_f):
#     card_data = read_cdb(sql_f)
#     attributes, races, types, categories, setnames, ot = read_conf(conf_f)
#
#     attr_codes = set()
#     race_codes = set()
#     level_codes = set()
#     type_codes = set()
#     cate_codes = set()
#     set_codes = set()
#     for v in card_data.values():
#         cate_codes.add(v[-1])
#         attr_codes.add(v[-2])
#         race_codes.add(v[-3])
#         level_codes.add(v[-4])
#         type_codes.add(v[-7])
#         set_codes.add(v[-8])
#
#     attr_codes = sorted(list(attr_codes))
#     race_codes = sorted(list(race_codes))
#     level_codes = sorted(list(level_codes))
#     type_codes = sorted(list(type_codes))
#     cate_codes = sorted(list(cate_codes))
#     set_codes = sorted(list(set_codes))
#
#     print('testing attr...')
#     print('attr num:', len(attributes))
#     print('attr code num:', len(attr_codes))
#     for attr in attr_codes:
#         print(attr, get_card_info(attr, attributes, info_type='attribute'))
#     print()
#
#     print('testing race...')
#     print('race num:', len(races))
#     print('race code num:', len(race_codes))
#     for race in race_codes:
#         print(race, get_card_info(race, races, info_type='race'))
#     print()
#
#     print('testing cate...')
#     print('cate num:', len(categories))
#     print('cate code num:', len(cate_codes))
#     for cate in cate_codes:
#         print(cate, get_card_info(cate, categories, info_type='category'))
#     print()
#
#     print('testing type...')
#     print('type num:', len(types))
#     print('type code num:', len(type_codes))
#     for type_ in type_codes:
#         print(type_, get_card_info(type_, types, info_type='type'))
#     print()
#
#     print('testing set...')
#     print('set num:', len(setnames))
#     print('set code num:', len(set_codes))
#     for s in set_codes:
#         if s:
#             print(s, get_setname(s, setnames))
#     print()
#
#     print('tesing level...')
#     print('level num:', len(level_codes))
#     for l in level_codes:
#         print(l, get_level(l))
#     print()
#
#
# def check_result():
#     with open('card_data/monster.json') as f:
#         m = json.load(f)
#
#     with open('card_data/spell.json') as f:
#         s = json.load(f)
#
#     with open('card_data/trap.json') as f:
#         t = json.load(f)
#
#     c = sum([len(v) for d in [m, s, t] for v in d.values()])
#
#     print(c)
B = 'b'
class A(object):
    a = 'a'

    def __init__(self):
        self.B = 1
        self.c = [1,2,3]
a = A()
print(a.__class__.__dict__)