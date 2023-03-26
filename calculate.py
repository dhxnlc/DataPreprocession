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

def calculation(input, column_1, column_2, method, output):
  input_filename = './' + input

  output_filename = './output/' + output + '_' + method + '.csv'

  csv_list = []

  with open(input_filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      csv_list.append(row)

  csv_list = convert_to_numeric(csv_list)

  data_type = find_column_datatype(input_filename)

  if (data_type[column_1] == 'categorical') or (data_type[column_2] == 'categorical'):  
      print('Categorical columns cannot be calculated on.')
      return
  
  column1 = []
  column2 = []
  
  for x in range(len(csv_list)):
     if csv_list[x][csv_list[0].index(column_1)] != '':
        column1.append(csv_list[x][csv_list[0].index(column_1)])
     else:
        column1.append(0) # We're just replacing null values with 0 here.

  for x in range(len(csv_list)):
     if csv_list[x][csv_list[0].index(column_2)] != '':
        column2.append(csv_list[x][csv_list[0].index(column_2)])
     else:
        column2.append(0)

  if method == 'add':
     csv_list[0].append(column_1 + '+' + column_2)
     for x in range(1, len(csv_list)):
        csv_list[x].append(column1[x] + column2[x])

  elif method == 'sub':
     csv_list[0].append(column_1 + '-' + column_2)
     for x in range(1, len(csv_list)):
        csv_list[x].append(column1[x] - column2[x])
     
  elif method == 'mul':
     csv_list[0].append(column_1 + '*' + column_2)
     for x in range(1, len(csv_list)):
        csv_list[x].append(column1[x] * column2[x])
     
  elif method == 'div':
     csv_list[0].append(column_1 + '/' + column_2)
     for x in range(1, len(csv_list)):
        if (column1[x] == 0) or (column2[x] == 0):
           csv_list[x].append('')
        else:
            csv_list[x].append(column1[x] / column2[x])

  with open(output_filename, 'w') as f:
      #using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(csv_list)

parser = argparse.ArgumentParser(description = 'Perform calculation (add/subtract/multiply/divide) on two columns.')
parser.add_argument('-if', '--input', help = 'Input filename.', type = str, required = True)
parser.add_argument('-o', '--option', type = str, choices=['find', 'calc'], required = True, help = 
                    'find: find name and datatype (numeric/categorical) of columns, norm: perform calculation')
parser.add_argument('-c1', '--column1', type = str, required = False, help = 'Name of column 1.')
parser.add_argument('-c2', '--column2', type = str, required = False, help = 'Name of column 2.')
parser.add_argument('-m', '--method', type = str, required = False, choices = ['add', 'sub', 'mul', 'div'], help = 
                    'Calculation method.')
parser.add_argument('-of', '--output', help = 'Output filename.', type = str, required = False)
args = parser.parse_args()
if args.option == 'find':
  print(find_column_datatype(args.input))
elif args.option == 'calc':
  calculation(args.input, args.column1, args.column2, args.method, args.output)