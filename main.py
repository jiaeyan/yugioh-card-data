from card_collector import YuGiOh


def main():
    yugioh = YuGiOh()
    yugioh.collect_cards('source/card_data.sql', 'source/strings.conf')
    yugioh.write_data()


if __name__ == '__main__':
    main()
