from flask import Flask, render_template
import configparser
import requests

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
MAX_LEVELS_BY_TOWNHALL = {
    1: {
        "Archer": 1,
        "Barbarian": 1,
        "Giant": 1,
        "Wall Breaker": 1,
        "Wall Wrecker": 1,
        "Battle Blimp": 1,
        "Stone Slammer": 1,
        "Siege Barracks": 1,
    },
    2: {
        "Archer": 2,
        "Barbarian": 2,
        "Giant": 2,
        "Wall Breaker": 2,
        "Wall Wrecker": 2,
        "Battle Blimp": 2,
        "Stone Slammer": 2,
        "Siege Barracks": 1,
    },
    5: {"Wall Wrecker": 5, "Battle Blimp": 5, "Stone Slammer": 5, "Siege Barracks": 3},
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


def api_request(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers)
    print(f"Request URL: {url} | Status Code: {response.status_code}")
    return response.json() if response.status_code == 200 else None


def get_clan_info():
    return api_request(f"/clans/%23{CLAN_ID}")


def get_clan_members():
    return api_request(f"/clans/%23{CLAN_ID}/members").get("items", [])


def get_player_info(player_tag):
    player_tag = player_tag.lstrip("#")  # Remove leading '#'
    return api_request(f"/players/%23{player_tag}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/clan_info")
def clan_info():
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
    max_levels = MAX_LEVELS_BY_TOWNHALL.get(town_hall_level, {})

    return render_template(
        "player_info.html",
        player=player,
        max_levels=max_levels,
        siege_machines=SIEGE_MACHINES,
    )


if __name__ == "__main__":
    app.run(debug=True)
