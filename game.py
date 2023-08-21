from deck import Deck

HAND_RATING = ['Royal Flush', 'Four of a Kind', 'Full House', 'Straight', 'Two Pair']
CARD_RANKS = ['A', 'K', 'Q', 'J', 'T']
CARD_SUITS = ['C', 'H', 'S', 'D']


def sort_by_suite(cards):
    return sorted(cards, key=lambda card: (CARD_SUITS.index(card.suit), CARD_RANKS.index(card.rank)))


def sort_by_rank(cards):
    return sorted(cards, key=lambda card: CARD_RANKS.index(card.rank))


def is_royal_flush(cards, ranks):
    if not is_straight(ranks):
        return False
    suite_count = {'C': 0, 'H': 0, 'S': 0, 'D': 0}
    for card in cards:
        suite_count[card.suit] += 1
    # check if there are 5 cards with the same suite
    if 5 not in suite_count.values():
        return False
    # get the suite of the royal flush
    royal_flush_suite = [k for k, v in suite_count.items() if v == 5][0]
    # get the cards with the royal flush suite
    royal_flush_cards = [card for card in cards if card.suit == royal_flush_suite]
    return len(royal_flush_cards) == 5


def is_four_of_a_kind(ranks):
    return list(ranks.values())[0] == 4


def is_full_house(ranks):
    return list(ranks.values())[0] == 3 and list(ranks.values())[1] >= 2


def is_straight(ranks):
    return 0 not in ranks.values()


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
    return sort_by_rank(ordered_cards)


def is_two_pair(ranks):
    return list(ranks.values()).count(2) >= 2


def get_four_of_a_kind_card_order(cards, ranks):
    ordered_cards = []
    remove_cards = []
    for card in cards:
        if card.rank == list(ranks.keys())[0]:
            ordered_cards.append(card)
            remove_cards.append(card)
    for card in remove_cards:
        cards.remove(card)
    ordered_cards.append(sort_by_rank(cards)[0])
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
    ordered_cards.append(sort_by_rank(cards)[0])
    return ordered_cards


def get_distribution(cards):
    ranks = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0}
    for card in cards:
        ranks[card.rank] += 1
    # sort the ranks by the amount of cards
    return {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}


def get_best(cards):
    ranks = get_distribution(cards)
    if is_royal_flush(cards, ranks):
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
        # # print(ranks)
        return Exception('No best hand')


def select_winner(player_hands, community_cards):
    all_hands = []
    for player_card in player_hands:
        # # print(f'Player {player_hands.index(player_card) + 1} cards: {player_card}')
        cards = player_card + community_cards
        best, card_value = get_best(cards)
        # # print(best, card_value)
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


def play_round(amount_players):
    deck = Deck()

    player_hands = []
    for i in range(amount_players):
        cards = deck.deal_cards(2)
        cards = sort_by_rank(cards)
        player_hands.append(cards)

    community_cards = deck.deal_cards(5)

    # for hand in player_hands:
    #    print(f'Player {player_hands.index(hand) + 1} cards: {hand}')
    # print(f'Community cards: {community_cards}')

    best_hand, indexes = select_winner(player_hands, community_cards)
    # print(f'Best hand: {best_hand}')
    return player_hands, indexes
