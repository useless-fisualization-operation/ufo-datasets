# Importing the required modules
import pandas as pd # To convert data into csv
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv("Data2.csv") # load csv in dataframe
locator = Nominatim(user_agent="hope") 
geocode = RateLimiter(locator.geocode, min_delay_seconds=1) # add delay to geocoding calls
del df["Posted"] # Delete Country attribute since it always has same values

df.to_csv('Data2.csv', encoding="utf-8", index=False) # save datafram to csv