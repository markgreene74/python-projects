#!/bin/env python3

import os

from collections import namedtuple

ROUNDS = int(os.environ.get("RPSLS_ROUNDS", 10))
Play = namedtuple("Play", "name, winover")
plays_list = ["rock", "paper", "scissors", "lizard", "spock"]
wins_list = [[1, 2, 3] for i in range(5)]
all_plays = [Play(name=i, winover=j) for i, j in zip(plays_list, wins_list)]


def play(aplay=None):
    if not aplay:
        return all_plays


def main():
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")


if __name__ == "__main__":
    main()
