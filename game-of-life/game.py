import datetime as dt

def when_is_now():
    return dt.datetime.now()

def run(BOARD_SIZE, CYCLES, DRYRUN):
    ''' docstring goes here'''
    print(f'This is the board size: {BOARD_SIZE}')
    print(f'This is the number of cycles: {CYCLES}')
    print(f'This is the value of DRYRUN: {DRYRUN}')
