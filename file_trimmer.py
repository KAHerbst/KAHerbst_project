import pandas as pd
import sys
#Does the intial trimming of removing the rows I do not want to use
f=pd.read_csv(data)
keep_col = ['State / County Name' , 'All Ages in Poverty Percent']
new_f = f[keep_col]
new_f.to_csv(trimmed, index=False)
#Now I have to figure out reformat the county and state data

if __name__ == '__main__':
    data = sys.argv[1]
    trimmed = sys.argv[2]
    
