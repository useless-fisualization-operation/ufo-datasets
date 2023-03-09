'''
Purpose: 

Remove entries without coordinates from the 
UFO dataset.

- Jonathan Gustaf Cilli
'''
# Importing the required modules
import pandas as pd # To convert data into csv
from bs4 import BeautifulSoup, SoupStrainer# To extract specific data from html tags
import sys # Needed to increase recursion limit


df = pd.read_csv("UfoDataWithImages.csv")
df = df[df['Longitude'].notna()]

df.to_csv('UfoDataWithImagesCleaned.csv', index=False)