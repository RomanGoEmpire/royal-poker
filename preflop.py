from game import play_round


def initialize_table():
    return {'AA': 0, 'AK': 0, 'AQ': 0, 'AJ': 0, 'AT': 0,
            'KK': 0, 'KQ': 0, 'KJ': 0, 'KT': 0,
            'QQ': 0, 'QJ': 0, 'QT': 0,
            'JJ': 0, 'JT': 0,
            'TT': 0}


def convert_to_table_string(winner):
    return f'{winner[0].rank}{winner[1].rank}'


played_amount = initialize_table()
won_amount = initialize_table()
even_amount = initialize_table()
lost_amount = initialize_table()


def preflop(rounds, amount_player):
    rounds_to_print = rounds / 100
    for round in range(rounds):
        if round % rounds_to_print == 0:
            print(f'{round / rounds * 100:.0f}%')
        hands, winner_indexes = play_round(amount_player)
        for index, hand in enumerate(hands):
            if index in winner_indexes and len(winner_indexes) == 1:
                won_amount[convert_to_table_string(hand)] += 1
            elif index in winner_indexes and len(winner_indexes) > 1:
                even_amount[convert_to_table_string(hand)] += 1
            else:
                lost_amount[convert_to_table_string(hand)] += 1
            played_amount[convert_to_table_string(hand)] += 1

    for key, value in played_amount.items():
        print(key,
              f"W: {won_amount[key] / value * 100:.0f}% S: {even_amount[key] / value * 100:.0f}% L: {lost_amount[key] / value * 100:.0f}%")

    file = f'{amount_player}_preflop.csv'
    with open(file, 'w') as file:
        file.write('Hand,Played,Won,Even,Lost\n')
        for key, value in played_amount.items():
            file.write(
                f"{key},{value},{won_amount[key] / value * 100:.1f}%,{even_amount[key] / value * 100:.1f}%,{lost_amount[key] / value * 100:.1f}%\n")


if __name__ == '__main__':
    preflop(1_000_000, 2)
