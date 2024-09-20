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


def get_clan_info():
    url = f"{BASE_URL}/clans/%23{CLAN_ID}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def get_clan_members():
    url = f"{BASE_URL}/clans/%23{CLAN_ID}/members"
    response = requests.get(url, headers=headers)
    return response.json().get("items", []) if response.status_code == 200 else None


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


@app.route("/player/<player_tag>")
def player_info(player_tag):
    player_info = get_player_info(player_tag)
    return render_template("player_info.html", player=player_info)


def get_player_info(player_tag):
    # Construct the API URL, replacing '#' with '%23'
    player_tag = player_tag.lstrip("#")  # Remove '#' if present
    url = f"{BASE_URL}/players/%23{player_tag}"
    response = requests.get(url, headers=headers)

    # Debugging output
    # print(f"Request URL: {url}")
    # print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        player_data = response.json()
        return {
            "name": player_data.get("name"),
            "tag": player_data.get("tag")[1:],  # Remove leading '#'
            "trophies": player_data.get("trophies"),
            "troops": player_data.get("troops", []),  # Ensure troops are included
        }
    return None


if __name__ == "__main__":
    app.run(debug=True)
