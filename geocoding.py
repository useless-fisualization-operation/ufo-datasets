'''
    Inspired by Abdishakur's tutorial:
    https://towardsdatascience.com/geocode-with-python-161ec1e62b89
    Note! Still need to comment on the code.
'''
# Importing the required modules
import pandas as pd # To convert data into csv
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv("Data2.csv")
locator = Nominatim(user_agent="hope")

# Example:
#location = locator.geocode("Hoover, AL, USA")
#print(f"Test = {location}")

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=0.2)

len = len(df.index) # number of rows in csv
checking = False
miss = 0
n = 0
for index, row in df.iterrows():
    if row['Latitude'] != row['Latitude']: # check if nan
        if n>30:
            if miss/n > 0.33: 
                print("---- Too many missed requests. Shutting down program. ---- ")
                break # end program if 30% misses
            else:
                print("---- Number of missed requests acceptable. Continuing... ---- ") 
                checking = False
                n = 0
                miss = 0
        if checking: n += 1
        try: 
            loc = locator.geocode(row['City']+", "+row['State'] + ", USA")
            df.at[index, 'Latitude'] = loc.latitude
            df.at[index, 'Longitude'] = loc.longitude
            print(f"{index}/{len}",u'\u2713')
        except Exception as exception: 
            print(f"{index}/{len}",u'\u2717',"Error! Waiting 2 seconds...")
            if not checking: 
                print("---- Checking ratio of missed requests (30 tries) ---- ")
                checking = True
            miss += 1
            time.sleep(2)

df.to_csv('Data2.csv', encoding="utf-8", index=False)