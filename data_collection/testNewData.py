import csv

with open('../edited_cvs/worldcupgoals_1930_2022.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        print(row[6])
        print(row[7])
