from source_loader import read_conf
from constants import *


# parse integer info to card info
def convert_int_info(conf_f, cards):
    attributes, races, card_types, effect_categories, setnames, ot = read_conf(conf_f)
    for k, v in cards.items():
        v[-1] = get_card_info(v[-1], effect_categories, info_type=EFFECT_CATEGORY)
        v[-2] = get_card_info(v[-2], attributes, info_type=ATTRIBUTE)
        v[-3] = get_card_info(v[-3], races, info_type=RACE)
        v[-4] = get_level(v[-4])
        v[-7] = get_card_info(v[-7], card_types, info_type=CARD_TYPE)
        v[-8] = get_setname(v[-8], setnames)
        v[-9] = str(v[-9]) if v[-9] else ''
        v[-10] = ot[v[-10]]
        cards[k] = v


def get_level(level_code):
    level = level_code & 0xff
    rscale = (level_code >> 24) & 0xff
    lscale = (level_code >> 16) & 0xff
    return level, rscale, lscale


def get_card_info(code, checklist, info_type=None):
    fil = 1
    i = 0

    upto = 1
    if info_type == EFFECT_CATEGORY:
        upto = 0x100000000
    elif info_type == CARD_TYPE:
        upto = 0x8000000
    elif info_type == RACE:
        upto = 0x2000000
    elif info_type == ATTRIBUTE:
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


def specialize_monster_info(card, card_info, defense):
    # the order of the monster type list is reversed of the 'strings.conf' file, which means the foremost
    # type determines the final type of the monster if multiple types applied
    for monster_type in [LINK, PENDULUM, XYZ, FUSION, SYNCHRO, RITUAL, EFFECT, NORMAL]:
        if monster_type in card[CARD_TYPE]:
            if monster_type == LINK:
                card[DEFENSE] = '-'
                card[LINK_NUMBER] = card_info[-4][0]
                card[LINK_DIRECTIONS] = get_link_directions(defense)

            else:
                card[DEFENSE] = defense
                size = RANK if monster_type == XYZ else LEVEL
                card[size] = card_info[-4][0]

                if monster_type == PENDULUM:
                    card[SCALE] = card_info[-4][1]

            return monster_type


def get_link_directions(link_marker):

    directions = []
    if link_marker & LINK_MARKER_TOP:
        directions.append(TOP)
    if link_marker & LINK_MARKER_TOP_LEFT:
        directions.append(TOP_LEFT)
    if link_marker & LINK_MARKER_TOP_RIGHT:
        directions.append(TOP_RIGHT)
    if link_marker & LINK_MARKER_LEFT:
        directions.append(LEFT)
    if link_marker & LINK_MARKER_RIGHT:
        directions.append(RIGHT)
    if link_marker & LINK_MARKER_BOTTOM:
        directions.append(BOTTOM)
    if link_marker & LINK_MARKER_BOTTOM_LEFT:
        directions.append(BOTTOM_LEFT)
    if link_marker & LINK_MARKER_BOTTOM_RIGHT:
        directions.append(BOTTOM_RIGHT)

    return '|'.join(directions)
