#!/bin/env python3

import os
from random import choice

ROUNDS = int(os.environ.get("RPSLS_ROUNDS", 10))
plays_list = ["rock", "paper", "scissors", "lizard", "spock"]
wins_list = [
    "scissors,lizard",
    "rock,spock",
    "paper,lizard",
    "spock,paper",
    "scissors,rock",
]
all_plays = dict(zip(plays_list, wins_list))


def play(aplay=None):
    if not aplay:
        return all_plays
    else:
        return sorted(all_plays.get(aplay).split(","))


def match(one="", two=""):
    # pick a random player if needed
    if one not in plays_list:
        one = choice(plays_list)
    if two not in plays_list:
        two = choice(plays_list)
    # return a tie or the winner
    if one == two:
        return "tie"
    if two in all_plays.get(one):
        # one wins
        return one
    else:
        # two wins
        return two


def main():
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")


if __name__ == "__main__":
    main()
