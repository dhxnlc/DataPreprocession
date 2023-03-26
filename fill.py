import csv
import argparse

def convert_to_numeric(array):
    new_array = []   
    for x in range(len(array)):
        rows = []
        for y in range(len(array[0])):
            try:
                rows.append(float(array[x][y]))
            except ValueError:
                rows.append(array[x][y])
        new_array.append(rows)
    return new_array

def find_column_datatype(file_name):

    csv_filename = './' + file_name
   
    csv_list = []

    with open(csv_filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csv_list.append(row)

    csv_list = convert_to_numeric(csv_list)

    column_datatype = {}

    for x in range(len(csv_list[0])):
        column = []
        for y in range(len(csv_list)):
                column.append(csv_list[y][x])
        for item in column[1:]:
            if isinstance(item, float):
                    column_datatype.update({column[0]: 'numeric'})
            else:
                    continue
        if column[0] not in column_datatype.keys():
             column_datatype.update({column[0]: 'categorical'})
    return column_datatype
   
def fill_missing_value(file_name, column_name, method, output):
    
  csv_filename = './' + file_name

  output_filename = './output/' + output + '_' + method + '.csv'

  csv_list = []

  with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  csv_list = convert_to_numeric(csv_list)

  data_type = find_column_datatype(csv_filename)

  if (method == 'mode') and (data_type[column_name] == 'numeric'):
      print('Cannot fill by mode for numeric column.')
      return
  elif (method != 'mode') and (data_type[column_name] == 'categorical'):  
      print('Categorical columns can only be filled by mode.')
      return
  
  column = []
  
  for x in range(len(csv_list)):
     column.append(csv_list[x][csv_list[0].index(column_name)])

  if method == 'mean':
     column = [i for i in column if isinstance(i,float)]
     mean = sum(column[1:])/len(column[1:])
     for x in range(len(csv_list)):
        if csv_list[x][csv_list[0].index(column_name)] == '':
          csv_list[x][csv_list[0].index(column_name)] = mean

  elif method == 'median':
     column = [i for i in column if isinstance(i,float)]
     column.sort()
     mid = len(column) // 2
     median = (column[mid] + column[~mid]) / 2
     for x in range(len(csv_list)):
        if csv_list[x][csv_list[0].index(column_name)] == '':
          csv_list[x][csv_list[0].index(column_name)] = median

  elif method == 'mode':
     column = [i for i in column if i != '']
     mode = (max(set(column), key = column.count))
     for x in range(len(csv_list)):
        if csv_list[x][csv_list[0].index(column_name)] == '':
          csv_list[x][csv_list[0].index(column_name)] = mode

  with open(output_filename, 'w') as f:
      # using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(csv_list)

parser = argparse.ArgumentParser(description = 'Fill missing values in column using mean, median or mode.')
parser.add_argument('-if', '--input', help = 'Input filename.', type = str, required = True)
parser.add_argument('-o', '--option', type = str, choices=['fill', 'find'], required = True, help = 
                    'find: find name and datatype (numeric/categorical) of columns, fill: fill missing value')
parser.add_argument('-c', '--column', type = str, required = False, help = 'Name of column to be filled.')
parser.add_argument('-m', '--method', type = str, required = False, choices=['mean', 'median', 'mode'], help = 
                    'Method to fill column with.')
parser.add_argument('-of', '--output', help = 'Output filename.', type = str, required = False)
args = parser.parse_args()
if args.option == 'find':
  print(find_column_datatype(args.input))
elif args.option == 'fill':
  fill_missing_value(args.input, args.column, args.method, args.output)