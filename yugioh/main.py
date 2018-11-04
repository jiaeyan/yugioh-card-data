from yugioh.cards.card_collector import CardCollector


def main():
    yugioh = CardCollector()
    yugioh.collect_cards('resources/cards.sql', 'resources/strings.conf')
    yugioh.write_data()


if __name__ == '__main__':
    main()
