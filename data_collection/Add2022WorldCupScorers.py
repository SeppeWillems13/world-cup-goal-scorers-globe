import csv

#Only do once now its done
# def update_player_goals(file1_path, file2_path):
#     player_goals = {}
#     with open(file1_path, 'r', encoding='ISO-8859-1') as csvfile1:
#         reader = csv.reader(csvfile1)
#         header = next(reader)  # get header row
#         for row in reader:
#             player_name = row[0]
#             goals = int(row[1])
#             player_goals[player_name] = [goals, row[2], row[3]]
#
#     with open(file2_path, 'r', encoding='ISO-8859-1') as csvfile2:
#         reader = csv.reader(csvfile2)
#         header = next(reader)  # skip header row
#         for row in reader:
#             try:
#                 if int(row[9]) > 0:
#                     player_name = row[7]
#                     if player_name in player_goals:
#                         # Update existing player
#                         goals = int(row[9])
#                         player_goals[player_name][0] += goals
#                         player_goals[player_name][1] += '-2022'
#                     else:
#                         # Add a new player
#                         player_goals[player_name] = [int(row[9]), '2022', row[0]]
#             except ValueError:
#                 continue
#
#     updated_rows = []
#     for player_name, data in player_goals.items():
#         updated_rows.append([player_name, data[0], data[1], data[2]])
#
#     # Sort by goals in descending order
#     updated_rows.sort(key=lambda x: x[1], reverse=True)
#
#     with open(file1_path, 'w', newline='', encoding='ISO-8859-1') as csvfile1:
#         writer = csv.writer(csvfile1)
#         writer.writerow(['Player', 'Goals', 'Years', 'Country'])
#         for row in updated_rows:
#             writer.writerow(row)
#
#
# update_player_goals('original_cvs/worldcupgoals.csv', 'original_cvs/FIFA WC 2022 Players Stats.csv')
