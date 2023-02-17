import csv
import requests
from bs4 import BeautifulSoup

# define the URL template
url_template = 'https://www.thesoccerworldcups.com/players/{}.php'
players = []

# open the CSV file in write mode and write a header row
with open('../edited_cvs/worldcupgoals_1930_2022Legacy.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        players.append(row)
# prompt user for the country name
country = input("Enter the country name: ")

# process each player in the filtered rows
for player in players:
    if player["Country"] == country:
        # convert the player's name to lowercase and replace spaces with underscores
        player_name = player['Player'].lower().replace(' ', '_')
        if(player_name == "eric_maxim_choupo-moting"):
            player_name = "eric_choupo_moting"
        # generate the player's URL and send a GET request
        url = url_template.format(player_name)
        response = requests.get(url)

        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # extract player information
        player_info = soup.find('div', class_='margen-y15 clearfix margen-t0')

        # extract name, born date, position, jersey number, and height
        if player_info is None:
            print(f"Unable to find player info for {player_name}")
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{player_name} {player['Country']} {player['Years']}\n")
            continue

        name = player_info.find('h2', class_='t-enc-1 margen-t0').text
        born_date = player_info.find('td', string='Born Date:').find_next_sibling('td').text
        position = player_info.find('td', string='Position:').find_next_sibling('td').text
        jersey_number_elem = player_info.find('td', string='Jersey Number:').find_next_sibling('td')
        jersey_number = ','.join(
            [num.strip() for num in jersey_number_elem.text.split(',')]) if jersey_number_elem else ''

        # print the information
        print(f"Name: {name.encode('utf-8')}")
        print(f"Born Date: {born_date}")
        print(f"Position: {position}")
        print(f"Jersey Number: {jersey_number}")

        # Find the table with class "a-center"
        table = soup.find('table', {'class': 'a-center'})

        # Find all the rows in the table except the first and last ones
        rows = table.find_all('tr')[1:-1]

        # Initialize counters for total goals and total games played
        total_goals = 0
        total_games = 0

        # Loop through the rows to extract goals scored for each World Cup year
        year_goals = {}
        for row in rows:
            cols = row.find_all('td')
            year = cols[0].text.strip()
            if cols[0].find('a'):
                goals = cols[7].text.strip()
                total_goals += int(goals)
                games = cols[3].text.strip()
                total_games += int(games)
                if year not in year_goals:
                    year_goals[year] = []
                year_goals[year].append(goals)

        # Concatenate the years into a string separated by commas
        fixed_years = ','.join(year_goals.keys())

        # Concatenate the goals for each year into a string separated by commas
        fixed_goals = ','.join([','.join(year_goals[year]) for year in year_goals])

        # append the new fields to the original row
        player['DateOfBirth'] = born_date
        player['Position'] = position
        player['JerseyNumber'] = jersey_number
        # overwrite the Goals and Years fields with the new values
        player['Goals'] = year_goals
        player['Years'] = fixed_years
        player['TotalGames'] = total_games
        player['GoalsPerGame'] = round(total_goals / total_games, 2)

# # Write the updated player data back to the CSV file
# with open("../edited_cvs/worldcupgoals_1930_2022.csv", 'w', newline='',
#           encoding='ISO-8859-1') as file:
#     writer = csv.DictWriter(file, fieldnames=["Player", "Goals", "Years", "Country", "BirthPlace",
#                                               "CountryOfBirth", "Latitude", "Longitude",
#                                               "DateOfBirth", "Position", "JerseyNumber",
#                                               "TotalGames", "GoalsPerGame"])
#     writer.writeheader()
#     for player in players:
#         if player["Country"] == country:
#             print(player)
#             writer.writerow(player)

# Append the updated player data to the CSV file
with open("../edited_cvs/worldcupgoals_1930_2022.csv", 'a', newline='',
          encoding='ISO-8859-1') as file:
    writer = csv.DictWriter(file, fieldnames=["Player", "Goals", "Years", "Country", "BirthPlace",
                                              "CountryOfBirth", "Latitude", "Longitude",
                                              "DateOfBirth", "Position", "JerseyNumber",
                                              "TotalGames", "GoalsPerGame"])
    for player in players:
        if player["Country"] == country:
            try:
                writer.writerow(player)
            except:
                print(f"Unable to write player {player['Player']} to CSV file")
                with open('log.txt', 'a') as log_file:
                    log_file.write(f"{player['Player']} {player['Country']} {player['Years']}\n")
                continue


