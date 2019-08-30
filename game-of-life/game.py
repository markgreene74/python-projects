import datetime as dt
import random as rn

min_range = 1_000
max_range = 1_000_000

def when_is_now():
    return dt.datetime.now()

def run(BOARD_SIZE, CYCLES, DRYRUN):
    ''' docstring goes here'''
    print(f'This is the board size: {BOARD_SIZE}')
    if not CYCLES:
        CYCLES = rn.randrange(min_range, max_range)
    print(f'This is the number of cycles: {CYCLES}')
    print(f'This is the value of DRYRUN: {DRYRUN}')
