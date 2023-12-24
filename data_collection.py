"""
File containing functions for V1.0 of data collection
"""
import pandas as pd
import csv
import os

# Use dictionary to obtain numeric value of a card in string format
card_dict = {"Jack": 11, "Queen": 12, "King": 13, "Ace": 14}


def init_player_dataframe(rounds):
    # Create a dictionary containing a separate dictionary for each round
    game_data = {}

    for i in range(1, rounds + 1):
        game_data[f"Round {i}"] = {}
    return game_data


def sum_stacks(list1):
    # Sums up the stack sizes
    count = 0
    for i in list1:
        count += i


def update_dataframe(player_list, winning_player, stacks, no_draw_list):
    # create a dataframe of the data for one round for each player
    # returns a dictionary containing all the data for a round
    round_dict = {}
    nodraws = no_draw_list
    # First we need to reset all variables to avoid repetition of entries
    for i in player_list:
        data = {
            "name": [],
            "stacksize": 0,
            "card drawn": 0,
            "card declared": 0,
            "has cheated": 0,
            "total_growth": 0,
            "has drawn": 0,
            "won": 0,
            "strategy": None,
            "role": None,
            "busted": False

        }

        # Now we can assign variables from player attributes
        name = i.name
        data["name"] = i.name
        stacksize = i.stacksize
        data["stacksize"] = i.stacksize
        drawn = i.card_drawn.value
        data["card drawn"] = i.card_drawn
        declared = i.card_declared_num
        data["card declared"] = i.card_declared_num
        data["strategy"] = i.strategy
        data["role"] = i.role
        data["busted"] = i.busted
        # Next we grab data not found in player attributes
        # Check for cheating (check card played is card drawn)
        # if statements used because string values in card drawn (Jack, Queen, King and Ace).
        if drawn in card_dict.keys():
            # Checks for cheating when card is string format
            if card_dict[drawn] != data["card declared"]:
                data["has cheated"] = 1
            else:
                data["has cheated"] = 0
        # If card is in number format, we can check cheating easily
        elif int(drawn) != declared:
            data["has cheated"] = 1
        else:
            data["has cheated"] = 0

        # check if player has won
        if i.name == winning_player:
            data["won"] = 1
        else:
            data["won"] = 0

        # check if player has drawn
        if i.card_declared_num in nodraws:
            data["has drawn"] = 0

        else:
            data["has drawn"] = 1

        # get player's growth
        data["total_growth"] = check_growth(i, stacks)
        # update the dataframe with a player's data
        round_dict[f"{i.name}"] = data

    return round_dict


def check_growth(player, initial_stacks):
    # Calculate how much money a player has made
    final_stack = player.stacksize
    growth = final_stack - initial_stacks
    return growth


def export_data(data, csv_filename):
    # Extract the header fields (column names) from the first round's data
    first_round_data = next(iter(data.values()))
    header_fields = list(first_round_data[next(iter(first_round_data))].keys())

    # Create the "output" folder if it doesn't exist within working directory
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    csv_filepath = os.path.join(output_folder, csv_filename)
    # Write into a csv file with a given name
    with open(csv_filepath, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Round"] + header_fields)
        writer.writeheader()
        # Write a player's round data as a row
        for round_name, round_data in data.items():
            for player_name, player_data in round_data.items():
                row = {"Round": round_name, **player_data}
                writer.writerow(row)


"""
Debugging function that can help track what is going on in the game
"""


def display_stats(players, nodraws, pot,
                  restprize):  #
    """
    Function to help keep track of what happened during the round
    players consists of a list of player objects while nodraws consists of a list of values.
    NOTE: This function prints out a lot of text.
    """
    # Create a list to store tuples consisting of name and card played
    draws = []
    first_prize = float(pot) * 0.3
    rest_prize_total = float(pot) * 0.7

    print("Here are the statistics for the round")
    print(f"Total pot size is {pot}")
    print(f"The first prize is: {first_prize}")
    print(f"Total rest prize is: {rest_prize_total}")
    print(f"Each loser gets: {restprize}")
    for i in players:
        print(f"Player: {i.name}")
        print("bid_size: ", i.bid)
        print("card drawn: ", i.card_drawn)
        print("card declared: ", i.card_declared_num)
    # Obtain drawing players and their cards
    for j in players:
        if j.card_declared_num in nodraws:
            continue
        else:
            temp_tuple = (j.name, j.card_declared_num)
            draws.append(temp_tuple)
    print("Here are the draws")
    # Loop through the list and print each tuple
    if len(draws) > 0:
        for pair in draws:
            print(f"Name: {pair[0]}, card played: {pair[1]}")
    else:
        print("No one drew this round!")
