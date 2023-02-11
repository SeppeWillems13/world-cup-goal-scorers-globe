import csv
from geopy.geocoders import Nominatim

# Initialize the geolocator
geolocator = Nominatim(user_agent="myGeocoder")

# Open the input CSV file
with open('edited_cvs/worldcupgoals_1930_2022_addedCities.csv', 'r', encoding='ISO-8859-1') as input_file:
    # Create a CSV reader
    reader = csv.reader(input_file)
with open('edited_cvs/worldcupgoals_1930_2022_addedCitiesAndCountries.csv', 'w', newline='', encoding='ISO-8859-1') as output_file:
    # Create a CSV writer
    writer = csv.writer(output_file)

    # Write the header row
    writer.writerow(['Player', 'Goals', 'Years', 'Country', 'BirthPlace', 'CountryOfBirth', 'Latitude', 'Longitude'])

    # Loop through each row in the input CSV file
    for row in reader:
        # Skip the header row
        if row[0] == 'Player':
            continue
        # Get the birth place
        birth_place = row[4]
        # Get the country of birth
        country_of_birth = None
        if row[5] == '':
            location = geolocator.geocode(birth_place, language="en")
            if location is not None:
                print(location)
                country_of_birth = location.address.split(', ')[-1]
        # Update the row with the country of birth and latitude/longitude information
        row[5] = country_of_birth if country_of_birth is not None else row[5]

        # Write the row to the output CSV file
        writer.writerow(row)
