from flask import Flask, render_template
import configparser
import requests
import random

app = Flask(__name__)

# Load the config file
Config = configparser.ConfigParser()
Config.read("config.ini")

# Get API token and Clan ID from the config file
API_TOKEN = Config.get("clashofclans", "api_token")
CLAN_ID = Config.get("clashofclans", "clan_id")

BASE_URL = "https://api.clashofclans.com/v1"
headers = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

# Define max levels for troops based on Town Hall levels
ELIXIR_TROOPS_MAX_LEVELS_BY_LAB = {
    1: {"Archer": 2, "Barbarian": 2, "Goblin": 2},
    2: {
        "Archer": 2,
        "Barbarian": 2,
        "Goblin": 2,
        "Giant": 2,
        "Balloon": 2,
        "Wall Breaker": 2,
    },
    3: {
        "Archer": 3,
        "Barbarian": 3,
        "Goblin": 3,
        "Giant": 2,
        "Balloon": 2,
        "Wall Breaker": 2,
        "Wizard": 2,
    },
    4: {
        "Archer": 3,
        "Barbarian": 3,
        "Goblin": 3,
        "Giant": 3,
        "Balloon": 3,
        "Wall Breaker": 3,
        "Wizard": 3,
    },
    5: {
        "Archer": 4,
        "Barbarian": 4,
        "Goblin": 4,
        "Giant": 4,
        "Balloon": 4,
        "Wall Breaker": 4,
        "Wizard": 4,
        "Healer": 2,
        "Dragon": 2,
    },
    6: {
        "Archer": 5,
        "Barbarian": 5,
        "Goblin": 5,
        "Giant": 5,
        "Balloon": 5,
        "Wall Breaker": 5,
        "Wizard": 5,
        "Healer": 3,
        "Dragon": 3,
        "P.E.K.K.A": 3,
    },
    7: {
        "Archer": 6,
        "Barbarian": 6,
        "Goblin": 6,
        "Giant": 6,
        "Balloon": 6,
        "Wall Breaker": 5,
        "Wizard": 6,
        "Healer": 4,
        "Dragon": 4,
        "P.E.K.K.A": 4,
        "Baby Dragon": 2,
    },
    8: {
        "Archer": 7,
        "Barbarian": 7,
        "Goblin": 7,
        "Giant": 7,
        "Balloon": 6,
        "Wall Breaker": 6,
        "Wizard": 7,
        "Healer": 4,
        "Dragon": 5,
        "P.E.K.K.A": 6,
        "Baby Dragon": 4,
        "Miner": 3,
    },
    9: {
        "Archer": 8,
        "Barbarian": 8,
        "Goblin": 7,
        "Giant": 8,
        "Balloon": 7,
        "Wall Breaker": 7,
        "Wizard": 8,
        "Healer": 5,
        "Dragon": 6,
        "P.E.K.K.A": 7,
        "Baby Dragon": 5,
        "Miner": 5,
        "Electro Dragon": 2,
    },
    10: {
        "Archer": 9,
        "Barbarian": 9,
        "Goblin": 8,
        "Giant": 9,
        "Balloon": 8,
        "Wall Breaker": 8,
        "Wizard": 9,
        "Healer": 5,
        "Dragon": 7,
        "P.E.K.K.A": 8,
        "Baby Dragon": 6,
        "Miner": 6,
        "Electro Dragon": 3,
        "Yeti": 2,
    },
    11: {
        "Archer": 9,
        "Barbarian": 9,
        "Goblin": 8,
        "Giant": 10,
        "Balloon": 9,
        "Wall Breaker": 9,
        "Wizard": 10,
        "Healer": 6,
        "Dragon": 8,
        "P.E.K.K.A": 9,
        "Baby Dragon": 7,
        "Miner": 7,
        "Electro Dragon": 4,
        "Yeti": 3,
        "Dragon Rider": 2,
    },
    12: {
        "Archer": 10,
        "Barbarian": 10,
        "Goblin": 8,
        "Giant": 10,
        "Balloon": 10,
        "Wall Breaker": 10,
        "Wizard": 10,
        "Healer": 7,
        "Dragon": 9,
        "P.E.K.K.A": 9,
        "Baby Dragon": 8,
        "Miner": 8,
        "Electro Dragon": 5,
        "Yeti": 4,
        "Dragon Rider": 3,
        "Electro Titan": 2,
    },
    13: {
        "Archer": 11,
        "Barbarian": 11,
        "Goblin": 9,
        "Giant": 11,
        "Balloon": 10,
        "Wall Breaker": 11,
        "Wizard": 11,
        "Healer": 8,
        "Dragon": 10,
        "P.E.K.K.A": 10,
        "Baby Dragon": 9,
        "Miner": 10,
        "Electro Dragon": 6,
        "Yeti": 5,
        "Dragon Rider": 3,
        "Electro Titan": 3,
        "Root Rider": 2,
    },
    14: {
        "Archer": 12,
        "Barbarian": 12,
        "Goblin": 9,
        "Giant": 12,
        "Balloon": 12,
        "Wall Breaker": 12,
        "Wizard": 12,
        "Healer": 9,
        "Dragon": 11,
        "P.E.K.K.A": 11,
        "Baby Dragon": 10,
        "Miner": 10,
        "Electro Dragon": 7,
        "Yeti": 5,
        "Dragon Rider": 4,
        "Electro Titan": 2,
        "Root Rider": 3,
    },
}

