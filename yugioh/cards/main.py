import argparse
import os

from yugioh.cards.card_collector import CardCollector


def main(sql_path, conf_path):
    """ Please make sure that before collecting cards, you have card.sql converted under your YGOPro root directory. """
    card_collector = CardCollector()
    card_collector.collect_cards(sql_path, conf_path)
    card_collector.write_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collects cards from YGOPro ADS SQL database.')
    parser.add_argument('ygo_root_dir', help='the root directory of the YGOPro ADS')
    args = parser.parse_args()

    ygo_root_dir = args.ygo_root_dir
    sql_path = os.path.join(ygo_root_dir, 'cards.sql')
    conf_path = os.path.join(ygo_root_dir, 'strings.conf')
    # sql_path = 'resources/cards.sql'
    # conf_path = 'resources/strings.conf'

    main(sql_path, conf_path)
