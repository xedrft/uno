import random
import config as conf
class Card(object):
    """
    Card is represented as tuple with properties 'color' and 'value'.
    Card can be evaluated if playable.
    """
    def __init__(self, c, v):
        self.color = c
        self.value = v

    def evaluate_card(self, open_c, open_v):
        if (
            (self.color == open_c) or
            (self.value == open_v) or
            (self.value in ["COL","PL4"])
        ):
            return True

    def show_card(self):
        print (self.color, self.value)

    def print_card(self):
        return str(self.color) + " " + str(self.value)

    def __repr__(self):
        return f"Card(color={self.color}, value={self.value})"


class Deck(object):
    """
    Deck consists of list of cards. Is initialized with standard list of cards.
    Deck can be shuffled, drawn from.
    """
    def __init__(self, player_1, player_2):
        self.cards = []
        self.cards_disc = []
        self.cards_all = []
        self.player_1 = player_1
        self.player_2 = player_2
        self.build()
        self.shuffle()

    def build(self):
        colors = ["RED","GRE","BLU","YEL"]

        cards_zero   = [Card(c,0) for c in colors]
        cards_normal = [Card(c,v) for c in colors for v in range (1,10)]*2
        cards_action = [Card(c,v) for c in colors for v in ["SKI","REV","PL2"]]*2
        cards_wild   = [Card("WILD",v) for v in ["COL","PL4"]]*4

        self.cards_all = cards_normal + cards_action + cards_zero + cards_wild
        for card in self.cards_all: self.cards.append(card)

    def discard(self, card):
        self.cards_disc.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_from_deck(self):
        if len(self.cards) == 0:
            if len(self.cards_disc) == 0:
                print("Both decks are empty. Restarting the game.")
                self.player_1.hand = list()
                self.player_2.hand = list()
                self.build()
                self.shuffle()
            else:
                self.cards = self.cards_disc
                self.cards_disc = []
                self.shuffle()
                for card in self.cards:
                    if card.value in ["COL", "PL4"]:
                        card.color = "WILD"
                        print(list(cardss.color for cardss in self.cards))

        return self.cards.pop()

    def show_deck(self):
        for c in self.cards:
            c.show_card()

    def show_discarded(self):
        for c in self.cards_disc:
            c.show_card()