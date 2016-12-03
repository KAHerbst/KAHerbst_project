import pandas as pd
import sys
import csv


f=pd.read_csv('poverty_data.csv')
keep_col = ['State / County Name' , 'All Ages in Poverty Percent']
new_f = f[keep_col]
new_f.to_csv('poverty_trimmed_initial.csv', index=False)
with open('poverty_trimmed.csv', 'w') as fout:
    writer = csv.writer(fout)
    with open('poverty_trimmed_initial.csv', 'r') as fin:
        reader = csv.reader(fin)
        for rownum, entry in enumerate(reader):
            if rownum<1:continue
            writer.writerow(entry)

with open('boundaries.csv' ,'r') as bounds_initial:
    with open('boundaries_trimmed.csv', 'w') as bounds:
        for row in bounds_initial:
            bounds.write(row)

poverty_dict = {}
with open('poverty_trimmed.csv','r') as trim:
    trim_read = csv.reader(trim)
    for row in trim_read:
        lst = row[0].split()
        poverty_dict[lst[0]] = row
with open('boundaries_trimmed.csv', 'r') as bounds:
    boundaries = csv.reader(bounds)
    with open('poverty_formatted.csv', 'w') as pov_final:
        writer = csv.writer(pov_final)
        for row in boundaries:
            print(row[0])
            if row[0] not in poverty_dict:
                poverty_dict[row[0]] = [row[0], '14.5']
            writer.writerow(poverty_dict[row[0]])
