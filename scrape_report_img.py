# Importing the required modules
import requests # To get the html page from url 
import pandas as pd # To convert data into csv
from bs4 import BeautifulSoup, SoupStrainer# To extract specific data from html tags
import re # Regex
import sys # Needed to increase recursion limit
sys.setrecursionlimit(10000)

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
#states = ['FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV'

#states=['NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']#mine

# PARSE THE HTML PAGES AND SAVE DATA INTO CSV FILE 
for state in states:
    print(state)
    request = requests.get(f"https://nuforc.org/webreports/ndxl{state}.html")
    # Regex is needed to complete missing tags:
    text = request.text
    #make rows: ends in td td if no image data, if image in td yes td
    #text = re.sub('<TD></TD>','<TD></TD></TR>', text)
    #text = re.sub('<TD>Yes</TD>','<TD>Yes</TD></TR>', text)
    text = re.sub('</TD>\n', '</TD></TR>\n', text)
    #use beautiful soup to create parse tree
    soup = BeautifulSoup(text, "html.parser")
    # All data will be stored in :
    attributes = []
    data = []
    # Find specific tags with help of BeautifulSoup (here: start of table)
    t_head = soup.find("table").find("tr")
    # Save the name of the attributes 
    for e in t_head:
        try: attributes.append(e.get_text())#ignore formatting, just get name of attribute
        except: continue
    # Add an additional attribute called url
    attributes.insert(1,"Url")
    attributes.append("Report")
    # Get the data
    t_body = soup.find("table").find_all("tr")[1:]#get all lines
    print(len(t_body))
    i=0
    for row in t_body:
        sub_data = []
        # Iterate through each attribute of the row
        for col in row:
            try:
                text = col.get_text() # Get the data, e.g. the name of the city
                if(text != "\n"): sub_data.append(col.get_text().encode('latin-1').decode('windows-1252')) # Save the sub data
                # Special condition for saving the urls: 
                if col.find('a',href=True):
                    report_url=col.find('a').get('href')
                    #print(report_url)
                    sub_data.append(f"https://nuforc.org/webreports/{report_url} ")
            except: continue
        # now try to follow the link to get to the whole description and image url
        request2 = requests.get(f"https://nuforc.org/webreports/{report_url}")
        text2 = request2.text
        text2=text2.encode('latin-1').decode('windows-1252')
        start_idx=text2.find("</FONT></TD>")+108
        stop_idx=text2[start_idx:].find("</FONT></TD>")+start_idx
        report=text2[start_idx:stop_idx]
        report=re.sub("<BR>","",report)
        sub_data.append(report)
        img_soup = BeautifulSoup(text2, 'html.parser')
        img_tags = img_soup.find_all('img')
        urls = [img['src'] for img in img_tags]
        #print(urls)
        sub_data[-2]=urls #replace yes with url
        #if no image, the image column says []
        #print(report)
        #print(sub_data)
        data.append(sub_data)
        dataFrame = pd.DataFrame(data=data, columns=attributes)
        dataFrame.to_csv('data_with_report_and_img_FL_FF.csv', mode='a', encoding="utf-8", index=False)

    #print(data)
    # Storing the data into Pandas DataFrame
    dataFrame = pd.DataFrame(data = data, columns = attributes)
    #print(attributes)
    del dataFrame["Country"]  # Delete Country attribute since it always has same values
    del dataFrame["Posted"]  # Delete Posted attribute
    dataFrame.rename(columns={'Date / Time': 'Date'}, inplace=True)  # Rename first attribute
    new_columns = ["Date", "City", "State", "Latitude", "Longitude", "Shape", "Duration", "Summary", "Report", "Images", "Url"]
    dataFrame = dataFrame.reindex(
        columns=new_columns)  # Swap columns (easier to read the csv data when Url is last elem)
    # Convert Pandas DataFrame into CSV file
    dataFrame.to_csv('data_with_report_and_img_final.csv', mode='a', encoding="utf-8", index=False)

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