import csv
import argparse

def count_number_of_lines_with_missing_values(file_name):

  csv_filename = './' + file_name

  csv_list = []

  with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  count = 0

  for x in range(len(csv_list)):
    row = []
    for y in range(len(csv_list[0])):
      row.append(csv_list[x][y])
    if "" in row:
      count += 1

  print('Number of rows with missing values: ', count)

parser = argparse.ArgumentParser(description = 'Count the number of lines with missing data.')
parser.add_argument('-f', '--filename', help = 'Input filename.', type = str, required = True)
args = parser.parse_args()
if args:
  count_number_of_lines_with_missing_values(args.filename)