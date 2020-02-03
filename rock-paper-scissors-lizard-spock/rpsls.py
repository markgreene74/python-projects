#!/bin/env python3

import os

ROUNDS = int(os.environ.get("RPSLS_ROUNDS", 10))
plays_list = ["rock", "paper", "scissors", "lizard", "spock"]
wins_list = ["scissors,lizard","rock,spock","paper,lizard","spock,paper","scissors,rock"]
all_plays = dict(zip(plays_list, wins_list))


def play(aplay=None):
    if not aplay:
        return all_plays
    else:
        return {aplay: all_plays.get(aplay)}


def main():
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")


if __name__ == "__main__":
    main()
