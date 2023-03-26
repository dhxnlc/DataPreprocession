import csv
import argparse

def delete_columns_with_missing_values(file_name, threshold, output):

  csv_filename = './' + file_name

  output_filename = './output/' + output

  csv_list = []

  with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  null_percentage_list = []

  for x in range(len(csv_list[0])):
    column = []
    for y in range(len(csv_list)):
      column.append(csv_list[y][x])
    null_percentage = round((float(column.count('')/len(column))),2)
    null_percentage_list.append(null_percentage)
 
  for item in null_percentage_list:
    if item > threshold:
      #print(null_percentage_list.index(item))
      for x in range(len(csv_list)):
        csv_list[x][null_percentage_list.index(item)] = 'delete'

  for x in range(len(csv_list)):
    csv_list[x] = [i for i in csv_list[x] if i != 'delete']
      
  with open(output_filename, 'w') as f:
      # using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(csv_list)

parser = argparse.ArgumentParser(description = 'Delete columns with percentage of missing values over a certain threshold.')
parser.add_argument('-i', '--input', help = 'Input filename.', type = str, required = True)
parser.add_argument('-t', '--threshold', type = float, required = True, help = 'Define a threshold.')
parser.add_argument('-o', '--output', help = 'Output filename.', type = str, required = True)
args = parser.parse_args()
if args:
  delete_columns_with_missing_values(args.input, args.threshold, args.output)