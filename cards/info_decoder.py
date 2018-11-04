import re

from card import CardTemplate
from constants import *


class Interpreter(object):

    def __init__(self, conf_f):
        self.attributes = []
        self.races = []
        self.card_types = []
        self.effect_categories = []
        self.set_names = {}
        self.ot = {}
        self.read_conf(conf_f)

    def read_conf(self, conf_f):
        """ Parses a strings.conf file to get card info.
        """
        self.ot = {1: 'OCG', 2: 'TCG', 3: 'OCG|TCG'}
        with open(conf_f, 'r') as f:
            for line in f:
                if re.match(r'!system 101\d', line):
                    self.attributes.append(line.strip().split()[2])
                elif re.match(r'!system 10[234]\d', line):
                    self.races.append(line.strip().split()[2])
                elif re.match(r'!system 10[5678]\d', line):
                    self.card_types.append(line.strip().split()[2])
                elif re.match(r'!system 11[0123]\d', line):
                    self.effect_categories.append(line.strip().split()[2])
                elif line.startswith('!setname'):
                    set_code, set_name = line.strip().split('\t')[0].split(maxsplit=2)[1:]
                    self.set_names[int(set_code, 16)] = set_name

    def interpret_digits(self, card_database):
        card_templates = []
        for card_id, info in card_database.items():
            info_container = {
                'card_id': card_id,
                'name': info[0],
                'description': info[1].replace(r'\r\n', '\n'),
                'ot': self.ot[info[2]],
                'alias': card_database[str(info[3])][0] if info[3] else '',
                'set_name': self.get_set_name(info[4]) if info[4] else '',
                'card_type': self.get_card_info(info[5], self.card_types, info_type=CARD_TYPE),
                'attack': info[6],
                'defense': info[7],
                'size': self.get_size(info[8]),
                'race': self.get_card_info(info[9], self.races, info_type=RACE) if info[9] else '',
                'attribute': self.get_card_info(info[10], self.attributes, info_type=ATTRIBUTE) if info[10] else '',
                'effect_category': self.get_card_info(info[11], self.effect_categories, info_type=EFFECT_CATEGORY) if info[11] else ''
            }
            card_template = CardTemplate(**info_container)
            card_templates.append(card_template)
        return card_templates

    @staticmethod
    def make_cards(card_templates):
        cards = [card_template.make_card() for card_template in card_templates]
        return cards

    def get_set_name(self, set_code):
        res = []
        for i in range(4):
            code = (set_code >> i * 16) & 0xffff
            name = self.set_names.get(code, None)
            if name:
                res.append(name)
        return '|'.join(res)

    @staticmethod
    def get_card_info(code, checklist, info_type=None):
        res = []
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

        while fil != upto:
            if code & fil:
                res.append(checklist[i])
            fil <<= 1
            i += 1

        return '|'.join(res)

    @staticmethod
    def get_size(size_code):
        size = size_code & 0xff
        rscale = (size_code >> 24) & 0xff
        lscale = (size_code >> 16) & 0xff
        return size, rscale, lscale

