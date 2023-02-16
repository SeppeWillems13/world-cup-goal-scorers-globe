import csv

with open('../edited_cvs/worldcupgoals_1930_2022.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row['BirthPlace']:
            print(f"{row['Player']}-{row['Years']}-{row['Country']}")
