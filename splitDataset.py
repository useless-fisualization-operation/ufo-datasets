# Importing the required modules
import pandas as pd # To convert data into csv
import sys # Needed to increase recursion limit
from concurrent.futures import ThreadPoolExecutor
sys.setrecursionlimit(10000)

df = pd.read_csv("Data.csv")
lent = len(df.index) # number of rows in csv
data = []
data2 = [['none',0]]

df['ID_REF_LOC'] = 0
df['ID_REF_SHAPE'] = 0
last_state = df['State'][0]
start = 0
for i in range(lent):
    if last_state != df['State'][i]: start = len(data)
    last_state =  df['State'][i]
    found_same_city = False
    id_loc = i
    for j in range(start, len(data)):
        if df['City'][i] == data[j][0]: 
            found_same_city = True
            data[j][4] = data[j][4] + 1 
            id_loc = j
            break
    if not found_same_city: data.append([df['City'][i],df['State'][i],df['Latitude'][i],df['Longitude'][i],1])
    df.at[i,'ID_REF_LOC'] = int(id_loc)

    id_shape = i
    found_same_shape = False
    #print(f"{i}: {df['Shape'][i]}")
    if df['Shape'][i] != df['Shape'][i]: 
        found_same_shape = True
        data2[0][1] = data2[0][1] + 1 
        id_shape = j
    else:
        for j in range(len(data2)):
            if df['Shape'][i].capitalize() == data2[j][0]: 
                found_same_shape = True
                data2[j][1] = data2[j][1] + 1 
                id_shape = j
                break
    if not found_same_shape: data2.append([df['Shape'][i].capitalize(), 1])
    df.at[i,'ID_REF_SHAPE'] = int(id_shape)
    if i%1000==0: print(f'Done {i}',u'\u2713')

df2 = pd.DataFrame(data, columns=['City', 'State', 'Latitude', 'Longitude','Tot'])
df2.to_csv('Data3.csv')
df3 = pd.DataFrame(data2, columns=['Shape','Tot'])
df3.to_csv('Data5.csv')

#df.drop('City','State','Latitude','Longitude', inplace=True)
del df['City']
del df['State']
del df['Latitude']
del df['Longitude']
del df['Shape']
new_col = ["ID_REF_LOC","ID_REF_SHAPE","Date","Duration","Images","Url","UrlImage","Summary"]
df = df.reindex(columns=new_col) # Swap columns (easier to read the csv data when Url is last elem)
    
df.to_csv('Data4.csv', index=False)
