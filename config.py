import configparser
import requests

# Load the config file
Config = configparser.ConfigParser()
Config.read("config.ini")

# Get API token and Clan ID from the config file
API_TOKEN = Config.get("clashofclans", "api_token_4G")
CLAN_ID = Config.get("clashofclans", "clan_id")

# Clash of Clans API base URL
BASE_URL = "https://api.clashofclans.com/v1"

# Headers for API request (required to authorize the request)
headers = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}


# Function to get clan information
def get_clan_info():
    url = f"{BASE_URL}/clans/%23{CLAN_ID}"  # Clan ID needs to be prefixed with %23 to represent '#'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get clan info. Status Code: {response.status_code}")
        return None


# Function to get clan members
def get_clan_members():
    url = f"{BASE_URL}/clans/%23{CLAN_ID}/members"
    response = requests.get(url, headers=headers)
    members = response.json().get("items", []) if response.status_code == 200 else []
    # Add tag to each member for routing
    for member in members:
        member["tag"] = member["tag"][1:]  # Remove leading '#' for the URL
    return members


# Display clan information
def display_clan_info(clan_info):
    if clan_info:
        print(f"Clan Name: {clan_info['name']}")
        print(f"Clan Level: {clan_info['clanLevel']}")
        print(f"Clan Points: {clan_info['clanPoints']}")
        print(f"Members: {clan_info['members']}")
        print(f"Location: {clan_info['location']['name']}")
        print(f"Description: {clan_info['description']}")
    else:
        print("No clan information available.")


# Display clan members
def display_clan_members(clan_members):
    if clan_members:
        print("\nClan Members:")
        for member in clan_members:
            print(
                f"- {member['name']} (Role: {member['role']}, Trophies: {member['trophies']})"
            )
    else:
        print("No clan members available.")


def get_player_info(player_tag):
    url = f"{BASE_URL}/players/%23{player_tag}"  # Use %23 to replace the '#' character
    response = requests.get(url, headers=headers)

    # Print the status code and response for debugging
    print(f"Request URL: {url}")
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())  # Print the entire response

    if response.status_code == 200:
        player_data = response.json()
        return {
            "name": player_data.get("name"),
            "tag": player_data.get("tag")[1:],  # Remove leading '#'
            "trophies": player_data.get("trophies"),
            "troops": player_data.get("troops", []),  # Ensure troops are included
        }
    return None


# Main function to display clan info and members
def main():
    # Get clan information
    clan_info = get_clan_info()
    display_clan_info(clan_info)

    # Get clan members
    clan_members = get_clan_members()
    display_clan_members(clan_members)


if __name__ == "__main__":
    main()
