'''
Purpose: 

Fast way to add images (and summary if chosen) 
to the already existing ufo dataset. Based on 
Annika's ufo_scrape_report.py 

- Jonathan Gustaf Cilli
'''
# Importing the required modules
import requests # To get the html page from url 
import pandas as pd # To convert data into csv
from bs4 import BeautifulSoup, SoupStrainer# To extract specific data from html tags
import re # Regex
import sys # Needed to increase recursion limit
from concurrent.futures import ThreadPoolExecutor
sys.setrecursionlimit(10000)

df = pd.read_csv("Data.csv")

''' Not currently used:'''
def addImageAndSummary(i):
    request = requests.get(df['Url'][i])
    # Add entire summary - Annika:
    text2= request.text
    text2=text2.encode('latin-1').decode('windows-1252')
    start_idx=text2.find("</FONT></TD>")+108
    stop_idx=text2[start_idx:].find("</FONT></TD>")+start_idx
    report=text2[start_idx:stop_idx]
    report=re.sub("<BR>","",report)
    report=re.sub("\n"," ",report)
    df.at[i, 'Summary'] = report
    # Add image - Annika:
    if df['Images'][i] == "Yes":
        print(f"Request {i}: {request.status_code}")
        if(request.status_code == 503): print(f"Error at {i}. DOING TOO MUCH WORK")
        request = requests.get(df['Url'][i])
        soup = BeautifulSoup(request.text, "html.parser")
        img = soup.find('img')
        df.at[i, 'UrlImage'] = img['src']
    df.at[i, 'Url'] = ""

def addJustImage(i):
    # Add image - Annika:
    if df['Images'][i] == "Yes":
        request = requests.get(df['Url'][i])
        print(f"Request {i}: {request.status_code}")
        if(request.status_code == 503): print(f"Error at {i}. DOING TOO MUCH WORK")
        request = requests.get(df['Url'][i])
        soup = BeautifulSoup(request.text, "html.parser")
        img = soup.find('img')
        df.at[i, 'UrlImage'] = img['src']

pool = ThreadPoolExecutor(3) # the server can't seem to handle more than 3
len = len(df.index) # number of rows in csv

for i in range(len):
    try: pool.submit(addJustImage, i)
    except KeyboardInterrupt: sys.exit()
    except Exception as e: print(f"Error at {i}: {e.__class__.__name__}")

pool.shutdown()

df.to_csv('UfoDataWithImages.csv', index=False)