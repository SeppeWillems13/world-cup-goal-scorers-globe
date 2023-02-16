import csv

# Open the CSV file and read in the data
with open('../edited_cvs/worldcupgoals_1930_2022.csv', 'r') as file:
    reader = csv.reader(file)

    # Skip the first row (header)
    next(reader)

    # Sort the remaining rows based on the number of goals and the country/player names
    sorted_rows = sorted(reader, key=lambda row: (row[3], row[0]))

# Open the output CSV file and write the sorted data
with open('../edited_cvs/worldcupgoals_1930_2022.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)

    # Write the header row
    writer.writerow(['Player', 'Goals', 'Years', 'Country', 'BirthPlace', 'CountryOfBirth', 'Latitude', 'Longitude'])

    # Write the sorted rows
    for row in sorted_rows:
        writer.writerow(row)