SPELLS_MAX_LEVELS_BY_LAB = {
    1: {"Lightning Spell": 2},
    2: {"Lightning Spell": 3, "Healing Spell": 2},
    3: {"Lightning Spell": 4, "Healing Spell": 2, "Rage Spell": 2},
    4: {"Lightning Spell": 4, "Healing Spell": 3, "Rage Spell": 3},
    5: {"Lightning Spell": 4, "Healing Spell": 4, "Rage Spell": 4, "Jump Spell": 2},
    6: {
        "Lightning Spell": 5,
        "Healing Spell": 5,
        "Rage Spell": 5,
        "Jump Spell": 2,
        "Poison Spell": 2,
        "Earthquake Spell": 2,
    },
    7: {
        "Lightning Spell": 6,
        "Healing Spell": 6,
        "Rage Spell": 5,
        "Jump Spell": 2,
        "Freeze Spell": 2,
        "Poison Spell": 3,
        "Earthquake Spell": 3,
        "Haste Spell": 2,
    },
    8: {
        "Lightning Spell": 7,
        "Healing Spell": 7,
        "Rage Spell": 5,
        "Jump Spell": 3,
        "Freeze Spell": 5,
        "Clone Spell": 3,
        "Poison Spell": 4,
        "Earthquake Spell": 4,
        "Haste Spell": 4,
        "Skeleton Spell": 3,
        "Bat Spell": 3,
    },
    9: {
        "Lightning Spell": 8,
        "Healing Spell": 7,
        "Rage Spell": 5,
        "Jump Spell": 3,
        "Freeze Spell": 6,
        "Clone Spell": 5,
        "Invisibility Spell": 2,
        "Poison Spell": 5,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 4,
        "Bat Spell": 4,
    },
    10: {
        "Lightning Spell": 9,
        "Healing Spell": 7,
        "Rage Spell": 6,
        "Jump Spell": 3,
        "Freeze Spell": 7,
        "Clone Spell": 5,
        "Invisibility Spell": 3,
        "Poison Spell": 6,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 6,
        "Bat Spell": 5,
        "Overgrowth Spell": 2,
    },
    11: {
        "Lightning Spell": 9,
        "Healing Spell": 8,
        "Rage Spell": 6,
        "Jump Spell": 4,
        "Freeze Spell": 7,
        "Clone Spell": 6,
        "Invisibility Spell": 4,
        "Poison Spell": 7,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 7,
        "Bat Spell": 5,
        "Recall Spell": 2,
        "Overgrowth Spell": 2,
    },
    12: {
        "Lightning Spell": 9,
        "Healing Spell": 8,
        "Rage Spell": 6,
        "Jump Spell": 4,
        "Freeze Spell": 7,
        "Clone Spell": 7,
        "Invisibility Spell": 4,
        "Poison Spell": 8,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 7,
        "Bat Spell": 5,
        "Recall Spell": 3,
        "Overgrowth Spell": 3,
    },
    13: {
        "Lightning Spell": 10,
        "Healing Spell": 9,
        "Rage Spell": 6,
        "Jump Spell": 5,
        "Freeze Spell": 7,
        "Clone Spell": 8,
        "Invisibility Spell": 4,
        "Poison Spell": 9,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 8,
        "Bat Spell": 6,
        "Recall Spell": 4,
        "Overgrowth Spell": 3,
    },
    14: {
        "Lightning Spell": 11,
        "Healing Spell": 10,
        "Rage Spell": 6,
        "Jump Spell": 4,
        "Freeze Spell": 7,
        "Clone Spell": 6,
        "Invisibility Spell": 4,
        "Poison Spell": 10,
        "Earthquake Spell": 5,
        "Haste Spell": 5,
        "Skeleton Spell": 7,
        "Bat Spell": 5,
        "Recall Spell": 5,
        "Overgrowth Spell": 4,
    },
}

