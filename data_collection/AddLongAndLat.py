import csv
import time

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

# Initialize a geolocator with a custom user agent
geolocator = Nominatim(user_agent="my-application-1")
geolocator.timeout = 10

# Open the input CSV file
with open('../edited_cvs/worldcupgoals_1930_2022_BirthPlaceAndCountries.csv', 'r',
          encoding='ISO-8859-1') as input_file:
    # Create a CSV reader
    reader = csv.reader(input_file)
    with open('../edited_cvs/worldcupgoals_1930_2022.csv', 'w', newline='',
              encoding='ISO-8859-1') as output_file:
        # Create a CSV writer
        writer = csv.writer(output_file)

        # Write the header row
        writer.writerow(
            ['Player', 'Goals', 'Years', 'Country', 'BirthPlace', 'CountryOfBirth', 'Latitude', 'Longitude'])
        # Loop through each row in the input CSV file
        for row in reader:
            # Skip the header row
            if row[0] == 'Player':
                continue
            # Get the birth place
            birthplace = row[4] + ", " + row[5]
            # Get the country of birth
            try:
                location = geolocator.geocode(birthplace)
            except GeocoderTimedOut:
                print(f"GeocoderTimedOut: {birthplace}")
                # Retry geocoding after a delay of 2 seconds
                time.sleep(2)
                location = geolocator.geocode(birthplace)

            if location:
                row[6] = str(location.latitude)
                row[7] = str(location.longitude)
            else:
                row[6] = str(0.0)
                row[7] = str(0.0)

            print(row)
            # Write the row to the output CSV file
            writer.writerow(row)
