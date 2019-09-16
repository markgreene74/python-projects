#!/bin/env python3

import os

ROUNDS = int(os.environ.get("RPSLS_ROUNDS", 10))


def main():
    print("Rock, paper, scissors, lizard, Spock")
    print(f"Will play {ROUNDS} rounds")


if __name__ == "__main__":
    main()
