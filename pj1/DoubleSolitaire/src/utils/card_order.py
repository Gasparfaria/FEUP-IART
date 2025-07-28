"""
Helper for card operations
"""

SUITS = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
RANKS = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
REDS = {"Hearts", "Diamonds"}
BLACKS = {"Spades", "Clubs"}

RANK_VALUE = {rank: index for index, rank in enumerate(RANKS)} # Ace = 0, ..., King = 12

SUIT_VALUE = {suit: index for index, suit in enumerate(SUITS)} # Hearts = 0, ..., Clubs = 3

def rank_index(rank):
    if None:
        return -1
    return RANK_VALUE.get(rank, -1)

def suit_index(suit):
    if None:
        return -1
    return SUIT_VALUE.get(suit, -1)


def compare_ranks(rank1, rank2):
    """ Returns:
        -1 if rank1 < rank2,
         0 if equal,
         1 if rank1 > rank2
    """
    return (rank_index(rank1) > rank_index(rank2)) - (rank_index(rank1) < rank_index(rank2))

def is_next_rank(current_rank, next_rank):
    """ Check if `next_rank` is exactly one rank above `current_rank` """
    return rank_index(next_rank) == rank_index(current_rank) + 1

def is_prev_rank(current_rank, prev_rank):
    """ Check if `prev_rank` is exactly one rank below `current_rank` """
    return rank_index(prev_rank) == rank_index(current_rank) - 1

def is_prev_dif_colour(current_suit, previous_suit):
    if (current_suit in REDS and previous_suit in BLACKS) or (current_suit in BLACKS and previous_suit in REDS):
        return True
    return False

def next_rank(rank):
    if (rank_index(rank) +1) < 0:
        return None
    return RANKS[rank_index(rank) + 1]

def prev_rank(rank):
    return RANKS[rank_index(rank) - 1]

def max_rank(current_rank, next_rank):
    """ Returns the maximum rank above `next_rank` """
    maxi = max(rank_index(next_rank), rank_index(current_rank))
    return RANKS[maxi]

def min_rank(current_rank, prev_rank):
    """ Returns the minimum rank below `prev_rank` """
    if current_rank is None:
        return prev_rank
    elif prev_rank is None:
        return current_rank
    mini = min(rank_index(prev_rank), rank_index(current_rank))
    return RANKS[mini]