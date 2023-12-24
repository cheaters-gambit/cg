class Card:
    suits = ["spades",
             "hearts",
             "diamonds",
             "clubs"]

    values = [None, None, "2", "3",
              "4", "5", "6", "7",
              "8", "9", "10",
              "Jack", "Queen",
              "King", "Ace"]

    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __repr__(self):
        """
        Return the string representation of the Card
        """
        v = self.values[self.value] + \
            " of " + \
            self.suits[self.suit]
        return v
