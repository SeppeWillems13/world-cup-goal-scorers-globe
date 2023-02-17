import csv

import requests
from bs4 import BeautifulSoup


def get_birthplace_info(player_name):
    """
    Returns the birthplace information for a player by making a request to their
    Wikipedia page and parsing the response using BeautifulSoup.
    """
    response = requests.get(f"https://en.wikipedia.org/wiki/{player_name}")
    soup = BeautifulSoup(response.text, "html.parser")
    birthplace_th = soup.find("th", text="Place of birth")
    if birthplace_th:
        birthplace_info = birthplace_th.find_next_sibling("td")
        birthplace_link = birthplace_info.find("a")
        if birthplace_link:
            birthplace = birthplace_link.get("title")
        else:
            birthplace = birthplace_info.text.strip()
        return birthplace
    return None


def get_birthplace(player_name):
    birthplace = get_birthplace_info(player_name)
    if not birthplace:
        response = requests.get(f"https://en.wikipedia.org/wiki/{player_name} + (footballer)")
        birthplace = get_birthplace_info(response)
    if birthplace and "," in birthplace:
        birthplace = birthplace.replace(",", " -")
    return birthplace or "SEARCH MANUALLY"


def update_csv(_filename):
    players = []

    # Read the player data from the CSV file
    with open(_filename, "r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append(row)

    # Update the player data with the birthplace information
    for player in players:
        player_name = player["Player"]
        print(player_name)
        birthplace = get_birthplace(player_name)
        print(birthplace)
        player["BirthPlace"] = birthplace
        player["Latitude"] = 0.0
        player["Longitude"] = 0.0

    # Write the updated player data back to the CSV file
    with open("../edited_cvs/worldcupgoals_1930_2022.csv", 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.DictWriter(file, fieldnames=["Player", "Goals", "Years", "Country", "BirthPlace", "CountryOfBirth",
                                                  "Latitude",
                                                  "Longitude"])
        writer.writeheader()
        # Write the data rows
        for player in players:
            try:
                writer.writerow(player)
            except UnicodeEncodeError:
                # Try different encodings
                encodings = ["ISO-8859-1", "utf-16"]
                for encoding in encodings:
                    try:
                        encoded_birth_place = player["BirthPlace"].encode(encoding)
                        player["BirthPlace"] = encoded_birth_place.decode(encoding)
                        writer.writerow(player)
                        break
                    except UnicodeEncodeError:
                        continue


if __name__ == '__main__':
    filename = "../edited_cvs/worldcupgoals_1930_2022Legacy.csv"
    update_csv(filename)
