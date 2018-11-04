import json
import re

from yugioh.constants import *
from yugioh.cards.info_decoder import Interpreter

# command line: sqlite3 card_data.cdb .dump > card_data.sql
# id: [name, description, ot, alias, set, card_type, atk, def, level, race, atrr, effect_category]


class CardCollector(object):

    def __init__(self):
        self.monster_database = self.init_monster_database()
        self.spell_database = self.init_spell_database()
        self.trap_database = self.init_trap_database()

    @staticmethod
    def init_monster_database():
        monster_database = {
            NORMAL: [],
            EFFECT: [],
            RITUAL: [],
            FUSION: [],
            SYNCHRO: [],
            XYZ: [],
            PENDULUM: [],
            LINK: [],
        }
        return monster_database

    @staticmethod
    def init_spell_database():
        spell_database = {
            NORMAL: [],
            RITUAL: [],
            QUICKPLAY: [],
            EQUIP: [],
            CONTINUOUS: [],
            FIELD: [],
        }
        return spell_database

    @staticmethod
    def init_trap_database():
        trap_database = {
            NORMAL: [],
            COUNTER: [],
            CONTINUOUS: [],
        }
        return trap_database

    def collect_cards(self, sql_f, conf_f):
        card_database = self.read_card_database(sql_f)
        decoder = Interpreter(conf_f)
        card_templates = decoder.interpret_digits(card_database)
        cards = decoder.make_cards(card_templates)
        self.classify_cards(cards)

    @staticmethod
    def read_card_database(sql_f):
        """ Parses a card sql database, gets the raw card info purely with digits.
        """
        count = 0
        with open(sql_f, 'r') as f:
            card_dict = {}
            for line in f:
                if line.startswith('INSERT'):
                    values = re.findall(r'VALUES\((.+)\)', line.strip())[0]
                    fields = values.split(',')
                    if "''" in fields:
                        # attaches card ID, name and description to the card dict
                        count += 1
                        card_dict[fields[0]] = list(map(lambda x: re.findall(r'\'(.+?)\'', x)[0], fields[1:3]))
                    else:
                        # attaches other raw card info in digit form to the card dict
                        card_dict[fields[0]] += list(map(lambda x: int(x), fields[1:]))
        print('Total number of cards:', count)
        return card_dict

    def classify_cards(self, cards):
        for card in cards:
            if card[CARD_TYPE].startswith(MONSTER):
                self.add_monster_card(card)
            else:
                self.add_spell_trap_card(card)

    def add_monster_card(self, card):
        types = card[CARD_TYPE].split('|')
        try:
            sub_type = types[-1]
            self.monster_database[sub_type].append(card)
        except KeyError:
            sub_type = types[1]
            self.monster_database[sub_type].append(card)

    def add_spell_trap_card(self, card):
        types = card[CARD_TYPE].split('|')
        sub_type = NORMAL if len(types) == 1 else types[-1]

        if card[CARD_TYPE].startswith(SPELL):
            self.spell_database[sub_type].append(card)
        else:
            self.trap_database[sub_type].append(card)

    def write_data(self, json_=True, txt=True):
        if json_:
            for fn, db in [('card_data/monster.json', self.monster_database),
                           ('card_data/spell.json', self.spell_database),
                           ('card_data/trap.json', self.trap_database)]:
                with open(fn, 'w') as f:
                    json.dump(db, f, indent=4, sort_keys=True)

        if txt:
            for fn, db in [('card_data/monster.txt', self.monster_database),
                           ('card_data/spell.txt', self.spell_database),
                           ('card_data/trap.txt', self.trap_database)]:
                with open(fn, 'w') as f:
                    for sub_type, cards in db.items():
                        f.write(sub_type + '\n')
                        for card in cards:
                            for var, val in card.items():
                                f.write('\t' + var + ': ' + str(val) + '\n')
                            f.write('\n')






