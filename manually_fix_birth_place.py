import csv


def get_manual_cities(_filename):
    players = []

    # Read the player data from the CSV file
    with open(_filename, "r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if '"' in row["BirthPlace"] or row["BirthPlace"] == "SEARCH MANUALLY":
                print(f"Enter the birth place for player {row['Player']}:")
                birth_place = input()
                row["BirthPlace"] = birth_place
            players.append(row)

    # Write the player data back to the CSV file
    with open(_filename, "w", encoding="ISO-8859-1", newline='') as file:
        fieldnames = ["Player", "Goals", "Years", "Country", "BirthPlace", "Latitude", "Longitude"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for player in players:
            writer.writerow(player)
    print(players)
    return players



if __name__ == '__main__':
    print("start")
    filename = "worldcupgoals.csv"
    get_manual_cities(filename)
    print("done")
