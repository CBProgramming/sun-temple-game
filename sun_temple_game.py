# The Sun Temple
# Chrisyopher Burrell
# 09/01/2018

import random

# functions

# runs main menu until user quits
def start_game():
    print("Welcome to the sun temple!")
    rules()    
    menu = True
    while menu == True:
        MENU_TEXT = ("\n1.  Play game\n2.  Rules\n"
                     "3.  Exit game\n")
        selection = input(MENU_TEXT)
        if selection == "1":
            play()
        elif selection == "2":
            rules()
        elif selection == "3":
            check = "Are you sure you want to quit (yes/no)?"
            if are_you_sure(check) == True:
                print("Thanks for playing!")
                menu = False
        else:
            print("Invalid choice, type a number from the "
                  "below options")

# function to check if user is sure with their choice
def are_you_sure(question):
    valid_input = False
    while valid_input == False:
        answer_if_sure = input(question).lower()
        if answer_if_sure == "yes" or answer_if_sure == "y":
            sure = True
            valid_input = True
        elif answer_if_sure == "no" or answer_if_sure == "n":
            sure = False
            valid_input = True
        else:
            print("Invalid input")
    return sure

# print rules
def rules():
    RULES = ("\nPlayers take turns to move around the board using "
            "a shared player token.\n* Players select their move "
            "from a move list\n* Once a move is selected it is "
            "removed from the move list for the remainder of the "
            "game\n* The player collects gems from every board "
            "space they move accross, including the space they "
            "end their move on.\n* The board is randomly seeded "
            "with a fixed set of gems.\n* There are 7 rubies (r), "
            "7 emeralds (e), 7 diamonds (d), 7 sapphires (s) and "
            "11 glass beads (g).\n* Scoring is based on the "
            "natural number system.  The first ruby a player "
            "collects is worth 1 point, the second ruby is worth "
            "an additional 2 points, the third ruby is worth an "
            "additional 3 points and so on.\n* Each gem stone, "
            "except the glass bead, has the same scoring system, "
            "but is counted separately.  For example if a player "
            "has 2 rubies and 3 emeralds, their rubies are worth "
            "3 points and their emeralds are worth 6 points, "
            "giving a total score of 9 points.\n* Glass beads "
            "subtract from a players total score rather than add "
            "to it.  They do so using the same scoring system.  "
            "The first glass bead deducts 1 point, the scond glass "
            "bead deducts a further 2 points and so on.\n* When "
            "the player token reaches the final board space the "
            "game is over.\n* When the game ends, the player with "
            "the most points is the winner.")
    print(RULES)

# initialise board
def populate_board(gem_board, ROW_AMOUNT, COLUMN_AMOUNT):
    gem = ["r", "e", "d", "s"] * 7 + ["g"] * 11
    random.shuffle(gem)
    gem_board[0] = "*"
    for board_index in range(1,ROW_AMOUNT * COLUMN_AMOUNT):
        gem_board[board_index]= (gem[board_index - 1])
    return gem_board

# display board state
def draw_board(ROW_AMOUNT, COLUMN_AMOUNT, game_board):
    print("\n")
    PIPE = "|"
    DASHES = "---"
    for row_index in range(ROW_AMOUNT):
        edge = ""
        space = ""
        for col_index in range(COLUMN_AMOUNT):
            edge = edge + PIPE + DASHES
            board_index = row_index * COLUMN_AMOUNT + col_index
            if row_index % 2 == 1:
                board_index = (row_index * COLUMN_AMOUNT
                + (COLUMN_AMOUNT - col_index) - 1)
            space = (space + PIPE + " " + game_board[board_index]
                     + " ")
        edge += PIPE
        space += PIPE
        print(edge)
        print(space)
    print(edge)

# get player names
def get_names(NUMBER_PLAYERS):
    player_name = []
    for players in range(NUMBER_PLAYERS):
        valid_name = False
        while valid_name == False:
            name = input("\nPlease enter player "
                         + str(players + 1) + "'s name: ")
            if " ".join(name.split()) == "":
                print("\nInvalid name entered.  Please enter "
                      + str(players + 1) + "'s name: ")
            else:
                valid_name = True
                player_name.append(" ".join(name.split()))
    return player_name

# set up score dictionary with player names
def initialise_gem_collections(NUMBER_PLAYERS, names_of_players):
    player_gems = {}
    for players in range(NUMBER_PLAYERS):
        player_gems[names_of_players[players]] = {}
        header = ["r","e","d","s","g","Score"]
        for gem in header:
            player_gems[names_of_players[players]][gem] = 0
    return player_gems

# gets player move
def get_player_move(available_moves, active_player):
    print("\nIt's your turn " + active_player + "!")
    print("\nAvailable moves:",available_moves)
    valid_move = False
    while valid_move == False:
        chosen_move = input("\nPlease choose how far to move "
                            "from the available moves above: ")
        if chosen_move.isdigit() == True:
            if int(chosen_move) in available_moves:
                available_moves.remove(int(chosen_move))
                valid_move = True
            else:
                print("\nNumber is not in list of moves.")
        else:
            print("\nInvalid input.  Input must be a number from the "
                  "list of moves.")     
    return int(chosen_move)

