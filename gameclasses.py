from xml.dom.minidom import parse


# SEED CLASS
# name: display name in game
# rarity: on a scale of 0 beyond (currently 0-2, common uncommon and rare seeds)
# climate: number 0-4 to show which climate the seed grows best in (polar,continental,temperate,dry,tropical)
# point_value: how many points the seed is worth when held at the end of the game
class Seed:
    def __init__(self, name, rarity, climate, point_value):
        self.name = name
        self.rarity = int(rarity)
        self.climate = climate
        self.point_value = point_value


class Contract:
    def __init__(self, seeds, point_value, round_reward, instant_reward, duration):
        self.seeds = seeds
        self.point_value = point_value
        self.round_reward = round_reward
        self.instant_reward = instant_reward
        self.duration = duration


class Deck:
    # list of seeds that are currently in the deck, will be populated by individual seed objects once deck is populated
    seeds = []
    contracts = []

    def __init__(self, filename):
        self.filename = filename

    def populate(self):
        deck_doc = parse(self.filename)
        deck_element = deck_doc.documentElement
        seed_nodes = deck_element.getElementsByTagName("seed")
        for i in range(len(seed_nodes)):
            current_node = seed_nodes[i]
            num_seeds = int(current_node.getAttribute("quantity"))
            # makes a copy of the seed object to add to the deck according to the quantity stated for the deck
            # possibly change so it doesnt call constructor every time, instead it should duplicate original to ^ speed
            for j in range(num_seeds):
                current_seed = Seed(current_node.getAttribute("name"), current_node.getAttribute("rarity"),
                                    current_node.getAttribute("climate"), current_node.getAttribute("point_value"))
                self.seeds.append(current_seed)


class Vault:
    def __init__(self, capacity):
        if type(capacity) == int:
            self.capacity = capacity
        elif type(capacity) == str:
            self.capacity = int(capacity)
        self.seeds = []


class Player:
    def __init__(self, vault_size, coins, number):
        self.vault = Vault(vault_size)
        self.coins = coins
        self.current_contracts = []
        self.completed_contracts = []
        self.number = number


class Game:
    players = []
    market = []
    discard = []

    def __init__(self, num_rounds, num_players, deck_name, seeds_per_market, filter_per_market, starting_coins,
                 starting_vault_size):
        self.current_round = 0
        self.num_rounds = int(num_rounds)

        self.num_players = int(num_players)
        self.deck = Deck(deck_name + ".xml")
        self.deck.populate()

        self.seeds_per_market = int(seeds_per_market)
        self.filter_per_market = int(filter_per_market)

        for i in range(self.num_players):
            self.players.append(Player(int(starting_vault_size), int(starting_coins), i))
