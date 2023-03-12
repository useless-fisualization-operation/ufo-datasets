'''
Purpose: 

Splits the ufo datasets into 3 separete csv files
with IDs and reference IDs.  

- Jonathan Gustaf Cilli
'''
# Importing the required modules
import pandas as pd # To convert data into csv
import sys # Needed to increase recursion limit
from concurrent.futures import ThreadPoolExecutor
sys.setrecursionlimit(10000)

df = pd.read_csv("../DataSets/UfoEntireData.csv")
lent = len(df.index) # number of rows in csv

df['Madar'] = ''
df['Hoax'] = ''
for i in range(lent):
    try:
        if "hoax" in df['Summary'][i].lower():
            df.at[i,'Hoax'] = 'Yes'
        if "madar" in df['Summary'][i].lower():
            df.at[i,'Madar'] = 'Yes'
    except: print(f"Error at: {i}")
df.to_csv('../DataSets/UfoEntireData2.csv', index=False)
