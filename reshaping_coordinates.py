import pandas as pd
import csv
import numpy as np


data=pd.read_csv('air_force_stations.csv')
data_np=data.to_numpy()

with open('airforce_reshaped.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Location", "State", "lat", "long", "command", "host wing", "primary missions and units"])#header
    i=0
    for nw in data['coordinates']:
        north=nw[0:nw.find('N')]
        north=north.replace("°",".").replace("′","").replace("″","")
        print(north)
        west=nw[nw.find('N')+2:nw.find('W')]
        west="-"+west.replace("°", ".").replace("′", "").replace("″", "")
        print(west)
        row=np.append(data_np[i,0:3], np.append([north,west],data_np[i,4:]))
        print(row)
        writer.writerow(row)
        i+=1

