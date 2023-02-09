import csv
import requests
from bs4 import BeautifulSoup


def get_birthplace(player_name):
    # Make a GET request to the Wikipedia page for the player
    print(player_name)
    response = requests.get(f"https://en.wikipedia.org/wiki/{player_name}")
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the birthplace information on the page
    birthplace_th = soup.find("th", text="Place of birth")
    if birthplace_th:
        birthplace_info = birthplace_th.find_next_sibling("td")
    else:
        birthplace_info = None

    # Return the birthplace information if it was found
    # CHANGE so also countryOfBirth gets saved will be easier for getting coordinates later
    if birthplace_info:
        birthplace_link = birthplace_info.find("a")
        if birthplace_link:
            birthplace = birthplace_link.get("title")
        else:
            birthplace = birthplace_info.text.strip()
        print(birthplace)
        return birthplace
    else:
        return "SEARCH MANUALLY"


def update_csv(_filename):
    players = []

    # Read the player data from the CSV file
    with open(_filename, "r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append(row)

    # Update the player data with the birthplace and latitude/longitude information
    for player in players:
        player_name = player["Player"]
        birthplace = get_birthplace(player_name)
        if birthplace:
            player["BirthPlace"] = birthplace
        player["Latitude"] = 0.0
        player["Longitude"] = 0.0

    # Write the updated player data back to the CSV file
    with open(filename, 'w', newline='', encoding='ISO-8859-1') as file:
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
    print("start")
    filename = "worldcupgoals.csv"
    update_csv(filename)
    print("done")
