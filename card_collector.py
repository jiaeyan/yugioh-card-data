import json
from constants import *
from source_loader import read_cdb
from info_interpreter import convert_int_info, specialize_monster_info

# command line: sqlite3 cards.cdb .dump > cards.sql
# id: [name, effect, ot, alias, set, type, atk, def, level, race, atrr, category]


def collect_cards(sql_f, conf_f):
    cards = read_cdb(sql_f)
    convert_int_info(conf_f, cards)

    monster_db, spell_db, trap_db = db_init()

    for k, v in cards.items():

        if v[-7].startswith(MONSTER):
            add_monster_card(k, v, monster_db)

        elif v[-7].startswith(SPELL):
            add_spell_trap_card(k, v, spell_db)

        elif v[-7].startswith(TRAP):
            add_spell_trap_card(k, v, trap_db)

    write_data(monster_db, spell_db, trap_db, json_=True, txt=True)


def db_init():
    monster_db = {
        NORMAL: {},
        EFFECT: {},
        RITUAL: {},
        FUSION: {},
        SYNCHRO: {},
        XYZ: {},
        PENDULUM: {},
        LINK: {},
    }

    spell_db = {
        NORMAL: {},
        RITUAL: {},
        QUICKPLAY: {},
        EQUIP: {},
        CONTINUOUS: {},
        FIELD: {},
    }

    trap_db = {
        NORMAL: {},
        COUNTER: {},
        CONTINUOUS: {},
    }

    return monster_db, spell_db, trap_db


def add_monster_card(card_id, card_info, monster_db):
    attack = '?' if card_info[-6] < 0 else card_info[-6]
    defense = '?' if card_info[-5] < 0 else card_info[-5]

    card = {
        NAME: card_info[0],
        ID: card_id,
        EFFECT: card_info[1],
        OT: card_info[2],
        ALIAS: card_info[3],
        SET: card_info[4],
        TYPE: card_info[5],
        ATTRIBUTE: card_info[-2],
        RACE: card_info[-3],
        EFFECT_CATEGORY: card_info[-1],
        ATTACK: attack,
    }

    monster_type = specialize_monster_info(card, card_info, defense)
    monster_db[monster_type][card_id] = card


def add_spell_trap_card(card_id, card_info, cdb):
    card = {
        NAME: card_info[0],
        ID: card_id,
        EFFECT: card_info[1],
        OT: card_info[2],
        ALIAS: card_info[3],
        SET: card_info[4],
        TYPE: card_info[5],
        EFFECT_CATEGORY: card_info[-1],
    }

    fields = card[TYPE].split('|')
    card_type = NORMAL if len(fields) == 1 else fields[1]
    cdb[card_type][card_id] = card


def write_data(monster_db, spell_db, trap_db, json_=True, txt=True):
    if json_:
        for fn, db in [('cards/monster.json', monster_db), ('cards/spell.json', spell_db), ('cards/trap.json', trap_db)]:
            with open(fn, 'w') as f:
                json.dump(db, f, indent=4, sort_keys=True)

    if txt:
        for fn, db in [('cards/monster.txt', monster_db), ('cards/spell.txt', spell_db), ('cards/trap.txt', trap_db)]:
            with open(fn, 'w') as f:
                for k, v in db.items():
                    f.write(k + '\n')
                    for cid, cinfo in v.items():
                        f.write('\t' + cid + '\n')
                        for cname, cstr in cinfo.items():
                            f.write('\t\t' + cname + ': ' + str(cstr) + '\n')


