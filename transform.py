import codecs
import csv

with codecs.open('edited_cvs/worldcupgoals_1930_2022_BirthPlace.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# Re-encode the data to ISO-8859-1
data = [[cell.encode("ISO-8859-1", errors="ignore").decode("ISO-8859-1") for cell in row] for row in data]

# Write the CSV file with ISO-8859-1 encoding
with codecs.open('edited_cvs/worldcupgoals_1930_2022_BirthPlaceTwo.csv', 'w', encoding='ISO-8859-1') as f:
    writer = csv.writer(f)
    writer.writerows(data)
