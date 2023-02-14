# Importing the required modules
import pandas as pd # To convert data into csv
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv("Data.csv") # load csv in dataframe
locator = Nominatim(user_agent="hope") 
geocode = RateLimiter(locator.geocode, min_delay_seconds=0.2) # add delay to geocoding calls

# ---------------------------------------------------------------------------------------
# Example of how the geocode works. Replace "Washington, PA, USA" with desired value. 
'''
location = locator.geocode("Washington, PA, USA")
print(f"Location = {location}")
print(f"Latitude: {location.latitude} Longitude: {location.longitude}")
'''
# ---------------------------------------------------------------------------------------

def add_coordinates(k,loc):
    df.at[k, 'Latitude'] = loc.latitude # update Latitude value
    df.at[k, 'Longitude'] = loc.longitude # update Longitude value

len = len(df.index) # number of rows in csv
count = 0 # counter of visited rows
'''
Time complexity O(n^2). Could probably be improved!
--- Pseudocode ---
Iterate through rows of dataframe (usually not reccomended to use the following approach):
    If row has no coordinates: 
        Send request to Nominatim and update the Latitude and Longitude values based on the city and state name
        Check for similar places in the remaining rows and update them accordingly  
'''
for i in range(len):
    if df['Latitude'][i] != df['Latitude'][i]: # not equal itself = nan (value yet not checked)
        print(f"Index: {i}, Count: {count}/{len}", end=" ")
        count += 1
        try: # try to request cooordinates from Nominatim
            loc = locator.geocode(df['City'][i]+", "+df['State'][i] + ", USA")
            add_coordinates(i, loc)
            print(u'\u2713') # print check mark
            # Check for similar places:
            for j in range(i+1, len): 
                if df['State'][j] != df['State'][i]: break 
                if df['City'][j] == df['City'][i]: 
                    count += 1
                    add_coordinates(j, loc)
        except Exception as exception: # Error during request
            print(u'\u2717', 'Error!') # print cross mark
            #time.sleep(2) # wait if Nominatim is angry at the frequency of requests

df.to_csv('Data.csv', encoding="utf-8", index=False) # Dataframe to csv