DARK_ELIXIR_TROOPS_MAX_LEVELS_BY_LAB = {
    5: {"Minion": 2, "Hog Rider": 2},
    6: {"Minion": 4, "Hog Rider": 4, "Valkyrie": 2, "Golem": 2},
    7: {
        "Minion": 5,
        "Hog Rider": 5,
        "Valkyrie": 4,
        "Golem": 4,
        "Witch": 2,
        "Lava Hound": 2,
    },
    8: {
        "Minion": 6,
        "Hog Rider": 6,
        "Valkyrie": 5,
        "Golem": 5,
        "Witch": 3,
        "Lava Hound": 3,
        "Bowler": 2,
    },
    9: {
        "Minion": 7,
        "Hog Rider": 7,
        "Valkyrie": 6,
        "Golem": 7,
        "Witch": 4,
        "Lava Hound": 4,
        "Bowler": 3,
        "Ice Golem": 3,
    },
    10: {
        "Minion": 8,
        "Hog Rider": 9,
        "Valkyrie": 7,
        "Golem": 9,
        "Witch": 5,
        "Lava Hound": 5,
        "Bowler": 4,
        "Ice Golem": 5,
        "Headhunter": 2,
    },
    11: {
        "Minion": 9,
        "Hog Rider": 10,
        "Valkyrie": 8,
        "Golem": 10,
        "Witch": 5,
        "Lava Hound": 6,
        "Bowler": 5,
        "Ice Golem": 5,
        "Headhunter": 3,
        "Apprentice Warden": 2,
    },
    12: {
        "Minion": 10,
        "Hog Rider": 10,
        "Valkyrie": 9,
        "Golem": 10,
        "Witch": 5,
        "Lava Hound": 6,
        "Bowler": 5,
        "Ice Golem": 6,
        "Headhunter": 3,
        "Apprentice Warden": 3,
        "Druid": 2,
    },
    13: {
        "Minion": 11,
        "Hog Rider": 12,
        "Valkyrie": 10,
        "Golem": 12,
        "Witch": 6,
        "Lava Hound": 6,
        "Bowler": 7,
        "Ice Golem": 7,
        "Headhunter": 2,
        "Apprentice Warden": 4,
        "Druid": 3,
    },
    14: {
        "Minion": 7,
        "Hog Rider": 7,
        "Valkyrie": 6,
        "Golem": 7,
        "Witch": 4,
        "Lava Hound": 6,
        "Bowler": 3,
        "Ice Golem": 3,
        "Headhunter": 2,
        "Apprentice Warden": 4,
        "Druid": 3,
    },
}

