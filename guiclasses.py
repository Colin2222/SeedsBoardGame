from tkinter import *

PLAYER_WIDTH = 150
PLAYER_HEIGHT = 200
PLAYER_FONT_SIZE = 7

MARKET_WIDTH = 400
MARKET_HEIGHT = 300

SEED_WIDTH = 75
SEED_HEIGHT = 100

MARKET_ROW = 2
PLAYER_ROW = 3
INPUT_ROW = 4
INFO_ROW = 5

PLAYER_COLORS = ["cornflower blue", "dark orange", "spring green", "DarkOrchid2", "cyan"]
SEED_COLORS = ["SeaGreen1", "SteelBlue1", "SlateBlue2"]
INPUT_COLOR = "gray85"


def display_menu():
    pass


def display_round(game, frame, wait_var):
    # clear frame
    clear_frame(frame)

    # display market and player info
    display_market(game.market, frame)
    player_frame = Frame(frame, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
    player_frame.grid(row=PLAYER_ROW, column=0)
    for i in range(game.num_players):
        display_player(game.players[i], player_frame)

    # display text box to prompt
    input_frame = Frame(frame)
    input_frame.grid(row=INPUT_ROW, column=0)
    input_entry = Entry(frame, width=100)
    input_entry.grid(row=INPUT_ROW, column=0)
    input_button = Button(frame, text="Submit move", command=lambda: wait_var.set(1))
    input_button.grid(row=INPUT_ROW, column=1)

    # display text for last move / indication of bidding war on seed or contract
    info_frame = Frame(frame)
    info_frame.grid(row=INFO_ROW, column=0)
    info_text = Label(info_frame, text="Move information will appear here")
    info_text.pack()

    # display decisions buttons (actions, numbers, propose trade, etc.)

    # return input button and entry so user input can be collected in main game loop
    return [input_button, input_entry, info_text]


def display_seed(seed, frame, seed_num):
    canvas = Canvas(frame, bg=SEED_COLORS[seed.rarity], width=SEED_WIDTH, height=SEED_HEIGHT)
    canvas.create_text(SEED_WIDTH / 2, SEED_HEIGHT / 2, text=seed.name, fill="black", font="Helvetica 7 bold")
    canvas.grid(row=MARKET_ROW, column=seed_num)


def display_market(market, frame):
    market_frame = Frame(frame, width=MARKET_WIDTH, height=MARKET_HEIGHT)
    market_frame.grid(row=MARKET_ROW, column=0)
    for i in range(len(market)):
        display_seed(market[i], market_frame, i)


def display_player(player, frame):
    canvas = Canvas(frame, bg=PLAYER_COLORS[player.number], width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
    # add text for player title
    canvas.create_text(PLAYER_WIDTH / 2, PLAYER_HEIGHT / 6, text="Player " + str(player.number), fill="black",
                       font="Helvetica 14 bold")

    # add text for number of seeds held by player
    canvas.create_text(PLAYER_WIDTH / 2, 2 * (PLAYER_HEIGHT / 6),
                       text="Seeds: " + str(len(player.vault.seeds)) + "/" + str(player.vault.capacity),
                       fill="black", font="Helvetica 7")

    # add text for number of coins held by player
    canvas.create_text(PLAYER_WIDTH / 2, 3 * (PLAYER_HEIGHT / 6), text="Coins: " + str(player.coins),
                       fill="black", font="Helvetica 7")

    canvas.grid(row=PLAYER_ROW, column=player.number, sticky=E)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
