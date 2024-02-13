from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf

class Game(object):
    """
    A game reflects an iteration of turns, until one player fulfills the winning condition of 0 hand cards.
    It initialized with two players and a turn object.
    """

    def __init__(self, player_1_name, player_2_name, starting_name, comment):

        if comment == False: block_print()

        self.player_1 = Player(player_1_name)
        self.player_2 = Player(player_2_name)
        self.turn = Turn(
            deck=Deck(
                player_1=self.player_1,
                player_2=self.player_2
            ),
            player_1=self.player_1,
            player_2=self.player_2,
        )
        self.turn_no = 0
        self.winner = 0
        self.points = 0

        # With each new game the starting player is switched, in order to make it fair
        while self.winner == 0:
            self.turn_no += 1
            card_open = self.turn.card_open
            bold(f'\n---------- TURN {self.turn_no} ----------')
            print(f'\nCurrent open card: {self.turn.card_open.print_card()}')

            if starting_name == self.player_1.name:
                if self.turn_no % 2 == 1:
                    player_act, player_pas = self.player_1, self.player_2
                else:
                    player_act, player_pas = self.player_2, self.player_1
            else:
                if self.turn_no % 2 == 0:
                    player_act, player_pas = self.player_1, self.player_2
                else:
                    player_act, player_pas = self.player_2, self.player_1

            player_act.show_hand()
            player_act.show_hand_play(card_open)
            self.turn.action(
                player=player_act,
                opponent=player_pas,
            )

            if check_win(player_act):
                self.winner = player_act.name
                print(f'{player_act.name} has won!')
                for card in player_pas.hand:
                    if card.value in range(0, 10):
                        self.points += card.value
                    elif card.value in ["PL2", "SKI", "REV"]:
                        self.points += 20
                    else:
                        self.points += 50
                break

            if check_win(player_pas):
                self.winner = player_pas.name
                print(f'{player_pas.name} has won!')
                for card in player_act.hand:
                    if card.value in range(0, 10):
                        self.points += card.value
                    elif card.value in ["PL2", "SKI", "REV"]:
                        self.points += 20
                    else:
                        self.points += 50
                break

            if player_act.card_play.value in ["REV", "SKIP"]:
                print(f'{player_act.name} has another turn')
                self.turn_no = self.turn_no - 1

            if (self.turn.count > 0) and (self.turn.count % 2 == 0):
                print(f'Again it is {player_act.name}s turn')
                self.turn_no = self.turn_no - 1

        if not comment: enable_print()


def tournament(tournament_iterations, comment):
    """
    A function that iterates various Games and outputs summary statistics over all executed simulations.
    """

    winner, points = "", 0

    if conf.luck["always_first"]:
        game = Game(
            player_1_name=conf.player_name_1,
            player_2_name=conf.player_name_2,
            starting_name=conf.player_name_2,
            comment=comment
        )
    else:
        if tournament_iterations % 2 == 1:
            game = Game(
                player_1_name=conf.player_name_1,
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_2,
                comment=comment
            )
        else:
            game = Game(
                player_1_name=conf.player_name_1,
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_1,
                comment=comment
            )

    return game.winner, game.points


def real(iterations, comment):
    n = 0
    winner, games = "", 0
    for i in range(iterations):
        points1 = 0
        points2 = 0
        gameCount = 0
        while points1 < 500 and points2 < 500:
            n += 1
            gameCount += 1
            points = tournament(n, comment)
            if points[0] == conf.player_name_1:
                points1 += points[1]
            else:
                points2 += points[1]
        points_difference = points1 - points2
        if points1 >= 500:
            winner = conf.player_name_1
            if not comment:
                block_print()
            print(bold(
                f"\n{conf.player_name_1} has won in {gameCount} games, winning the opponent by {abs(points_difference)} points!"))
            enable_print()
        else:
            winner = conf.player_name_2
            if not comment:
                block_print()
            print(bold(
                f"\n{conf.player_name_2} has won in {gameCount} games, winning the opponent by {abs(points_difference)} points!"))
            enable_print()
        games = gameCount

    return winner, games, points_difference, n
