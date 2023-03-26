import csv
import argparse

def delete_duplicates(file_name, output):

  csv_filename = './' + file_name

  output_filename = './output/' + output

  csv_list = []

  with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)
    
  for x in range(1,len(csv_list)):
    for y in range(x - 1):
      if csv_list[x] == csv_list[y]:
        csv_list[x] = []
      
  with open(output_filename, 'w') as f:
      # using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(csv_list)

parser = argparse.ArgumentParser(description = 'Drop duplicates.')
parser.add_argument('-i', '--input', help = 'Input filename.', type = str, required = True)
parser.add_argument('-o', '--output', help = 'Output filename.', type = str, required = True)
args = parser.parse_args()
if args:
  delete_duplicates(args.input, args.output)
