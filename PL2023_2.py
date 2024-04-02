import re
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import lxml

#Classic scraping, calling the strings from the website 
pd.options.display.max_columns = None 

url = "https://footystats.org/england/premier-league#"
url 

user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

res =requests.get('https://footystats.org/england/premier-league#',
                headers=user_agent)

content = requests.get(url).text

soup = BeautifulSoup(res.text, "lxml")
str(soup)[:200000]

Table = soup.find("table", class_ = "full-league-table table-sort col-sm-12 mobify-table")
Table

#setting up columns and rows.
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

df.to_csv("2023_2024.csv")
df.to_csv

Data2023bis = pd.read_csv("2023_2024.csv")
Data2023bis

#getting rid of the columns that are also in the other 2023 dataset
columns_to_drop = ['WWin', 'DDraw', 'LLoss', 'GFGoals For (GF).The number of goals thisteam have scored.', 'GAGoals Against (GA).The number of goals thisteam have conceded.', 'GDGoal Difference (GD).Goals Scored - Goals Conceded', 'Pts', 'Last 5', 'Yellow Card / Red Card', 'Corners / match'] 
Data2023bis = df.drop(columns_to_drop, axis=1)
Data2023bis

#Changing row name for the sake of merging 
Data2023bis['Team'] = Data2023bis['Team'].replace({'Liverpool FC': 'Liverpool',
                                    'Arsenal FC': 'Arsenal',
                                     'Manchester City FC': 'Manchester City',
                                     'Aston Villa FC': 'Aston Villa',
                                     'Tottenham Hotspur FC': 'Tottenham Hotspur',
                                     'Manchester United FC': 'Manchester United',
                                     'West Ham United FC': 'West Ham United',
                                     'Newcastle United FC': 'Newcaslte United',
                                     'Brighton & Hove Albion FC': 'Brighton & Hove Albion ',
                                     'Wolverhampton Wanderers FC': 'Wolverhampton Wanderers',
                                     'Chelsea FC': 'Chelsea',
                                     'Fulham FC': 'Fulham',
                                     'AFC Bournemouth': 'Bournemouth',
                                     'Crystal Palace FC': 'Crystal Palace',
                                     'Brentford FC': 'Brentford',
                                     'Nottingham Forest FC': 'Nottingham Forest',
                                     'Luton Town FC': 'Luton Town',
                                     'Everton FC': 'Everton',
                                     'Burnley FC': 'Burnley',
                                     'Sheffield United FC': 'Sheffield United'})
print(Data2023bis)

Data2023bis.to_csv('PL2023Bonus.csv')

FinalData = pd.read_csv('PL2023Bonus.csv')
FinalData



