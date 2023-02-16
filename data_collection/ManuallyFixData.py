import csv
import requests
from bs4 import BeautifulSoup

# define the URL template
url_template = 'https://www.thesoccerworldcups.com/players/{}.php'

# prompt user for the country name
country = input("Enter the country name: ")

# read the CSV file and filter rows based on the country
with open('../edited_cvs/worldcupgoals_1930_2022.csv', 'r') as file:
    reader = csv.DictReader(file)
    filtered_rows = [row for row in reader if row['Country'].lower() == country.lower()]

# process each player in the filtered rows
for row in filtered_rows:
    # convert the player's name to lowercase and replace spaces with underscores
    player_name = row['Player'].lower().replace(' ', '_')

    # generate the player's URL and send a GET request
    url = url_template.format(player_name)
    response = requests.get(url)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract player information
    player_info = soup.find('div', class_='margen-y15 clearfix margen-t0')

    # extract name, born date, position, jersey number, and height
    if player_info is None:
        print(f"Unable to find player info for {row['Player']}")
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{row['Player']} - {url}")
        continue
    name = player_info.find('h2', class_='t-enc-1 margen-t0').text
    born_date = player_info.find('td', string='Born Date:').find_next_sibling('td').text
    position = player_info.find('td', string='Position:').find_next_sibling('td').text
    jersey_number_elem = player_info.find('td', string='Jersey Number:').find_next_sibling('td')
    jersey_number = ','.join([num.strip() for num in jersey_number_elem.text.split(',')]) if jersey_number_elem else ''

    # print the information
    print(f"Name: {name}")
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
    for row in rows:
        cols = row.find_all('td')
        year = cols[0].text.strip()
        if cols[0].find('a'):
            goals = cols[7].text.strip()
            total_goals += int(goals)
            games = cols[3].text.strip()
            total_games += int(games)
            print(f'{year}: {goals} goals')
    # Print the total goals and total games played for the Algerian national team
    print(f'Wikipedia link: https://www.wikiwand.com/en/{player_name}')
    print(f'Total games played: {total_games}')
    print(f'Total goals scored: {total_goals}')


