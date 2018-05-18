import re

# command line: sqlite3 cards.cdb .dump > cards.sql
# id: [name, effect, ot, alias, set, type, atk, def, level, race, atrr, category]

def read_cdb(sql_f):
    with open(sql_f, 'r') as f:
        cards = {}
        for line in f:
            if line.startswith('INSERT'):
                values = re.findall(r'VALUES\((.+)\)', line.strip())[0]
                fields = values.split(',')
                if "''" in fields:
                    cards[fields[0]] = list(map(lambda x: re.findall(r'\'(.+?)\'', x)[0], fields[1:3]))
                else:
                    cards[fields[0]] += list(map(lambda x: int(x), fields[1:]))
    return cards


def read_conf(conf_f):
    attributes = []
    races = []
    types = []
    categories = []
    setnames = {}
    ot = {1: 'OCG', 2: 'TCG', 3: 'OCG & TCG'}
    with open(conf_f, 'r') as f:
        for line in f:
            if re.match(r'!system 101\d', line):
                attributes.append(line.strip().split()[2])
            elif re.match(r'!system 10[234]\d', line):
                races.append(line.strip().split()[2])
            elif re.match(r'!system 10[5678]\d', line):
                types.append(line.strip().split()[2])
            elif re.match(r'!system 11[0123]\d', line):
                categories.append(line.strip().split()[2])
            elif line.startswith('!setname'):
                k, v = line.strip().split('\t')[0].split(maxsplit=2)[1:]
                setnames[int(k, 16)] = v
    return attributes, races, types, categories, setnames, ot


def get_level(level_code):
    level = level_code & 0xff
    rscale = (level_code >> 24) & 0xff
    lscale = (level_code >> 16) & 0xff
    return level, rscale, lscale


def get_card_info(code, checklist, info_type=None):
    fil = 1
    i = 0

    upto = 1
    if info_type == 'category':
        upto = 0x100000000
    elif info_type == 'type':
        upto = 0x8000000
    elif info_type == 'race':
        upto = 0x2000000
    elif info_type == 'attribute':
        upto = 0x80

    res = []
    while fil != upto:
        if code & fil:
            res.append(checklist[i])
        fil <<= 1
        i += 1
    return '|'.join(res)


def get_setname(setcode, setnames):
    res = []
    for i in range(4):
        code = (setcode >> i * 16) & 0xffff
        name = setnames.get(code, None)
        if name:
            res.append(name)
    return '|'.join(res)


def collect_cards(sql_f, conf_f):
    cards = read_cdb(sql_f)
    convert_int_info(conf_f, cards)

    monster_db = {'通常': {}, '效果': {}, '仪式': {}, '融合': {}, '同调': {}, '超量': {}, '灵摆': {}, '连接': {}}
    spell_db = {'通常': {}, '仪式': {}, '速攻': {}, '装备': {}, '永续': {}, '场地': {}}
    trap_db = {'通常': {}, '反击': {}, '永续': {}}
    for k, v in cards.items():
        if v[-7].startswith('怪兽'):
            add_monster_card(k, v, monster_db)
        elif v[-7].startswith('魔法'):
            add_spell_trap_card(k, v, spell_db)
        elif v[-7].startswith('陷阱'):
            add_spell_trap_card(k, v, trap_db)


def convert_int_info(conf_f, cards):
    attributes, races, types, categories, setnames, ot = read_conf(conf_f)
    for k, v in cards.items():
        v[-1] = get_card_info(v[-1], categories, info_type='category')
        v[-2] = get_card_info(v[-2], attributes, info_type='attribute')
        v[-3] = get_card_info(v[-3], races, info_type='race')
        v[-4] = get_level(v[-4])
        v[-7] = get_card_info(v[-7], types, info_type='type')
        v[-8] = get_setname(v[-8], setnames)
        v[-9] = str(v[-9]) if v[-9] else ''
        v[-10] = ot[v[-10]]
        cards[k] = v


def add_monster_card(card_id, card_info, monster_db):
    pass


def add_spell_trap_card(card_id, card_info, cdb):
    card = {
        '卡名': card_info[0],
        '密码': card_id,
        '效果': card_info[1],
        'OT': card_info[2],
        '同名卡': card_info[3],
        '字段': card_info[4],
        '卡片种类': card_info[5],
        '效果类型': card_info[-1],
    }

    fields = card['卡片种类'].split('|')
    if len(fields) == 1:
        cdb['通常'][card_id] = card
    else:
        cdb[fields[1]][card_id] = card


def debug(sql_f, conf_f):
    cards = read_cdb(sql_f)
    attributes, races, types, categories, setnames, ot = read_conf(conf_f)

    attr_codes = set()
    race_codes = set()
    level_codes = set()
    type_codes = set()
    cate_codes = set()
    set_codes = set()
    for v in cards.values():
        cate_codes.add(v[-1])
        attr_codes.add(v[-2])
        race_codes.add(v[-3])
        level_codes.add(v[-4])
        type_codes.add(v[-7])
        set_codes.add(v[-8])

    attr_codes = sorted(list(attr_codes))
    race_codes = sorted(list(race_codes))
    level_codes = sorted(list(level_codes))
    type_codes = sorted(list(type_codes))
    cate_codes = sorted(list(cate_codes))
    set_codes = sorted(list(set_codes))

    print('testing attr...')
    print('attr num:', len(attributes))
    print('attr code num:', len(attr_codes))
    for attr in attr_codes:
        print(attr, get_card_info(attr, attributes, info_type='attribute'))
    print()

    print('testing race...')
    print('race num:', len(races))
    print('race code num:', len(race_codes))
    for race in race_codes:
        print(race, get_card_info(race, races, info_type='race'))
    print()

    print('testing cate...')
    print('cate num:', len(categories))
    print('cate code num:', len(cate_codes))
    for cate in cate_codes:
        print(cate, get_card_info(cate, categories, info_type='category'))
    print()

    print('testing type...')
    print('type num:', len(types))
    print('type code num:', len(type_codes))
    for type in type_codes:
        print(type, get_card_info(type, types, info_type='type'))
    print()

    print('testing set...')
    print('set num:', len(setnames))
    print('set code num:', len(set_codes))
    for s in set_codes:
        if s:
            print(s, get_setname(s, setnames))
    print()

    print('tesing level...')
    print('level num:', len(level_codes))
    for l in level_codes:
        print(l, get_level(l))
    print()


# collect_cards('cards.sql', 'strings.conf')
# debug('cards.sql', 'strings.conf')
print(135 & LINK_MARKER_TOP_LEFT)