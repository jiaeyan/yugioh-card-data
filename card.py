from constants import *


class CardTemplate(object):

    def __init__(self,
                 card_id=None,
                 name=None,
                 description=None,
                 ot=None,
                 alias=None,
                 set_name=None,
                 card_type=None,
                 attack=None,
                 defense=None,
                 size=None,
                 race=None,
                 attribute=None,
                 effect_category=None):

        self.card_id = card_id
        self.name = name
        self.description = description
        self.ot = ot
        self.alias = alias
        self.set_name = set_name
        self.card_type: str = card_type
        self.attack: int = attack
        self.defense: int = defense
        self.size = size
        self.race = race
        self.attribute = attribute
        self.effect_category = effect_category

    def make_card(self):
        if self.card_type.startswith(MONSTER):
            return self.make_monster_card()
        else:
            return self.make_spell_trap_card()

    def get_base_card(self):
        card = {
            NAME: self.name,
            ID: self.card_id,
            DESCRIPTION: self.description,
            OT: self.ot,
            ALIAS: self.alias,
            SET: self.set_name,
            CARD_TYPE: self.card_type,
            EFFECT_CATEGORY: self.effect_category,
        }
        return card

    def make_monster_card(self):
        card = self.get_base_card()
        attack = '?' if self.attack < 0 else self.attack

        card.update({ATTRIBUTE: self.attribute,
                     RACE: self.race,
                     ATTACK: attack})
        self.customize_monster_card(card)
        return card

    def customize_monster_card(self, card):
        defense = '?' if self.defense < 0 else self.defense

        if LINK in self.card_type:
            card[DEFENSE] = '-'
            card[LINK_NUMBER] = self.size[0]
            card[LINK_DIRECTIONS] = self.get_link_directions(defense)
        else:
            card[DEFENSE] = defense
            size = RANK if XYZ in self.card_type else LEVEL
            card[size] = self.size[0]

            if PENDULUM in self.card_type:
                card[SCALE] = self.size[1]

    @staticmethod
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

    def make_spell_trap_card(self):
        card = self.get_base_card()
        return card