# update player position
def move_player(old_place, move, board_size):
    if old_place + move > board_size:
        new_position = board_size
    else:
        new_position = old_place + move
    return new_position

# update gem collection
def update_gem_collection(old_space, new_space, game_board,
                          player_gems, player_name):
    game_board[old_space] = " "
    gem_collector = old_space + 1
    while gem_collector <= new_space:
        current_gem = game_board[gem_collector]
        player_gems[player_name][current_gem] += 1
        game_board[gem_collector] = " "
        gem_collector = gem_collector + 1
    game_board[new_space] = "*"
    return player_gems, game_board

# calculate scores
def calculate_scores(player_gem,NUMBER_PLAYERS,names):
    for players in range(NUMBER_PLAYERS):
        ruby = natural_number(player_gem,names,"r",players)
        emerald = natural_number(player_gem,names,"e",players)
        diamond = natural_number(player_gem,names,"d",players)
        sapphire = natural_number(player_gem,names,"s",players)
        glass = -natural_number(player_gem,names,"g",players)
        player_gem[names[players]]["Score"] = int(ruby + emerald
                                + diamond + sapphire + glass)

# calculate natural number
def natural_number(player_gems,names_of_players,gem_id,player_index):
    natural_num = (player_gems[names_of_players[player_index]][gem_id]
    * (player_gems[names_of_players[player_index]][gem_id] + 1) / 2)
    return natural_num


# output collections
def output_collections(player_gems,NUMBER_PLAYERS,names_of_players):
    print("\nCurrent gem collections:")
    for players in range(NUMBER_PLAYERS):
        rubies = str(player_gems[names_of_players[players]]["r"])
        emeralds = str(player_gems[names_of_players[players]]["e"])
        diamonds = str(player_gems[names_of_players[players]]["d"])
        sapphires = str(player_gems[names_of_players[players]]["s"])
        glass = str(player_gems[names_of_players[players]]["g"])
        score = str(player_gems[names_of_players[players]]["Score"])
        print("\n" + names_of_players[players] + "'s Collection: "
              "Rubies: " + rubies + ", Emeralds: " + emeralds
              + ", Diamonds: " + diamonds + ", Sapphires: "
              + sapphires + ", Glass Beads: " + glass + ", Score: "
              + score)

# determine and print the winner
def determine_winner(player_gems,NUMBER_PLAYERS,names_of_players):
    winner_index = 0
    is_draw = False
    for players in range(1,NUMBER_PLAYERS):
        if (player_gems[names_of_players[players]]["Score"]
        == player_gems[names_of_players[winner_index]]["Score"]):
            is_draw = True
        else:
            if (player_gems[names_of_players[players]]["Score"]
            > player_gems[names_of_players[winner_index]]["Score"]):
                winner_index = players
                is_draw = False
    if is_draw:
        print("\nIt's a draw!")
    else:
        print("\n" + names_of_players[winner_index] + " has won!")
             
# run game
def play():
    # initialise variables
    NUM_PLAYERS = 2
    ROW_COUNT = 5
    COLUMN_COUNT = 8
    player_board_position = 0
    turn_count = 0
    board = [""] * ROW_COUNT * COLUMN_COUNT
    moves_available = [0,1,1,2,2,3,3,4,4,5,5,6,6]
    gems = ["r", "e", "d", "s"] * 7 + ["g"] * 11
    game_on = True
    # get player names
    player_names = get_names(NUM_PLAYERS)
    # set up dictionary of player scores
    gem_collections = initialise_gem_collections(NUM_PLAYERS,
                                                 player_names)
    # shuffles gems and populates board
    board = populate_board(board, ROW_COUNT, COLUMN_COUNT)     
    # draws board
    draw_board(ROW_COUNT, COLUMN_COUNT, board)
    while game_on:
        active_player = turn_count % NUM_PLAYERS
        turn_count = turn_count + 1
        active_player_name = player_names[active_player]
        # gets player move
        player_move = get_player_move(moves_available,
                                      active_player_name)
        # update player position
        old_position = player_board_position
        player_board_position = move_player(old_position,
                                            player_move,
                                            len(board) - 1)
        # collect gems from board
        gem_collections, board = update_gem_collection(old_position,
                                                       player_board_position,
                                                       board,
                                                       gem_collections,
                                                       active_player_name)
        # show board state
        draw_board(ROW_COUNT, COLUMN_COUNT, board)
        # calculate score
        calculate_scores(gem_collections,NUM_PLAYERS,player_names)
        #output collections and scores
        output_collections(gem_collections,NUM_PLAYERS,player_names)
        # test if game has ended
        if player_board_position == len(board) - 1:
            game_on = False
    determine_winner(gem_collections,NUM_PLAYERS,player_names)

# main
start_game()