SIEGE_MACHINES_MAX_LEVELS_BY_LAB = {
    10: {"Wall Wrecker": 3, "Battle Blimp": 3, "Stone Slammer": 3},
    11: {
        "Wall Wrecker": 4,
        "Battle Blimp": 4,
        "Stone Slammer": 4,
        "Siege Barracks": 4,
        "Log Launcher": 4,
    },
    12: {
        "Wall Wrecker": 4,
        "Battle Blimp": 4,
        "Stone Slammer": 4,
        "Siege Barracks": 4,
        "Log Launcher": 4,
        "Flame Flinger": 4,
    },
    13: {
        "Wall Wrecker": 5,
        "Battle Blimp": 4,
        "Stone Slammer": 5,
        "Siege Barracks": 4,
        "Log Launcher": 4,
        "Flame Flinger": 4,
        "Battle Drill": 4,
    },
    14: {
        "Wall Wrecker": 5,
        "Battle Blimp": 4,
        "Stone Slammer": 5,
        "Siege Barracks": 5,
        "Log Launcher": 5,
        "Battle Drill": 4,
        "Flame Flinger": 4,
    },
    # Add for higher Town Hall levels...
}

SIEGE_MACHINES = [
    "Wall Wrecker",
    "Battle Blimp",
    "Stone Slammer",
    "Siege Barracks",
    "Log Launcher",
    "Flame Flinger",
    "Battle Drill",
]

# Define max levels for pets based on Town Hall levels
DARK_ELIXIR_TROOPS = [
    "Minion",
    "Hog Rider",
    "Valkyrie",
    "Golem",
    "Witch",
    "Lava Hound",
    "Bowler",
    "Ice Golem",
    "Headhunter",
    "Apprentice Warden",
    "Druid",
]

PETS = [
    "L.A.S.S.I",
    "Electro Owl",
    "Mighty Yak",
    "Unicorn",
    "Frosty",
    "Diggy",
    "Poison Lizard",
    "Phoenix",
    "Spirit Fox",
]
MAX_LEVELS_BY_TOWNHALL_PETS = {
    14: {"L.A.S.S.I": 10, "Electro Owl": 10, "Mighty Yak": 10, "Unicorn": 10},
    15: {
        "L.A.S.S.I": 15,
        "Electro Owl": 10,
        "Mighty Yak": 15,
        "Unicorn": 10,
        "Frosty": 10,
        "Diggy": 10,
        "Poison Lizard": 10,
        "Phoenix": 10,
    },
    16: {
        "L.A.S.S.I": 15,
        "Electro Owl": 15,
        "Mighty Yak": 15,
        "Unicorn": 10,
        "Frosty": 10,
        "Diggy": 10,
        "Poison Lizard": 10,
        "Phoenix": 10,
        "Spirit Fox": 10,
    },
}


def api_request(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers)
    print(f"Request URL: {url} | Status Code: {response.status_code}")
    return response.json() if response.status_code == 200 else None


def get_clan_info():
    url = f"{BASE_URL}/clans/%23{CLAN_ID}"
    response = requests.get(url, headers=headers)

    # Debugging output
    print(f"Request URL: {url}")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        clan_data = response.json()
        return {
            "name": clan_data.get("name"),
            "tag": clan_data.get("tag"),
            "trophies": clan_data.get("trophies"),
            "builderTrophies": clan_data.get("builderTrophies"),
            "warLeague": clan_data.get("warLeague"),
            "wins": clan_data.get("warWins"),
            "losses": clan_data.get("warLosses"),
            "location": clan_data.get("location"),
            "badgeUrls": clan_data.get("badgeUrls"),
        }
    return None


def get_clan_members():
    return api_request(f"/clans/%23{CLAN_ID}/members").get("items", [])


