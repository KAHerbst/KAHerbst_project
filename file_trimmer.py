import pandas as pd
import sys
f=pd.read_csv(data)
keep_col = ['State / County Name' , 'All Ages in Poverty Percent']
new_f = f[keep_col]
new_f.to_csv(trimmed, index=False)


if __name__ == '__main__':
    data = sys.argv[1]
    trimmed = sys.argv[2]
    
