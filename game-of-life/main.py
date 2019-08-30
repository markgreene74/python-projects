#!/usr/bin/env python3

import os
import sys
import game

# read env variables
BOARD_SIZE = os.environ.get('BOARD_SIZE', '20x20')
CYCLES = os.environ.get('CYCLES')
DRYRUN = os.environ.get('DRYRUN', False)


if __name__ == "__main__":
    print("{}".format(game.when_is_now()))
    game.run(BOARD_SIZE, CYCLES, DRYRUN)
    print("hello world")
