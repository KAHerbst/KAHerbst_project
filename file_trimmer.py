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
            if rownum<4:continue
            writer.writerow(entry)
