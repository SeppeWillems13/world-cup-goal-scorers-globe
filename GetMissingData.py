import csv

player_goals = []
with open('edited_cvs/worldcupgoals_1930_2022_BirthPlaceAndCountries.csv', 'r', encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # skip header row
    for row in reader:
        if row[2] == '0' or row[4] == 'SEARCH MANUALLY' or row[5] == '':
            player_goals.append(row)
        if row[3] != row[5]:
            player_goals.append(row)

# print the rows where Years is 0
for player in player_goals:
    print(player)
