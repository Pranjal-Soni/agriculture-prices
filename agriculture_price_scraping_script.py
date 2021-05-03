import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import timedelta, date



def daterange(date1, date2):
    """Generate dates between two dates"""
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


date_list = []
start_date = date(2020, 1, 1) 
end_date = date(2020, 12, 31)


for dt in daterange(start_date, end_date):
    date_list.append(str(dt.strftime("%d-%b-%Y")))
    
#generate the dataframe
df = pd.DataFrame()
for date in tqdm(date_list):
    res = requests.get("https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=24&Tx_State=UP&Tx_District=1&Tx_Market=0&DateFrom="+date+"&DateTo="+date+"&Fr_Date="+date+"&To_Date="+date+"&Tx_Trend=0&Tx_CommodityHead=Potato&Tx_StateHead=Uttar+Pradesh&Tx_DistrictHead=Agra&Tx_MarketHead=--Select--")
    soup = BeautifulSoup(res.content,"lxml")
    table_df = pd.read_html(str(soup.find("table")))
    df = pd.concat([df,pd.DataFrame(table_df[0])])
    
#droping extra columns and null rows
df = df.drop(["State Name","Group","Min Price (Rs/Quintal)","Max Price (Rs/Quintal)","Modal Price (Rs/Quintal)"],axis=1)
df = df.dropna().reset_index(drop=True)

#saving the dataframe
df.to_excel("patato_prices.xlsx",index = False)