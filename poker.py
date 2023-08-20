import random

from card import Card

HAND_RATING = ['Royal Flush', 'Four of a Kind', 'Full House', 'Straight', 'Two Pair']
CARD_RANKS = ['A', 'K', 'Q', 'J', 'T']


def create_deck():
    deck = []
    for suit in ['C', 'D', 'H', 'S']:
        for rank in ['T', 'J', 'Q', 'K', 'A']:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck


def get_distribution(cards):
    ranks = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0}
    for card in cards:
        ranks[card.rank] += 1
    # sort the ranks by the amount of cards
    return {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}


def is_royal_flush(cards):
    """
    >>> is_royal_flush([Card('T', 'C'), Card('J', 'C'), Card('Q', 'C'), Card('K', 'C'), Card('A', 'C'), Card('T', 'D'), Card('J', 'S')])
    True
    >>> is_royal_flush([Card('T', 'C'), Card('J', 'C'), Card('Q', 'C'), Card('K', 'C'), Card('A', 'D'), Card('T', 'D'), Card('J', 'S')])
    False
    """
    suits = {'C': 0, 'D': 0, 'H': 0, 'S': 0}
    for card in cards:
        suits[card.suit] += 1
    has_same_suit = 5 in suits.values()
    # suit that has 5 cards
    suit = ''
    for key, value in suits.items():
        if value == 5:
            suit = key
            break
    if not has_same_suit:
        return False
    ranks = ['T', 'J', 'Q', 'K', 'A']
    for card in cards:
        if card.rank in ranks and card.suit == suit:
            ranks.remove(card.rank)
    return len(ranks) == 0


def is_four_of_a_kind(ranks):
    """
    >>> is_four_of_a_kind({'T': 4, 'J': 1, 'Q': 2, 'K': 0, 'A': 0})
    True
    >>> is_four_of_a_kind({'T': 3, 'J': 1, 'Q': 2, 'K': 1, 'A': 0})
    False
    """
    # check if the first key has 4 cards
    return list(ranks.values())[0] == 4


def is_full_house(ranks):
    """
    >>> is_full_house({'T': 3, 'Q': 2,'J': 1 , 'K': 0, 'A': 0})
    True
    >>> is_full_house({'T': 3, 'Q': 3,'J': 1,  'K': 0, 'A': 0})
    True
    >>> is_full_house({'T': 2, 'J': 1, 'Q': 2, 'K': 1, 'A': 0})
    False
    """
    return list(ranks.values())[0] == 3 and list(ranks.values())[1] >= 2


def is_straight(ranks):
    """
    >>> is_straight({'T': 1, 'J': 1, 'Q': 1, 'K': 1, 'A': 2})
    True
    >>> is_straight({'T': 1, 'J': 1, 'Q': 1, 'K': 3, 'A': 0})
    False
    """
    return 0 not in ranks.values()


def is_two_pair(ranks):
    """
    >>> is_two_pair({'T': 2, 'J': 2, 'Q': 2, 'K': 1, 'A': 0})
    True
    >>> is_two_pair({'T': 1, 'J': 1, 'Q': 2, 'K': 1, 'A': 1})
    False
    """
    return list(ranks.values()).count(2) >= 2


def sort_cards(hands):
    # sort the cards by rank
    return sorted(hands, key=lambda card: CARD_RANKS.index(card.rank))


def get_four_of_a_kind_card_order(cards, ranks):
    ordered_cards = []
    remove_cards = []
    for card in cards:
        if card.rank == list(ranks.keys())[0]:
            ordered_cards.append(card)
            remove_cards.append(card)
    for card in remove_cards:
        cards.remove(card)
    ordered_cards.append(sort_cards(cards)[0])
    return ordered_cards


def get_full_house_card_order(cards, ranks):
    ordered_cards = []
    for card in cards:
        if card.rank == list(ranks.keys())[0]:
            ordered_cards.append(card)
    for card in cards:
        if card.rank == list(ranks.keys())[1]:
            ordered_cards.append(card)
    if len(ordered_cards) > 5:
        ordered_cards = ordered_cards[:5]
    return ordered_cards


def get_two_pair_card_order(cards, ranks):
    ordered_cards = []
    remove_cards = []
    for card in cards:
        if card.rank == list(ranks.keys())[0]:
            ordered_cards.append(card)
            remove_cards.append(card)
        if card.rank == list(ranks.keys())[1]:
            ordered_cards.append(card)
            remove_cards.append(card)
    for card in remove_cards:
        cards.remove(card)
    ordered_cards.append(sort_cards(cards)[0])
    return ordered_cards


