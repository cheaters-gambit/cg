from typing import List
from data_collection import sum_stacks, check_growth, display_stats, update_dataframe
import random
from deck import Deck
from player import Player

global stack_sizes

# Create a dictionary to calculate growth
growth = {}
# Set up an initial stack size
init_stacksize = 1000


def init_game():
    # Select the game mode (All civilian (1), All police (2) or one police per group (3))
    gamemodes = ["1", "2", "3"]
    while True:

        gamemode = input(f"Enter Game Mode. Available game modes are {gamemodes} : ")
        if gamemode in gamemodes:
            break
        else:
            print("Please select one of the available only")
            continue
    # Select number of players.
    """
    WARNING: The game is designed to be played by 6 players.
             Selecting any other number will lead to the automatic assigning of
             civilian role to all players and therefore prevent any policing behaviour
    """
    while True:
        number_of_players = input("Enter the number of players: ")
        try:
            number_of_players = int(number_of_players)
            break
        except ValueError:
            print("Number of players must be a valid integer.")
    # List to store player objects
    player_list = []
    # List to store player names
    name_list = []
    for i in range(number_of_players):
        # Select name of players, code ensures a unique name is given
        while True:
            name = input("Enter name of player: ")
            if not name:
                print("You have not entered a name")
            elif name in name_list:
                print("That name is taken, please use a different name")
            else:
                name_list.append(name)
                break
        # List of available strategies
        strategies_list = ["human", "greedy", "cheaters-gambit", "honest", "lowroll"]
        while True:
            # Select strategy of players
            strategy = input(f"Enter strategy. Available strategies = {strategies_list} : ").lower()
            if strategy in strategies_list:
                break
            else:
                print("Please select one of the available only")
                continue
        # Create player object
        player = Player(name=name, stack=init_stacksize, strategy=strategy)
        # Add player object to list
        player_list.append(player)
    # Initialise deck of cards
    deck = Deck()
    return gamemode, deck, player_list


def setup_gamemode(mode, player_list):
    # Here we split players into groups and civilian/police for game modes 2 and 3
    if mode == "1":
        # No grouping is needed for game mode 1, and we can assign all players as civilians
        for i in player_list:
            i.role = "civilian"
        return
    else:
        # Now we split players into 2 groups randomly for game modes 2 and 3
        # Note that this will only work if there are 6 players (which is how the game should be played)
        templist = player_list.copy()
        # Shuffle a copy of the player list to ensure random assignation
        random.shuffle(templist)
        if len(templist) == 6:
            group1_list = templist[0:3]
            group2_list = templist[3:6]
        else:
            print("Error: Cannot split into 2 groups of 3 due to number of players")
            for i in player_list:
                # Ensures no policing can be done if wrong number of players
                i.role = "civilian"
            return
        # Now we can assign players to their groups
        for i in group1_list:
            i.group = 1
        for j in group2_list:
            j.group = 2
    # Now we can assign players as police according to game mode structure
    if mode == "2":
        # In game mode 2, all players are police
        for i in player_list:
            i.role = "police"
    if mode == "3":
        # For this game mode we can use the already randomised group list to assign police and civilians
        group1_list[0].role = "police"
        group1_list[1].role = "civilian"
        group1_list[2].role = "civilian"
        # Now we can do the same for group 2
        group2_list[0].role = "police"
        group2_list[1].role = "civilian"
        group2_list[2].role = "civilian"
    # Now the player's roles are assigned, and we can return the group lists for later use
    # REMEMBER THE LISTS CONTAIN THE PLAYER OBJECTS AND NOT THEIR NAMES
    return group1_list, group2_list


def get_active_players(player_list):
    # Check for non-bankrupt players (players with a stacksize > 0)
    playing_players = []
    for i in player_list:
        if i.stacksize != 0:
            playing_players.append(i)
    return playing_players


