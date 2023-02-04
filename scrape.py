# Importing the required modules
import requests # To get the html page from url 
import pandas as pd # To convert data into csv
from bs4 import BeautifulSoup # To extract specific data from html tags
import re # Regex
import sys # Needed to increase recursion limit
sys.setrecursionlimit(10000)

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

# PARSE THE HTML PAGES AND SAVE DATA INTO CSV FILE 
for state in states:
    request = requests.get(f"https://nuforc.org/webreports/ndxl{state}.html")
    # Regex is needed to complete missing tags:
    text = request.text
    text = re.sub('<TD></TD>','<TD></TD></TR>', text)
    text = re.sub('<TD>Yes</TD>','<TD>Yes</TD></TR>', text)
    soup = BeautifulSoup(text, "html.parser")
    # All data will be stored in :
    attributes = []
    data = []
    # Find specific tags with help of BeautifulSoup
    t_head = soup.find("table").find("tr")
    # Save the name of the attributes 
    for e in t_head:
        try: attributes.append(e.get_text())
        except: continue
    # Add an additional attribute called url
    attributes.insert(1,"url")
    # Get the data
    t_body = soup.find("table").find_all("tr")[1:]
    for row in t_body:
        sub_data = []
        # Iterate through each attribute of the row
        for col in row:
            try:
                text = col.get_text() # Get the data, e.g. the name of the city 
                if(text != "\n"): sub_data.append(col.get_text()) # Save the sub data
                # Special condition for saving the urls: 
                if col.find('a',href=True): sub_data.append(f"https://nuforc.org/webreports/{col.find('a').get('href')} ")
            except: continue
        data.append(sub_data)
    
    # Storing the data into Pandas DataFrame
    dataFrame = pd.DataFrame(data = data, columns = attributes)
    # Converting Pandas DataFrame into CSV file
    dataFrame.to_csv('Data.csv', mode='a', encoding="utf-8", index=False)

'''
# OLD CODE:
for state in states:
    request = requests.get(f"https://nuforc.org/webreports/ndxl{state}.html")
    # Regex is needed to complete missing tags:
    text = request.text
    text = re.sub('<TD></TD>','<TD></TD></TR>', text)
    text = re.sub('<TD>Yes</TD>','<TD>Yes</TD></TR>', text)
    # Save html in Pages folder
    with open(f"Pages/{state}.html", "w") as f:
        f.write(text)
'''