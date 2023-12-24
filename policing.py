def reset_policed_attributes(player_list):
    """
    Reset the .checked and .busted attributes for all players in the player_list.
    """
    for player in player_list:
        player.checked = False
        player.busted = False


def run_round_of_policing(player_list):
    """
    Run a round of policing for each player in player_list.
    """
    for player in player_list:
        if player.strategy == "human":
            policeman(player, player_list)
        else:
            policeman_auto(player, player_list)


def police(player):
    # If player did not cheat -> nothing happens
    if player.card_declared_num == player.card_drawn.value:
        print("Player did not cheat")
    # If player did cheat, they are busted and have to play the card they drew
    else:
        player.busted = True
        print("Cheater caught")
        player.card_declared_num = player.card_drawn.value
    # Mark player as checked so other police don't check him
    player.checked = True


def get_unpoliced_in_group(player, playerlist):
    group_num = player.group
    # Players can be policed if they are in the same group, and haven't already been checked
    # Players cannot police themselves
    objects_list = [i for i in playerlist if i != player and i.group == group_num and not i.checked]
    if objects_list:
        # If there is at least 1 option, return a list with the player
        # Also return a list with the player names
        names_list = [j.name for j in objects_list]
        return objects_list, names_list
    else:
        # If there are no options, return two empty lists
        return [], []


def policeman_auto(focal_player, playerlist):
    # Performs the same actions as policeman() but assuming yes is inputted at all times
    if focal_player.role != "police":
        print(f"{focal_player.name} is not a police officer.")
        return
    while True:
        police_choices, police_choices_names = get_unpoliced_in_group(focal_player, playerlist)
        if not police_choices:
            print(f"There are no more choices available for {focal_player.name}.")
            break
        else:
            # debugging
            # print("These are the players you can police:")
            for i in police_choices:
                # Police the chosen player
                police(i)
                # debugging
                # print(f"{focal_player.name}, you have policed {i.name}.")


def policeman(focal_player, playerlist):
    # Only allow policing by police
    if focal_player.role != "police":
        print(f"{focal_player.name} is not a police officer.")
        return
    while True:
        # .lower allows user to input caps in yes/no
        yesno = input(f"{focal_player.name}, would you like to police? ").lower()
        if yesno in ["yes", "no"]:
            break
        else:
            print("Please select Yes or No")
    if yesno == "no":
        print("You have chosen not to Police")
        return
    elif yesno == "yes":
        while True:
            # Grab available policing choices
            police_choices, police_choices_names = get_unpoliced_in_group(focal_player, playerlist)
            if not police_choices:
                print(f"There are no more choices available for {focal_player.name}.")
                break
            else:
                print("These are the players you can police:")
                for i in police_choices:
                    print(f"- {i.name}")
                    # Allow player to select an available target
                choice = input(f"{focal_player.name}, who would you like to check? ")
                if choice in police_choices_names:
                    # Grab a player objects position in a list from the position of its name in another list
                    index = police_choices_names.index(choice)
                    # Police the chosen player
                    police(police_choices[index])
                    print(f"{focal_player.name}, you have policed {choice}.")
                    while True:
                        # .lower allows user to input caps in yes/no
                        keep_policing = input("Would you like to keep policing? ").lower()
                        if keep_policing in ["yes", "no"]:
                            break
                        else:
                            print("Please select Yes or No")
                    if keep_policing == "yes":
                        pass
                    else:
                        print("You have chosen to finish policing.")
                        break
                else:
                    print("Please choose from available choices.")
                    pass
