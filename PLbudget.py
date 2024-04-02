import pandas as pd
from bs4 import BeautifulSoup 
import re
import requests
import lxml

#Classic processes of scraping, calling the website strings.
user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
url = "https://sportune.20minutes.fr/sport-business/football/les-budgets-des-clubs-de-la-premier-league-2023-2024-312241/2"
url 

res=requests.get("https://sportune.20minutes.fr/sport-business/football/les-budgets-des-clubs-de-la-premier-league-2023-2024-312241/2",
                headers=user_agent)

content = requests.get(url).text

soup = BeautifulSoup(res.text, "lxml")
str(soup)[:200000]

contents = re.findall('<tbody>.*?\n</tbody>\n</table>',str(soup), re.DOTALL)
contents

#Forming the tables with rows and columns.
all_headers = []

for html_content in contents:
    html_soup = BeautifulSoup(html_content, 'html.parser')    
    headers = html_soup.find_all("th")    
    all_headers.extend(headers)

print(all_headers)


Titles = []
for i in headers : 
    title = i.text
    Titles.append(title)

print(Titles)

df = pd.DataFrame(columns=Titles)
print(df)

#selecting certain strings "td" expressing the rows in the html code.
df = all_rows = []
for html_content in contents:
    html_soup = BeautifulSoup(html_content, 'html.parser')
    rows = html_soup.find_all("tr")
    rows_data = []
    for row in rows:
        cells = row.find_all("td")
        cell_data = [cell.get_text(strip=True) for cell in cells]
        rows_data.append(cell_data)
    all_rows.extend(rows_data)
    

print(all_rows) 

if all_rows:
    all_rows.pop(-1)

print(all_rows)

df = pd.DataFrame(columns=Titles)

df = pd.concat([df, pd.DataFrame(all_rows, columns=Titles)], ignore_index=True)

print(df)

df.to_csv('Budget2023.csv')

Budget2023 = pd.read_csv('Budget2023.csv')
Budget2023

#Replacing the xxxM€ to 9 digit in case the code could be used in the future. 

df['Budget'] = df['Budget'].replace({'800 M€': '800 000 000',
                                    '720 M€': '720 000 000',
                                     '690 M€': '690 000 000',
                                     '600 M€': '600 000 000',
                                     '550 M€': '550 000 000',
                                     '525 M€': '525 000 000',
                                     '305 M€': '305 000 000',
                                     '290 M€': '290 000 000',
                                     '230 M€': '230 000 000',
                                     '220 M€': '220 000 000',
                                     '200 M€': '200 000 000',
                                     '200 M€': '200 000 000',
                                     '185 M€': '185 000 000',
                                     '175 M€': '175 000 000',
                                     '160 M€': '165 000 000',
                                     '155 M€': '155 000 000',
                                     '145 M€': '145 000 000',
                                     '125 M€': '125 000 000',
                                     '121 M€': '121 000 000',
                                     '120 M€': '120 000 000',
                                     '90 M€': '90 000 000'})

print(df)

df.to_csv('Budget2023.csv')