import csv

# open input and output CSV files
with open('../edited_cvs/worldcupgoals_1930_2022.csv', newline='') as input_file, open('../edited_cvs/worldcupgoals_1930_2022.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # read the header row
    header = next(reader)
    header.append("TotalGoalsScored")  # add new column header
    writer.writerow(header)  # write the modified header row to the output file

    # iterate over the remaining rows
    for row in reader:
        total_games = int(row[11])
        goals_per_game = float(row[12])
        total_goals_scored = int(total_games * goals_per_game)  # calculate total goals scored
        row.append(total_goals_scored)  # add total goals scored to the row
        writer.writerow(row)  # write the modified row to the output file
