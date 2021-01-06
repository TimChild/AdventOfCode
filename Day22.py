import numpy as np
import copy
from typing import List, Tuple
import pandas as pd


class Player:
    def __init__(self, starting_cards):
        self.hand = starting_cards


def get_hands(fp):
    with open(fp) as f:
        raw = f.readlines()

    h1start = 1
    h1end = np.where(np.array(raw) == '\n')[0][0]

    hand1 = [l.strip() for l in raw[h1start:h1end]]

    h2start = h1end+2
    h2end = None

    hand2 = [l.strip() for l in raw[h2start:h2end]]

    hand1, hand2 = [[int(x) for x in hand] for hand in [hand1, hand2]]
    return hand1, hand2


def take_turn(p1hand: List[int], p2hand: List[int]):
    """Modifies hands (lists) in place"""
    hands = p1hand, p2hand
    p1card, p2card = [hand.pop(0) for hand in hands]

    if p1card > p2card:
        p1hand.extend([p1card, p2card])
    elif p2card > p1card:
        p2hand.extend([p2card, p1card])
    else:
        raise RuntimeError(f'ERROR: p1, p2: {p1card, p2card}')


def play_game1(player1: Player, player2: Player) -> Tuple[int, List[int]]:
    p1, p2 = player1, player2
    while p1.hand and p2.hand:
        take_turn(p1.hand, p2.hand)
    if p1.hand and not p2.hand:
        winner, win_hand = 1, p1.hand
    elif p2.hand and not p1.hand:
        winner, win_hand = 2, p2.hand
    else:
        raise RuntimeError(f'ERROR: p1, p2: {p1.hand, p2.hand}')
    print(f'Player {winner} wins with hand: {win_hand}')
    return winner, win_hand


class RecursiveGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.previous_hands: List[Tuple[List[int]]] = []
        self.winnings = []

    def play_game(self, p1hand: List[int], p2hand: List[int]):
        hands = (p1hand, p2hand)
        if tuple(hands) in self.previous_hands:
            rule = 'Infinite Recursion Rule'
            game_winner = 1
        elif any([len(hand) == 0 for hand in hands]):
            rule = 'No cards left rule'
            if len(p1hand) == 0 and len(p2hand) != 0:
                game_winner = 2
            elif len(p2hand) == 0 and len(p1hand) != 0:
                game_winner = 1
            else:
                raise RuntimeError(f'ERROR: {p1hand, p2hand}')
            print(
                f'{"   " * (self.game_id - 1)}Game {self.game_id} Winner: Player1 Wins through {rule}: {p1hand, p2hand}')
        else:
            round_winner = self.play_round(*hands)

            self.previous_hands = []

            game_winner, rule = self.play_game(*hands)
        return game_winner, rule

    def play_round(self, p1hand: List[int], p2hand: List[int]):
        hands = (p1hand, p2hand)
        self.previous_hands.append(tuple(hands))
        cards = [hand.pop(0) for hand in hands]
        if all([len(h) >= c for c, h in zip(cards, hands)]):
            new_game = RecursiveGame(self.game_id+1)
            new_hands = [hand[:c] for hand, c in zip(hands, cards)]
            print(f'!!! Playing sub game {self.game_id+1} to determine round. p1, p2, c1, c2 = {p1hand, p2hand, *cards}\n'
                  f'New Hands: {new_hands}')
            round_winner, rule = new_game.play_game(*new_hands)
            print(f'==== Ended sub game {self.game_id+1} with round_winner, rule: {round_winner, rule}')
        else:
            if cards[0] > cards[1]:
                round_winner, card_val = 1, cards[0]
            elif cards[1] > cards[0]:
                round_winner, card_val = 2, cards[1]
            else:
                raise RuntimeError(f'ERROR1: p1, p2, cards = {p1hand, p2hand, cards}')
            print(f'{"   "*(self.game_id-1)}Game {self.game_id} Round Winner : Not Enough Cards Winner is Player {round_winner} with card_val {card_val}')
        if round_winner == 1:
            hands[0].extend(cards)
        elif round_winner == 2:
            hands[1].extend(reversed(cards))
        else:
            raise RuntimeError(f'ERROR2: p1, p2, cards, round_winner = {p1hand, p2hand, cards, round_winner}')
        return round_winner

    # def play_full_game(self, player1: Player, player2: Player, show_progress=True):
    #     p1, p2 = player1, player2
    #     if show_progress:
    #         print(p1.hand, '\n', p2.hand)
    #     while
    #         self.play_round(p1.hand, p2.hand)
    #         self.previous_hands = []
    #         if show_progress:
    #             print(p1.hand, '\n', p2.hand)


def play_game2(player1: Player, player2: Player, show_progress=True) -> Tuple[int, List[int]]:
    p1, p2 = player1, player2
    p2game = RecursiveGame(1)
    if show_progress:
        print(p1.hand, '\n', p2.hand)
    while p1.hand and p2.hand:
        p2game.play_round(p1.hand, p2.hand)
        # p2game.previous_hands = []
        if show_progress:
            print(p1.hand, '\n', p2.hand)

    if p1.hand and not p2.hand:
        winner, win_hand = 1, p1.hand
    elif p2.hand and not p1.hand:
        winner, win_hand = 2, p2.hand
    else:
        raise RuntimeError(f'ERROR: p1, p2: {p1.hand, p2.hand}')
    print(f'Player {winner} wins with hand: {win_hand}')
    return winner, win_hand


def get_score(winning_hand):
    score = np.sum([(i+1)*x for i, x in enumerate(reversed(winning_hand))])
    return score


if __name__ == '__main__':
    fp = 'Day22_Input_test.txt'
    # fp = 'Day22_Input.txt'

    h1, h2 = get_hands(fp)
    p1 = Player(h1)
    p2 = Player(h2)

    # print(p1.hand, p2.hand)
    # take_turn(p1.hand, p2.hand)
    # print(p1.hand, '\n', p2.hand)
    # take_turn(p1.hand, p2.hand)
    # print(p1.hand, '\n', p2.hand)
    # take_turn(p1.hand, p2.hand)
    # print(p1.hand, '\n', p2.hand)
    # take_turn(p1.hand, p2.hand)
    # print(p1.hand, '\n', p2.hand)

    winner, win_hand = play_game1(p1, p2)
    print(f'\n\nPart 1:\nWinning score: {get_score(win_hand)}\n\n')

    h1, h2 = get_hands(fp)
    p1, p2 = [Player(h) for h in (h1, h2)]
    p2game = RecursiveGame(1)

    # p2game.play_game(p1.hand, p2.hand)

    print(p1.hand, '\n', p2.hand)
    for i in range(79):
        p2game.play_round(p1.hand, p2.hand)
        p2game.previous_hands = []
        print(p1.hand, '\n', p2.hand)
    # winner, win_hand = play_game2(p1, p2, show_progress=True)
    # print(f'\n\nPart 2:\nWinning score: {get_score(win_hand)}\n\n')






