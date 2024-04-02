import re
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import lxml

pd.options.display.max_columns = None 

#starting traditional scraping protocol 
url = "https://www.skysports.com/premier-league-table/2021"
url 

user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

res=requests.get('https://www.skysports.com/premier-league-table/2021',
                headers=user_agent)

soup = BeautifulSoup(res.text, "lxml")

# printing the string of caracters of our web table
Table = soup.find('table', class_='standing-table__table')
Table


# We select headers and row names by selecting the "th" and "tr" strings
headers = Table.find_all("th")
print(headers)

Titles = []
for i in headers : 
    title = i.text
    Titles.append(title)

print(Titles)

df = pd.DataFrame(columns=Titles)
print(df)

rows = Table.find_all("tr")
rows

for i in rows[1:]:
    data = i.find_all("td")
    row = [tr.text for tr in data]
    print(row)
    l = len(df)
    df.loc[l] = row

print(df)

df.to_csv("PL2021.csv")
df.to_csv

#We now clean the datas by removing useless columns and replacing wrong team names

data2021 = pd.read_csv("PL2021.csv")
data2021

data2021 = data2021.iloc[:, 2:]
data2021

data2021 = data2021.iloc[:, :9]
data2021

data2021['Team'] = data2021['Team'].replace({'\nLiverpool\n': 'Liverpool',
                                    '\nArsenal\n': 'Arsenal',
                                     '\nManchester City\n': 'Manchester City',
                                     '\nAston Villa\n': 'Aston Villa',
                                     '\nTottenham Hotspur\n': 'Tottenham Hotspur',
                                     '\nManchester United\n': 'Manchester United',
                                     '\nWest Ham United\n': 'West Ham United',
                                     '\nNewcastle United\n': 'Newcaslte United',
                                     '\nBrighton & Hove Albion\n': 'Brighton & Hove Albion ',
                                     '\nWolverhampton Wanderers\n': 'Wolverhampton Wanderers',
                                     '\nChelsea\n': 'Chelsea',
                                     '\nFulham\n': 'Fulham',
                                     '\nBournemouth\n': 'Bournemouth',
                                     '\nCrystal Palace\n': 'Crystal Palace',
                                     '\nBrentford\n': 'Brentford',
                                     '\nNottingham Forest\n': 'Nottingham Forest',
                                     '\nLuton Town\n': 'Luton Town',
                                     '\nEverton\n': 'Everton',
                                     '\nBurnley\n': 'Burnley',
                                     '\nSheffield United\n': 'Sheffield United',
                                      '\nLeicester City\n': 'Leicester City',
                                    '\nLeeds United\n': 'Leeds United',
                                    '\nSouthampton\n':'Southampton',
                                    ' \nBrighton and Hove Albion\n' : 'Brighton and Hove Albion',
                                    '\nWest Bromwich Albion\n': 'West Bromwich Albion', '\nWatford\n' : 'Watford', 
                                    '\nNorwich City\n':'Norwich City' })
print(data2021)

data2021.to_csv('PL2021.csv')