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

def normalization(input, column_name, method, output):
  input_filename = './' + input

  output_filename = './output/' + output + '_' + method + '.csv'

  csv_list = []

  with open(input_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  csv_list = convert_to_numeric(csv_list)

  data_type = find_column_datatype(input_filename)

  if (data_type[column_name] == 'categorical'):  
      print('Categorical columns cannot be normalized.')
      return
  
  column = []
  
  for x in range(len(csv_list)):
     column.append(csv_list[x][csv_list[0].index(column_name)])

  if method == 'min-max':
     column = [i for i in column if isinstance(i,float)]
     for x in range(1, len(csv_list)):
        if csv_list[x][csv_list[0].index(column_name)] != '':
          csv_list[x][csv_list[0].index(column_name)] = (csv_list[x][csv_list[0].index(column_name)] - min(column))/(max(column)-min(column))

  elif method == 'z-score':
     column = [i for i in column if isinstance(i,float)]
     mean = sum(column) / len(column)
     variance = sum([((x - mean) ** 2) for x in column]) / len(column)
     std = variance ** 0.5
     for x in range(1, len(csv_list)):
        if csv_list[x][csv_list[0].index(column_name)] != '':
          csv_list[x][csv_list[0].index(column_name)] = (csv_list[x][csv_list[0].index(column_name)] - mean)/std
  with open(output_filename, 'w') as f:
      # using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(csv_list)

parser = argparse.ArgumentParser(description = 'Perform normalization on a column.')
parser.add_argument('-if', '--input', help = 'Input filename.', type = str, required = True)
parser.add_argument('-o', '--option', type = str, choices=['norm', 'find'], required = True, help = 
                    'find: find name and datatype (numeric/categorical) of columns, norm: perform normalization')
parser.add_argument('-c', '--column', type = str, required = False, help = 'Name of column to be filled.')
parser.add_argument('-m', '--method', type = str, required = False, choices=['min-max', 'z-score'], help = 
                    'Normalization.')
parser.add_argument('-of', '--output', help = 'Output filename.', type = str, required = False)
args = parser.parse_args()
if args.option == 'find':
  print(find_column_datatype(args.input))
elif args.option == 'norm':
  normalization(args.input, args.column, args.method, args.output)