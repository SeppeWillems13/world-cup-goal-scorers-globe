import csv
import random
from collections import defaultdict

# Read in the CSV file and extract the latitude and longitude data
with open('../edited_cvs/worldcupgoals_1930_2022.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

# Create a dictionary to group players by birthplace
groups = defaultdict(list)
for row in data:
    groups[row['BirthPlace']].append(row)

# Iterate over each group of players with the same birthplace
with open('../edited_cvs/worldcupgoals_1930_2022.csv', mode='w', newline='') as outfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for group in groups.values():
        # Check if there are multiple players in the group
        if len(group) > 1:
            # Generate a random offset for each player in the group
            offsets = [(random.uniform(-0.015, 0.015), random.uniform(-0.015, 0.015)) for _ in range(len(group))]
            # Apply the offset to each player's latitude and longitude
            for row, (offset_lat, offset_lon) in zip(group, offsets):
                row['Latitude'] = str(float(row['Latitude']) + offset_lat)
                row['Longitude'] = str(float(row['Longitude']) + offset_lon)
                writer.writerow(row)
        else:
            # If there's only one player in the group, write their original row
            writer.writerow(group[0])
