#!/bin/env python3

import os
from random import choice

ROUNDS: int = int(os.environ.get("RPSLS_ROUNDS", 10))
PLAYERS_FILE: str = "rpsls.txt"
players_list: list = ["rock", "paper", "scissors", "lizard", "spock"]
wins_list: list = [
    "scissors,lizard",
    "rock,spock",
    "paper,lizard",
    "spock,paper",
    "scissors,rock",
]
players_table: dict = dict(zip(players_list, wins_list))


def player(a_player: str = None) -> list:
    """ Given a player return the list of players that
        win in a match against it
    """
    if not a_player:
        return players_table
    else:
        return sorted(players_table.get(a_player).split(","))


def load_players_file() -> list:
    """ If exists load the file containing a list of players
        and create a match list. Also perform a sanity check
        on the list.
        If the number of players is less than the number of
        rounds then cycle through the list
    """
    # if the file doesn't exist return a list
    # of empty players
    if not os.path.isfile(PLAYERS_FILE):
        return [("", "")] * ROUNDS
    # read the file, parse it and perform sanity check
    with open(PLAYERS_FILE) as f:
        data = f.readlines()
    return data


def match(one: str = "", two: str = "") -> str:
    """ Given player one and player two return the result
        of the match (either a tie or one of the two players)
    """
    # pick a random player if needed
    if one not in players_list:
        one = choice(players_list)
    if two not in players_list:
        two = choice(players_list)
    # return a tie or the winner
    if one == two:
        return "tie"
    if two in players_table.get(one):
        # one wins
        return one
    else:
        # two wins
        return two


def main() -> None:
    # print some useful information
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")
    # load the players file if it exists
    # otherwise get a list of empty player
    # which will trigger the random player selection
    match_list = load_players_file()
    # start the game
    for i in match_list:
        winner = match(i[0], i[1])
        print(winner)


if __name__ == "__main__":
    main()
