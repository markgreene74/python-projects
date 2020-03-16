#!/bin/env python3

import os
from random import choice

ROUNDS: int = int(os.environ.get("RPSLS_ROUNDS", 10))
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
    if not a_player:
        return players_table
    else:
        return sorted(players_table.get(a_player).split(","))


def match(one: str = "", two: str = "") -> str:
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
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")
    counter = 0
    while counter < ROUNDS:
        winner = match()
        print(winner)
        counter += 1


if __name__ == "__main__":
    main()
