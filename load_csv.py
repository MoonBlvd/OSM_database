import csv
import numpy as np
def run(data_name):
    i = 0
    data_dict = {}
    with open(data_name, 'r') as file:
        tmp = csv.reader(file, delimiter = ',')
        for line in tmp:
            if i == 0:
                fields = line
                for field in fields:
                    data_dict[field] = []
            elif line != []:
                for j, data in enumerate(line):
                    data_dict[fields[j]].append(data)
            i += 1
    return data_dict
