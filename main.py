import random
from tkinter import *

from gameclasses import *
from guiclasses import *

# default constants for the game creation menu
DEFAULT_NUM_PLAYERS = "5"
DEFAULT_DECK = "basedeck"
DEFAULT_SEEDS_PER_MARKET = "10"
DEFAULT_FILTER_PER_MARKET = "0"
DEFAULT_STARTING_COINS = "9"
DEFAULT_VAULT_SIZE = "3"
DEFAULT_NUM_ROUNDS = "10"

# constants to implement
DEFAULT_VAULT_EXPANSION_SIZE = "3"
DEFAULT_VAULT_EXPANSION_COST = "5"
WAIT_TIME_MS = 1000

game_started = False


def begin_game(round_amount, player_amount, deck_name, seed_amount, filter_amount, coin_amount, vault_size, gui_root):
    game = Game(round_amount, player_amount, deck_name, seed_amount, filter_amount, coin_amount, vault_size)
    play_round(game, gui_root)


def play_round(game, gui_root):
    # pull seeds from the deck and fill the market
    for i in range(game.seeds_per_market):
        rand = random.randint(0, len(game.deck.seeds) - 1)
        game.market.append(game.deck.seeds.pop(rand))

    # create variable that the program will wait until it gets changed to signal a user input
    waiting_variable = IntVar()

    # remove previous frame and create new frame for round
    gui_root.winfo_children()[0].destroy()
    round_frame = Frame(gui_root)
    round_frame.pack(expand=True, fill=BOTH)
    input_info = display_round(game, round_frame, waiting_variable)
    input_button = input_info[0]
    input_entry = input_info[1]
    info_text = input_info[2]
    gui_root.title("Round " + str(game.current_round))

    # let players make their decisions
    move_cache = []
    for i in range(game.num_players):
        player = game.players[i]
        input_entry.delete(0, "end")
        input_entry.insert(0, "Player " + str(player.number))

        # wait for input
        input_button.wait_variable(waiting_variable)
        move_cache.append(input_entry.get())

        # redisplay round based on player action
        input_info = display_round(game, round_frame, waiting_variable)
        input_button = input_info[0]
        input_entry = input_info[1]
        info_text = input_info[2]
        input_entry.delete(0, "end")
        input_entry.insert(0, "Player " + str(player.number))
    overlaps = check_move_overlap(move_cache)
    print(len(overlaps))
    for i in range(len(overlaps)):
        players_bidding = []
        for j in range(len(move_cache)):
            if int(move_cache[j][4]) == overlaps[i]:
                players_bidding.append(game.players[j])
        # update info text to show which players are bidding for which seed
        bidding_list = ""
        for x in range(len(players_bidding)):
            bidding_list += str(players_bidding[x].number)
            if x is not len(players_bidding) - 1:
                bidding_list += ", "
        info_text.configure(text="The following players are bidding for the "
                                 + game.market[overlaps[i]].name + ": " + bidding_list)
        # wait to let players read the text previously displayed
        #wait_for_time(gui_root, WAIT_TIME_MS)

        # get bidding input from each player
        bid_cache = []
        for y in range(len(players_bidding)):
            input_entry.delete(0, "end");
            input_entry.insert(0, "Bid for Player " + str(y))
            input_button.wait_variable(waiting_variable)
            bid_cache.append(input_entry.get())

            # update display of round
            input_info = display_round(game, round_frame, waiting_variable)
            input_button = input_info[0]
            input_entry = input_info[1]
            info_text = input_info[2]
        print(bid_cache)


def process_input(player, player_input, market):
    if player_input == "vault":
        player.vault.capacity += 3
    elif player_input[:3] == "buy":
        seed_num = int(player_input[4])
        player.vault.seeds.append(market.pop(seed_num))


def wait_for_time(gui_root, time):
    var = IntVar()
    gui_root.after(time, var.set(1))
    root.wait_variable(var)


def check_move_overlap(move_cache):
    seed_overlaps = []
    for i in range(len(move_cache)):
        if move_cache[i][:3] == "buy" and int(move_cache[i][4]) not in seed_overlaps:
            for j in range(i + 1, i + 1 + len(move_cache[i + 1:])):
                if move_cache[i][4] == move_cache[j][4]:
                    seed_overlaps.append(int(move_cache[i][4]))
                    break
    return seed_overlaps


# GAME WINDOW WIDGET
root = Tk()
root.geometry("1000x650")
root.title("Seed Game")

frame = Frame(root)
frame.pack(expand=True, fill=BOTH)

button1 = Button(frame, text="Start Game", command=lambda: begin_game(rounds_entry.get(), player_entry.get(),
                                                                      deck_entry.get(), seeds_entry.get(),
                                                                      filter_entry.get(), coins_entry.get(),
                                                                      vault_entry.get(), root))
button1.place(x=475, y=300)

# number of players
player_entry = Entry(frame, width=20)
player_entry.place(x=0, y=25)
player_entry.insert(0, DEFAULT_NUM_PLAYERS)
player_entry_text = Label(frame, text="Number of Players")
player_entry_text.place(x=0, y=0)

# deck name
deck_entry = Entry(frame, width=20)
deck_entry.place(x=0, y=100)
deck_entry.insert(0, DEFAULT_DECK)
deck_entry_text = Label(frame, text="Deck Name")
deck_entry_text.place(x=0, y=75)

# seeds per market
seeds_entry = Entry(frame, width=20)
seeds_entry.place(x=0, y=175)
seeds_entry.insert(0, DEFAULT_SEEDS_PER_MARKET)
seeds_entry_text = Label(frame, text="Seeds per Market")
seeds_entry_text.place(x=0, y=150)

# seeds filtered per market
filter_entry = Entry(frame, width=20)
filter_entry.place(x=0, y=250)
filter_entry.insert(0, DEFAULT_FILTER_PER_MARKET)
filter_entry_text = Label(frame, text="Seeds Filtered per Market")
filter_entry_text.place(x=0, y=225)

# starting number of coins
coins_entry = Entry(frame, width=20)
coins_entry.place(x=0, y=325)
coins_entry.insert(0, DEFAULT_STARTING_COINS)
coins_entry_text = Label(frame, text="Starting Coins")
coins_entry_text.place(x=0, y=300)

# starting vault size
vault_entry = Entry(frame, width=20)
vault_entry.place(x=0, y=400)
vault_entry.insert(0, DEFAULT_VAULT_SIZE)
vault_entry_text = Label(frame, text="Starting Vault Size")
vault_entry_text.place(x=0, y=375)

# number of rounds
rounds_entry = Entry(frame, width=20)
rounds_entry.place(x=0, y=475)
rounds_entry.insert(0, DEFAULT_NUM_ROUNDS)
rounds_entry_text = Label(frame, text="Number of Rounds")
rounds_entry_text.place(x=0, y=450)

root.resizable(False, False)
root.mainloop()

# start the game with randomization and preparation of game materials

# EACH ROUND:
# first the EPA director draws 9 seed cards and discards 2
# there are 3 market phases that the players can do one of the following in each one:
# 1. enter the bidding for a seed
# 2. enter the bidding for a contract
# 3. flip over a completed contract card to earn the rewards
# 4. pay to expand their seed vault
