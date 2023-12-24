from random import shuffle

from card import Card


class Deck:
    def __init__(self):
        # Grabs all possible combinations of card suit & value
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def get_card(self):
        # Shuffle deck and grab top card
        shuffle(self.cards)
        return self.cards[0]
