import strategy
from card import Card
from strategy import greedy, cheaters_gambit, honest, lowroll

# Dictionary used to convert from string to numbers
card_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12,
             "King": 13, "Ace": 14}


class Player:
    strategies_list = ["human", "greedy", "cheaters-gambit", "honest", "lowroll"]

    # Initialise a player's attributes
    def __init__(self, name, stack, strategy):
        self.name = name
        self.card_drawn = 0
        self.card_declared_num = None
        self.stacksize = stack
        self.bid = 0
        self.strategy = strategy
        self.checked = False
        self.role = None
        self.group = None
        self.busted = False

    def draw_card(self, card):
        # Self-explanatory
        self.card_drawn = card

    def make_bid(self):
        # Bids are automatically set to 100 for non-human strategies
        if self.strategy != "human":
            if self.stacksize >= 100:
                self.bid = 100
            else:
                self.bid = self.stacksize
            self.stacksize -= self.bid
            return
        # Show a human player their stacksize
        print(f"{self.name}, your stack size is: {self.stacksize}")
        while True:
            bid = input("Enter your bid: ")
            # Ensure a player has at least the bidsize inputted
            try:
                bid = int(bid)
                if bid < self.stacksize:
                    self.bid = bid
                    self.stacksize -= bid
                    break
                else:
                    print("Bid must be less than stack size.")
            except ValueError:
                print("Bid must be a valid integer.")

    def declare_card(self):
        # Set declarations for different non-human strategies
        var = self.card_drawn.value
        if self.strategy == "greedy":
            self.card_declared_num = strategy.greedy(var)
            return
        elif self.strategy == "cheaters-gambit":
            self.card_declared_num = strategy.cheaters_gambit(var)
            return
        elif self.strategy == "honest":
            self.card_declared_num = strategy.honest(var)
            return
        elif self.strategy == "lowroll":
            self.card_declared_num = strategy.lowroll(var)
            return
        # Show humans the card they drew
        print(f"{self.name}, you have drawn the card: {self.card_drawn}")
        while True:
            # Ensure a player declares a valid card
            card_declared = int(input("Please declare your card between 2 and 14 : "))
            try:
                if 2 <= card_declared <= 14:
                    self.card_declared_num = card_declared
                    break
            except ValueError:
                print("Card value must be an integer between 2 to 14")
