import numpy as np


SUITS = ['Spade', 'Club', 'Diamond', 'Heart']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
POSSIBLE_CARDS = [f'{suit} {rank}' for suit in SUITS for rank in RANKS]
STARTING_DECK = list(POSSIBLE_CARDS)
CARDS_VALUE = {f'{suit} {rank}': int(rank) if rank.isdigit() else 10 if rank in ['J', 'Q', 'K'] else 11 for suit in SUITS for rank in RANKS}


# DEFINING THE BASIC STRATEGY DEVIATIONS
# Defining the players engine as a numpy array
# The columns represent dealer's up card: 2, 3, 4, 5, 6, 7, 8, 9, 10, A
# H = Hit, S = Stand, D = Double, 
# for splits Y = Yes, N = No

# all arrays are 3 dimensional, with exactly 3 layers
    # main layer (0) defines the true count value to enable an exception
    # layer (1) defines the standard play
    # layer (2) is for the exceptions, where the player should play differently based on the true count


HARD_TOTALS = np.array([
    # 8 or less
    [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [5, 'H', 'D'], [3, 'H', 'D'], [1, 'H', 'D'], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan],[np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 9
    [[1, 'H', 'D'], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [3, 'H', 'D'], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 10
    [[np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 11
    [[np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan]],
    # 12
    [[3, 'H', 'S'], [2, 'H', 'S'], [0, 'H', 'S'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 13
    [[-1, 'H', 'S'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 14
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # 15
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [4, 'H', 'S']],
    # 16
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [4, 'H', 'S'], [0, 'H', 'S'], [np.nan,'H',np.nan]],
    # 17+
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]]
], dtype=object)

SOFT_TOTALS = np.array([
    # A9
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]], 
    # A8
    [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [3, 'S', 'D'], [1, 'S', 'D'], [1, 'S', 'D'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]], 
    # A7
    [[0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # A6
    [[1, 'H', 'D'], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # A5
    [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # A4
    [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # A3
    [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
    # A2
    [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]]
], dtype=object)


PAIR_SPLITTING = np.array([
    # AA
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan]],
    # TT
    [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [6, 'N', 'Y'], [5, 'N', 'Y'], [4, 'N', 'Y'], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 99
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]], 
    # 88
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan]],
    # 77
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 66
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 55
    [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 44
    [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 33
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
    # 22
    [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]]
], dtype=object)
