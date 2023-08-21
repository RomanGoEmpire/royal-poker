import random

from card import Card

CARD_RANKS = ['A', 'K', 'Q', 'J', 'T']
CARD_SUITS = ['C', 'H', 'S', 'D']


class Deck:
    def __init__(self):
        self.deck = self.init_deck()

    def init_deck(self):
        deck = [(Card(rank, suit)) for suit in CARD_SUITS for rank in CARD_RANKS]
        shuffled_deck = list(deck)
        random.shuffle(shuffled_deck)
        return shuffled_deck

    def get_card(self):
        return self.deck.pop()

    def deal_cards(self, num):
        return [self.get_card() for _ in range(num)]