def check_draws_between_card_values(card_values: List[int]):
    # Copy and sort cards played
    new_list = card_values.copy()
    new_list.sort(reverse=True)
    # Check for a draw between the highest cards and remove them from ordered_card_list
    draws = True
    # Keep checking for draws until no draws or no cards are left
    while draws and len(new_list) > 1:
        focal_var = new_list[0]
        if new_list[1] == focal_var:
            # Let's remove all instances from the list:
            new_list = remove_items(new_list, focal_var)
        # Check that the list isn't empty
        if len(new_list) > 1:
            # Check if there is another draw
            if new_list[0] == new_list[1]:
                continue
            else:
                # If there are no mo draws, we can break the loop and return the list
                draws = False
    return new_list


def sum_pot(playing_players):
    # Straightforward
    pot = 0
    for i in playing_players:
        pot += i.bid
    # Duplicate pot
    pot *= 2
    return pot


def settle_game(playing_players, pot, round_number_x, dataframe):
    # Get declared cards
    global rest_prize_portion
    # Get round number for data collection
    round_number = round_number_x
    # Get dataframe for data collection
    game_data = dataframe
    # Initialise a list to track cards played
    card_list = []
    # track winner's name
    winner_name = None
    for j in playing_players:
        card_list.append(j.card_declared_num)

    # Check for draws:
    no_draw_list = check_draws_between_card_values(card_list)
    # For debugging, check cards that haven't drawn by uncommenting line below
    # print(f"This is the no draw list: {no_draw_list}")

    # Now, Lets check whether everyone has drawn:
    if len(no_draw_list) == 0:
        print("Everyone drew, no one wins!")
        # Update data frame as game is already settled
        dataframe[f"Round {round_number}"] = update_dataframe(playing_players, winner_name, init_stacksize,
                                                              no_draw_list)
        return
    # declare winning value:
    winner = no_draw_list[0]
    print(f"The winning card number is: {winner}")

    # declare losing but still participating card values:
    participating_list = no_draw_list[1::]

    # define first prize:
    first_prize = float(pot) * 0.3
    print(f"Winner gets: {first_prize}")
    # define rest prize:
    rest_prize = float(pot) * 0.7
    """
    NOTE: THE BELOW CODE LEADS TO SITUATIONS WHERE WINNING PORTION < LOSING PORTION FIXED BY SETTING A FIXED PRIZE
    # each player gets a fraction of rest_prize determined by len(participating_list)
    if len(participating_list) > 0:
        rest_prize_portion = round(rest_prize / len(participating_list))
    else:
        rest_prize_portion = 0
    """
    # To solve this problem, each non-drawing losing player gets amount equivalent to round with no draws
    rest_prize_portion = rest_prize / 5
    # We can run the function that displays all round stats for debugging by uncommenting the line below
    # display_stats(playing_players, no_draw_list, pot, rest_prize_portion)
    # Give prizes:
    for i in playing_players:
        # Give winner first prize
        if i.card_declared_num == winner:
            i.stacksize += first_prize
            # Set winner var to winner's name
            winner_name = i.name
            # Announce winner (optional)
            print(f"The winner is: {i.name}")
            # for debugging, we can check a stack size has been properly updated by uncommenting line below
            # print(f"Winner's new stack size is: {i.stacksize}")
        # give the rest their part
        elif i.card_declared_num in participating_list:
            # For debugging, we can check correct addition of stacksize by uncommenting line below
            # print(f"{i.name}'s stack adding operation is: {i.stacksize} + {rest_prize_portion}")
            i.stacksize += rest_prize_portion
            # For debugging, we can check losing players and correct update of stacksize by uncommenting line below
            # print(f"Loser {i.name}'s new stack size is: {i.stacksize}")
        elif i.card_declared_num != winner:
            # Print out players that lost
            print(f"{i.name} Drew the round and got disqualified")
        # Obtain growth so far
        growth[i.name] = check_growth(i, init_stacksize)
    # Now we can update the dataframe with the data from the round
    dataframe[f"Round {round_number}"] = update_dataframe(playing_players, winner_name, init_stacksize, no_draw_list)
    # For debugging, we can print player's growths to ensure everything is working by uncommenting line below
    # print(f"Here is each player's total growth: {growth}")
    # For debugging, we can test data collection by uncommenting lines below
    # print(dataframe[f"Round {round_number}"])
    # print(dataframe)


def remove_items(list_of_players, item):
    # Here we return a list without any instances of what we're removing
    res = [i for i in list_of_players if i != item]

    return res
