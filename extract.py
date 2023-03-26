import csv
import argparse

def extract_columns_with_missing_values(file_name):

  csv_filename = './' + file_name

  csv_list = []

  with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  for x in range(len(csv_list[0])):
    column = []
    for y in range(len(csv_list)):
      column.append(csv_list[y][x])
    if "" in column:
      print('Column', x)

parser = argparse.ArgumentParser(description = 'Extract column with missing values.')
parser.add_argument('-f', '--filename', help = 'Input filename.', type = str, required = True)
args = parser.parse_args()
if args:
  extract_columns_with_missing_values(args.filename)