def get_royal_flush_card_order(cards):
    # suit that has 5 cards
    ordered_cards = []
    suits = {'C': 0, 'D': 0, 'H': 0, 'S': 0}
    for card in cards:
        suits[card.suit] += 1
    # suit that has 5 cards
    suit = ''
    for key, value in suits.items():
        if value == 5:
            suit = key
            break
    for card in cards:
        if card.suit == suit:
            ordered_cards.append(card)
    return sort_cards(ordered_cards)


def get_best(cards):
    ranks = get_distribution(cards)
    if is_royal_flush(cards):
        return 'Royal Flush', get_royal_flush_card_order(cards)
    elif is_four_of_a_kind(ranks):
        return 'Four of a Kind', get_four_of_a_kind_card_order(cards, ranks)
    elif is_full_house(ranks):
        return 'Full House', get_full_house_card_order(cards, ranks)
    elif is_straight(ranks):
        return 'Straight', None
    elif is_two_pair(ranks):
        return 'Two Pair', get_two_pair_card_order(cards, ranks)
    else:
        print(ranks)
        return Exception('No best hand')


def select_winner(player_hands, community_cards):
    all_hands = []
    for player_card in player_hands:
        print(f'Player {player_hands.index(player_card) + 1} cards: {player_card}')
        cards = player_card + community_cards
        best, card_value = get_best(cards)
        print(best, card_value)
        all_hands.append((best, card_value))
    # get indexes of best hands with help of HAND_RANKS
    all_indexes = [HAND_RATING.index(hand[0]) for hand in all_hands]
    # get index of best hand
    best_hand_index = min(all_indexes)
    if all_indexes.count(best_hand_index) == 1:
        index_of_best_hand = all_indexes.index(best_hand_index)
        return all_hands[index_of_best_hand], [index_of_best_hand]  # return best hand
    if all_indexes.count(best_hand_index) > 1 and best_hand_index == 0 or best_hand_index == 3:
        indexes_of_best_hands = [i for i, x in enumerate(all_indexes) if x == best_hand_index]
        return all_hands[indexes_of_best_hands[0]], indexes_of_best_hands
    if all_indexes.count(best_hand_index) > 1:
        indexes_of_best_hands = [i for i, x in enumerate(all_indexes) if x == best_hand_index]
        best_hands = [all_hands[index][1] for index in indexes_of_best_hands]
        for i in range(5):
            current_cards = [hand[i] for hand in best_hands]
            current_indexes = [CARD_RANKS.index(card.rank) for card in current_cards]
            best_card_index = min(current_indexes)
            if current_indexes.count(best_card_index) == 1:
                best_hand_index = current_indexes.index(best_card_index)
                return all_hands[best_hand_index], [best_hand_index]
        return all_hands[indexes_of_best_hands[0]], indexes_of_best_hands


def calulate_odds():
    rounds = 10_000_000
    hands = {'Royal Flush': 0, 'Four of a Kind': 0, 'Full House': 0, 'Straight': 0, 'Two Pair': 0}
    for round in range(rounds):
        if round % 10_000 == 0:
            print(round)
        deck = create_deck()
        cards = deck[:7]
        best, card_value = get_best(cards)
        hands[best] += 1
    # print percentage
    for key, value in hands.items():
        length = len(key)
        print(key, ' ' * (15 - length), f"{value / rounds * 100:.4f}%")

    # save results to csv
    with open('poker.csv', 'w') as file:
        for key, value in hands.items():
            file.write(f"{key},{value / rounds * 100}")


def get_index_rank(rank):
    return CARD_RANKS.index(rank)


if __name__ == '__main__':
    # doctest.testmod()

    rounds = 100_000
    players = 2
    hands = {'Royal Flush': 0, 'Four of a Kind': 0, 'Full House': 0, 'Straight': 0, 'Two Pair': 0}
    all_possible_hands = {'AA': 0, 'AK': 0, 'AQ': 0, 'AJ': 0, 'AT': 0,
                          'KK': 0, 'KQ': 0, 'KJ': 0, 'KT': 0,
                          'QQ': 0, 'QJ': 0, 'QT': 0,
                          'JJ': 0, 'JT': 0,
                          'TT': 0}
    open_cards = []
    hand_rank = None
    for round in range(rounds):
        deck = create_deck()
        hands = []
        open_cards = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
        print(f'Open cards: {open_cards}')
        for player in range(players):
            hand = [deck.pop(), deck.pop()]
            hand = sort_cards(hand)
            hands.append(hand)
            if player == 0:
                hand_rank = hand[0].rank, hand[1].rank
        best_hands, player_indexes = select_winner(hands, open_cards)
        for player in player_indexes:
            print(f'Player {player + 1} won!')
        print(f'Won with {best_hands[0]}: {best_hands[1]}')
        print(f'Hand rank: {hand_rank}')
        all_possible_hands[f'{hand_rank[0]}{hand_rank[1]}'] += 1
    print(all_possible_hands)
