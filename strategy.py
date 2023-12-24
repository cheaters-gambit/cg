import random

"""
Here you can modify the basic strategies by changing the range of "declaration = random.randint()"
"""
def greedy(card_drawn):
    declaration = 0
    if card_drawn <= 11:
        declaration = random.randint(11, 14)
    else:
        declaration = card_drawn
    return declaration


def cheaters_gambit(card_drawn):

    declaration = random.randint(10, 12)
    return declaration


def honest(card_drawn):
    declaration = card_drawn

    return declaration


def lowroll(card_drawn):
    declaration = 2
    return declaration
