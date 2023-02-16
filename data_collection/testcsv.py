import csv

with open('updated_players.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        player = row['Player']
        years = row['Years'].split(',')
        goals = row['Goals'].split(',')
        for i in range(len(years)):
            year = years[i]
            goal = goals[i]
            print(f"{player} scored {goal} goals in {year}")