def get_player_info(player_tag):
    player_tag = player_tag.lstrip("#")  # Remove leading '#'
    return api_request(f"/players/%23{player_tag}")


@app.route("/")
def home():
    clan = get_clan_info()
    return render_template("clan_info.html", clan=clan)


@app.route("/clan_members")
def clan_members():
    members = get_clan_members()
    return render_template("clan_members.html", members=members)


@app.route("/player/<tag>")
def player_info(tag):
    player = get_player_info(tag)
    town_hall_level = player.get("townHallLevel", 1)  # Default to 1 if not found

    # Calculate the laboratory level (lab starts at Town Hall 3)
    laboratory_level = max(1, town_hall_level - 2)

    # Fetch the correct max levels based on laboratory level
    elixir_troop_max_levels = ELIXIR_TROOPS_MAX_LEVELS_BY_LAB.get(laboratory_level, {})
    dark_elixir_troop_max_levels = DARK_ELIXIR_TROOPS_MAX_LEVELS_BY_LAB.get(
        laboratory_level, {}
    )
    siege_machine_max_levels = SIEGE_MACHINES_MAX_LEVELS_BY_LAB.get(
        laboratory_level, {}
    )
    spells_max_levels = SPELLS_MAX_LEVELS_BY_LAB.get(laboratory_level, {})
    # builder_base_max_levels = BUILDER_BASE_MAX_LEVELS_BY_LAB.get(laboratory_level, {})

    pets_max_levels = MAX_LEVELS_BY_TOWNHALL_PETS.get(town_hall_level, {})

    return render_template(
        "player_info.html",
        player=player,
        town_hall_level=town_hall_level,
        elixir_troop_max_levels=elixir_troop_max_levels,
        dark_elixir_troop_max_levels=dark_elixir_troop_max_levels,
        siege_machines=SIEGE_MACHINES,
        siege_machine_max_levels=siege_machine_max_levels,
        spells_max_levels=spells_max_levels,
        dark_elixir_troops=DARK_ELIXIR_TROOPS,
        pets_max_levels=pets_max_levels,
        pets=PETS,
        # builder_base_max_levels=builder_base_max_levels,
    )


def create_roster(
    available_any_day, available_one_to_two_days, total_days=7, roster_size=15
):
    # Initialize the roster dictionary
    roster = {f"Day {i}": [] for i in range(1, total_days + 1)}

    # Distribute members available any day
    for i in range(len(available_any_day)):
        day = f"Day {i % total_days + 1}"  # Rotate across days
        roster[day].append(available_any_day[i])

    # Randomly assign members available one or two days
    for member in available_one_to_two_days:
        chosen_days = random.sample(range(1, total_days + 1), 2)
        for day in chosen_days:
            if len(roster[f"Day {day}"]) < roster_size:
                roster[f"Day {day}"].append(member)

    # Balance out rosters to ensure 15 members per day
    for day in roster:
        while len(roster[day]) < roster_size:
            random_member = random.choice(available_any_day + available_one_to_two_days)
            if random_member not in roster[day]:
                roster[day].append(random_member)

    return roster


@app.route("/roster")
def roster_page():
    # Initialize your lists
    available_any_day = [
        "Ace",
        "coco974",
        "岑汝轩",
        "ZeroDay",
        "sim sim",
        "Hiken",
        "Lucille",
        "Suki",
        "Lakaï",
        "TiboTango",
        "Thiboss",
        "ru xuan",
    ]  # Fill this list with player names available any day
    available_one_to_two_days = [
        "Shinra",
        "Sim",
        "Cocoque",
        "Bakasable",
        "SimSim",
        "mr.khas",
        "Will",
        "Kazuto",
    ]

    # Create the roster
    roster = create_roster(available_any_day, available_one_to_two_days)

    # Render the roster template and pass the roster data
    return render_template("roster.html", roster=roster)


if __name__ == "__main__":
    app.run(debug=True)
