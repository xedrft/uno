import random
from src.utils import underline
import json

with open('config.json', 'r') as file:
    data = json.load(file)

draw_state = data["luck"]["lucky_draws"]["state"]
draw_luck = data["luck"]["lucky_draws"]["luck"]
unfavor = data["skill"]["disfavor_wild"]
color = data["skill"]["wild_color"]
highest = data["skill"]["highest_card"]
skip = data["skill"]["skip_chain"]
plus = data["skill"]["plus_uno"]
player_name_1 = data["player_name_1"]
player_name_2 = data["player_name_2"]



class Player(object):
    """
    Player consists of a list of cards representing a players hand cards.
    Player can have a name, hand, playable hand. Thereform the players' state can be determined.
    """

    def __init__(self, name):
        self.name = name
        self.hand = list()
        self.hand_play = list()
        self.card_play = 0
        self.action = 0
        self.majority_color = list()

    def return_hand(self):
        return self.hand



    def evaluate_hand(self, card_open):
        """
        Loops through each card in players' hand. Evaluation depends on card open.
        Required parameters: card_open as card
        """

        self.hand_play.clear()
        for card in self.hand:
            if card.evaluate_card(card_open.color, card_open.value):
                self.hand_play.append(card)


    def draw_initial_luck(self, deck, card_open):
        i = -1
        action = deck.cards[i]
        while (deck.cards[i].value not in ["PL2", "PL4", "REV", "SKI", "COL"]):
            i -= 1
            action = deck.cards[i]
        self.hand.append(action)
        self.evaluate_hand(card_open)
        print(f'{self.name} draws {action.print_card()}')
        
            

    def draw_initial(self, deck, card_open):
        """
        Initial draws (no "lucky draw")
        """

        card = deck.draw_from_deck()
        self.hand.append(card)
        self.evaluate_hand(card_open)
        print(f'{self.name} draws {card.print_card()}')

    def draw(self, deck, card_open):
        """
        Adds a card to players' hand and evaluates the hand
        Required parameters:
            - deck as deck
            - card_open as card
        """

        # Checks for: if there is lucky_draw on, if it is player 2,
        # and then occurs at a chance given by the value in config
        if draw_state and self.name == player_name_2 and random.random() <= draw_luck:
            self.draw_with_luck(deck, card_open)
            return
        card = deck.draw_from_deck()
        self.hand.append(card)
        self.evaluate_hand(card_open)
        print(f'{self.name} draws {card.print_card()}')


    def draw_with_luck(self, deck, card_open):
        if len(deck.cards) == 0:
            deck.draw_from_deck()
        i = -1
        playable = deck.cards[i]
        while (not playable.evaluate_card(card_open.color, card_open.value)) and len(deck.cards) > abs(i):
            i -= 1
            playable = deck.cards[i]
        if not playable.evaluate_card(card_open.color, card_open.value):
            self.draw_initial(deck, card_open)
        else:
            self.hand.append(playable)
            self.evaluate_hand(card_open)
            print(f'{self.name} draws {playable.print_card()}')


    def skip_chain(self, deck, card_open):
        if card_open.value in ["REV", "SKI"]:
            for card in self.hand_play:
                if card.value in ["REV", "SKI"]:
                    self.card_play = card
                    self.hand.remove(card)
                    self.hand_play.remove(card)
                    deck.discard(card)
                    print(f'\n{self.name} plays {card.print_card()}')
                    return True

    def unfavor_wild(self):
        if len(self.hand_play) >= 2:
            for value in self.hand_play:
                if value.value in ["COL", "PL4"]:
                    self.hand_play.remove(value)
                    return value

    def play_highest(self, deck):
        points = {i: i for i in range(0, 10)}
        points.update({"REV": 20, "SKI": 20, "PL2": 20, "COL": 50, "PL4": 50})

        value = max(points[card.value] for card in self.hand_play)
        index = list(points[card.value] for card in self.hand_play).index(value)

        self.card_play = self.hand_play[index]
        self.hand.remove(self.card_play)
        self.hand_play.remove(self.card_play)
        deck.discard(self.card_play)
        print(f'\n{self.name} plays {self.card_play.print_card()}')

        self.wild_choice()


    def wild_choice(self):
        if color:
            if self.name == player_name_1:
                if self.card_play.value in ["PL4", "COL"]:
                    self.card_play.color = self.choose_color()
            else:
                if self.card_play.value in ["PL4", "COL"]:
                    self.card_play.color = random.choice(["RED", "GRE", "BLU", "YEL"])
        else:
            if self.card_play.value in ["PL4", "COL"]:
                self.card_play.color = random.choice(["RED", "GRE", "BLU", "YEL"])
    
    
    def plus_uno(self, deck, opponent):
        if len(opponent) <= 3:
            for card in self.hand_play:
                if card.value in ["PL4", "PL2"]:
                    self.card_play = card
                    self.hand.remove(card)
                    self.hand_play.remove(card)
                    deck.discard(card)
                    print(f'\n{self.name} plays {card.print_card()}')
                    return True


    def play_rand(self, deck, card_open, opponent):

        """
        Reflecting a players' random move, that consists of:
            - Shuffling players' hand cards
            - Lopping through hand cards and choosing the first available hand card to be played
            - Remove card from hand & replace card_open with it
        
        Required parameters: deck as deck
        """
        if plus and self.name == player_name_1:
            if self.plus_uno(deck, opponent):
                return
        
        if unfavor and self.name == player_name_1:
            self.unfavor_wild()

        if skip and self.name == player_name_1:
            if self.skip_chain(deck, card_open):
                return
            

        if highest and self.name == player_name_1:
            self.play_highest(deck)
            return

        random.shuffle(self.hand_play)
        for card in self.hand:
            if card == self.hand_play[-1]:
                self.card_play = card
                self.hand.remove(card)
                self.hand_play.pop()
                deck.discard(card)
                print(f'\n{self.name} plays {card.print_card()}')
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
                print(f'{self.name} counters with {card.print_card()}')
                break

    def choose_color(self):
        """
        Chooses a card color when a player plays PL4 or WILD COL.
        Color is determined by the majority color in the active players' hand.
        """

        colors = [card.color for card in self.hand if card.color in ["RED", "GRE", "BLU", "YEL"]]
        if len(colors) > 0:
            max_color = max(colors, key=colors.count)
        else:
            max_color = random.choice(["RED", "GRE", "BLU", "YEL"])

        print(f'{self.name} chooses {max_color}')
        return max_color

    def show_hand(self):
        underline(f'\n{self.name}s hand:')
        for card in self.hand:
            card.show_card()

    def show_hand_play(self, card_open):
        underline(f'\n{self.name}s playable hand:')
        self.evaluate_hand(card_open)
        for card in self.hand_play:
            card.show_card()
