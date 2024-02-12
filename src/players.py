import random
from src.utils import underline
import config as conf

class Player(object):
    """
    Player consists of a list of cards representing a players hand cards.
    Player can have a name, hand, playable hand. Thereform the players' state can be determined.
    """
    
    def __init__(self, name):
        self.name         = name
        self.hand         = list()
        self.hand_play    = list()
        self.card_play    = 0
        self.action       = 0
    
    def evaluate_hand(self, card_open):
        """
        Loops through each card in players' hand. Evaluation depends on card open.
        Required parameters: card_open as card
        """

        self.hand_play.clear()
        for card in self.hand:
            if card.evaluate_card(card_open.color, card_open.value) == True:
                self.hand_play.append(card)
    
    def draw(self, deck, card_open):
        """
        Adds a card to players' hand and evaluates the hand
        Required parameters:
            - deck as deck
            - card_open as card
        """
        
        card = deck.draw_from_deck()
        self.hand.append(card)
        self.evaluate_hand(card_open)
        print (f'{self.name} draws {card.print_card()}')
        
    def play_highest(self, deck):
        points = {i: i for i in range(0, 10)}
        points.update({"REV": 20, "SKI": 20, "PL2": 20, "COL": 50, "PL4": 50})
        highest = self.hand_play[0]
        for card in self.hand_play[1:]:
            if points[card.value] > points[highest.value]:
                highest = card
        self.card_play = highest
        self.hand.remove(highest)
        self.hand_play.remove(highest)
        deck.discard(highest)
        print(f'\n{self.name} plays {highest.print_card()}')

        self.wild_choice()

    def wild_choice(self):
        if conf.skill["wild_color"]:
            if self.name == conf.player_name_1:
                if (self.card_play.color == "WILD"):
                        self.card_play.color = self.choose_color()
            else:
                if (self.card_play.color == "WILD"):
                        self.card_play.color = random.choice(["RED","GRE","BLU","YEL"])
        else:
            if (self.card_play.color == "WILD") or (self.card_play.value == "PL4"):
                self.card_play.color = random.choice(["RED","GRE","BLU","YEL"])

    def play_rand(self, deck, card_open):

        """
        Reflecting a players' random move, that consists of:
            - Shuffling players' hand cards
            - Lopping through hand cards and choosing the first available hand card to be played
            - Remove card from hand & replace card_open with it
        
        Required parameters: deck as deck
        """
        if conf.skill["highest_card"] and self.name == conf.player_name_1:
            self.play_highest(deck)
            return
        random.shuffle(self.hand_play)
        for card in self.hand:
            if card == self.hand_play[-1]:
                self.card_play = card
                self.hand.remove(card)
                self.hand_play.pop()
                deck.discard(card)
                print (f'\n{self.name} plays {card.print_card()}')
                break

        self.wild_choice()


    def play_counter(self, deck, card_open, plus_card):
        """
        Reflecting a players' counter move to a plus card.
        Required parameters:
            - deck as deck
            - card_open as card
            - plus_card as card
        """
        
        for card in self.hand:
            if card == plus_card:
                self.card_play = card
                self.hand.remove(card)
                deck.discard(card)
                self.evaluate_hand(card_open)
                print (f'{self.name} counters with {card.print_card()}')
                break
        
    def choose_color(self):
        """
        Chooses a card color when a player plays PL4 or WILD COL.
        Color is determined by the majority color in the active players' hand.
        """
        
        colors = [card.color for card in self.hand if card.color in ["RED","GRE","BLU","YEL"]]
        if len(colors)>0:
            max_color = max(colors, key = colors.count)
        else:
            max_color = random.choice(["RED","GRE","BLU","YEL"])

        print (f'{self.name} chooses {max_color}')
        return max_color
    
    def show_hand(self):
        underline (f'\n{self.name}s hand:')
        for card in self.hand:
            card.show_card()
        
    def show_hand_play(self, card_open):
        underline (f'\n{self.name}s playable hand:')
        self.evaluate_hand(card_open)
        for card in self.hand_play:
            card.show_card()