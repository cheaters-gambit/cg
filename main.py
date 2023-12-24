from game import init_game, get_active_players, sum_pot, settle_game, setup_gamemode
from data_collection import init_player_dataframe, export_data
from policing import police, policeman, get_unpoliced_in_group, policeman_auto, reset_policed_attributes, \
    run_round_of_policing
import csv


def main():
    print("Welcome to The Cheater's Gambit")
    """ INITIAL SETUP """
    # Obtain gamemode, decks and set up players
    gamemode, deck, player_list = init_game()
    # Start at round 1
    current_round = 1
    # Define number of rounds to be played
    max_rounds = 10
    # Initialise game data dictionary
    game_data = init_player_dataframe(max_rounds)
    # Set up groups (for gamemode 2 and 3) and player roles
    setup_gamemode(gamemode, player_list)
    """ ROUNDS """
    # Play for an assigned number of rounds
    while True and current_round <= max_rounds:

        print("Round: ", str(current_round))

        # Check active (non-bankrupt) players
        playing_players = get_active_players(player_list)
        # If only one player remains, end game
        if len(playing_players) < 2:
            print("Only one player remains!")
            print("GAME OVER, thank you for playing.")
            break

        # Player's turns
        for j in playing_players:
            j.make_bid()
            j.draw_card(deck.get_card())
            j.declare_card()
        # Policing for game modes 2 and 3:
        if gamemode == "2" or gamemode == "3":
            # We need to reset the .checked attribute to enable subsequent rounds of policing
            reset_policed_attributes(player_list)
            # Now we can police
            run_round_of_policing(player_list)

        # Sum round pot
        pot = sum_pot(playing_players)

        # Settle game: check draws, declare winner and split pot
        settle_game(playing_players, pot, current_round, game_data)
        # Prepare to move on to next round
        current_round += 1
    print("GAME OVER, thank you for playing.")
    """ DATA EXPORTING """
    # Export game data to a file with an assigned name
    export_data(game_data, 'game_data.csv')


if __name__ == "__main__":
    main()
