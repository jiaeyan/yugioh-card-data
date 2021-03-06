import json
import re

from yugioh.constants import *
from yugioh.cards.info_decoder import Interpreter

# command line: sqlite3 data.cdb .dump > data.sql
# id: [name, description, ot, alias, set, card_type, atk, def, level, race, atrr, effect_category]


class CardCollector(object):
    """ This class provides functions to collect YuGiOh card data from YGOPro ADS, and also writing function to record
        in disk.

        Attributes:
            monster_database: the card database of monsters in YuGiOh.
            spell_database: the card database of spell in YuGiOh.
            trap_database: the card database of trap in YuGiOh.
    """

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
        """ The core function of this class, collects card data from YGOPro ADS SQL database. """
        card_database = self.read_card_database(sql_f)
        decoder = Interpreter(conf_f)
        card_templates = decoder.interpret_digits(card_database)
        cards = decoder.make_cards(card_templates)
        self.classify_cards(cards)

    @staticmethod
    def read_card_database(sql_f):
        """ Parses a card sql database, gets the raw card info purely with digits. """
        count = 0
        with open(sql_f, 'r') as f:
            card_dict = {}
            for line in f:
                if line.startswith('INSERT'):
                    values = re.findall(r'VALUES\((.+)\)', line.strip())[0]
                    if "''" in values:
                        count += 1
                        card_id, card_name, card_info = values.split(',', maxsplit=2)
                        description = re.findall(r'\'(.+?)\'', card_info)[0]  # .replace(',', '，')
                        card_dict[card_id] = [card_name[1:-1], description]
                    else:
                        fields = values.split(',')
                        card_dict[fields[0]] += list(map(lambda x: int(x), fields[1:]))
        print('Total number of cards:', count)
        return card_dict

    def classify_cards(self, cards):
        """ Given a list of card attribute dictionaries, classifies them into different types, e.g., monster, spell,
            trap.
        """
        for card in cards:
            if card[CARD_TYPE].startswith(MONSTER):
                self.add_monster_card(card)
            else:
                self.add_spell_trap_card(card)

    def add_monster_card(self, card):
        """ Adds a monster card into corresponding sub type in the monster card database. """
        types = card[CARD_TYPE].split('|')
        try:
            sub_type = types[-1]
            self.monster_database[sub_type].append(card)
        except KeyError:
            sub_type = types[1]
            self.monster_database[sub_type].append(card)

    def add_spell_trap_card(self, card):
        """ Adds a spell/trap card into corresponding sub type in the spell/trap card database. """
        types = card[CARD_TYPE].split('|')
        sub_type = NORMAL if len(types) == 1 else types[-1]

        if card[CARD_TYPE].startswith(SPELL):
            self.spell_database[sub_type].append(card)
        else:
            self.trap_database[sub_type].append(card)

    def write_data(self, json_=True, txt=True):
        if json_:
            for fn, db in [('data/cards/monster.json', self.monster_database),
                           ('data/cards/spell.json', self.spell_database),
                           ('data/cards/trap.json', self.trap_database)]:
                with open(fn, 'w') as f:
                    json.dump(db, f, indent=4, sort_keys=True)

        if txt:
            for fn, db in [('data/cards/monster.txt', self.monster_database),
                           ('data/cards/spell.txt', self.spell_database),
                           ('data/cards/trap.txt', self.trap_database)]:
                with open(fn, 'w') as f:
                    for sub_type, cards in db.items():
                        f.write(sub_type + '\n')
                        for card in cards:
                            for var, val in card.items():
                                f.write('\t' + var + ': ' + str(val) + '\n')
                            f.write('\n')






