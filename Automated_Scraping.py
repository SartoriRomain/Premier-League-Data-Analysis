#This section aims to computerize our previous scraping manipulation.

from bs4 import BeautifulSoup
import urllib3
import re
import time
from collections import defaultdict
import numpy as np
import tqdm
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import matplotlib.patches as patches


urlpage_4 = 'https://www.skysports.com/premier-league-table/2023'

# The objective of the function get_page is to extract and return HTML elements corresponding to a
# specified tag and a specific class from a given web page.

def get_page(urlpage_4,element,html_class):
    req_5 = urllib3.PoolManager()
    res_5 = req_5.request('GET', urlpage_4)
    row_html_5 = BeautifulSoup(res_5.data, 'html.parser')
    PL19 = row_html_5.find_all(element , 
    class_= html_class)
    return(PL19)

PL19= str(get_page(urlpage_4, 'tr', 'row-body'))

list_team_20 = re.findall('<span class="team-name">(.*?)</span>', str(PL19))

# Here, we parse statistics data for a particular
# team from a given HTML document (PL19). It extracts relevant information such as position, points, wins, draws, losses, 
# goals scored, and goals conceded, and returns these statistics in a dictionary format.

def extract_team_20_stats(PL19, team):
    team= team.title()
    teams = re.findall('<span class="team-name">(.*?)</span>', 
    str(PL19))
    position= (list_team_20.index(team)+1)
    start = PL19.find(team)
    end = PL19.index("</tr>", start)
    team_data_20 = PL19[start:end]
    match_played= 38
    data = [int(s) for s in re.findall(r'<td.*?>(\d+)</td>', team_data_20)]
    points= data[0]
    wins= data [1]
    drawns= data [2]
    loses =data [3]
    goals_for = data [4]
    goals_against = data [5]
    team_stats20 = {'match_played': match_played,
    'position': position,'points': points,
                    'wins': wins,'loses': loses ,
                    'drawns':  drawns,'goals_for': goals_for,
        'goals_against':goals_against
    }
    return team_stats20

team_stats_20 = {}

# Extracting the team statistics and the adding columns for the team name and the year.
for team in list_team_20:
    team_stats = extract_team_20_stats(PL19, team)
    team_stats_df = pd.DataFrame(team_stats, index=[0])
    team_stats_df['team'] = team
    team_stats_df['year'] = 2020
    team_stats_20[team] = team_stats_df



# Scrapes Premier League standings data for a given year from Sky Sports website. It extracts team statistics
# from the HTML table and organizes them into a list of dictionaries, with each dictionary representing statistics for one team.

def scrape_premier_league_standings(year):
    url = f"https://www.skysports.com/premier-league-table/{year}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}.")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='standing-table__table')
    if table is None:
        print("Failed to find the standings table.")
        return None
    
    standings_data = []
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        team_name = columns[1].text.strip()
        matches_played = int(columns[2].text.strip())
        wins = int(columns[3].text.strip())
        draws = int(columns[4].text.strip())
        losses = int(columns[5].text.strip())
        goals_for = int(columns[6].text.strip())
        goals_against = int(columns[7].text.strip())
        goal_difference = int(columns[8].text.strip())
        points = int(columns[9].text.strip())
        
        standings_data.append({
            'Team': team_name,
            'Matches Played': matches_played,
            'Wins': wins,
            'Draws': draws,
            'Losses': losses,
            'Goals For': goals_for,
            'Goals Against': goals_against,
            'Goal Difference': goal_difference,
            'Points': points
        })
    
    return standings_data

year = 2023
standings = scrape_premier_league_standings(year)
if standings:
    team_stats_20 = extract_team_20_stats(standings, year)
    print(team_stats_20)

# Now we try automating the budget scraping 
url_7 = "https://sportune.20minutes.fr/sport-business/football/les-budgets-des-clubs-de-la-premier-league-2023-2024-312241/2"

def scrape_premier_league_budgets(url):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    res = requests.get(url, headers=user_agent)
    if res.status_code != 200:
        print("Failed to retrieve data.")
        return None
    
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    contents = re.findall('<tbody>.*?\n</tbody>\n</table>', str(soup), re.DOTALL)
    
    all_headers = []
    for html_content in contents:
        html_soup = BeautifulSoup(html_content, 'html.parser')    
        headers = html_soup.find_all("th")    
        all_headers.extend(headers)
    
    Titles = [i.text for i in all_headers]
    df = pd.DataFrame(columns=Titles)
    
    all_rows = []
    for html_content in contents:
        html_soup = BeautifulSoup(html_content, 'html.parser')
        rows = html_soup.find_all("tr")
        rows_data = []
        for row in rows:
            cells = row.find_all("td")
            cell_data = [cell.get_text(strip=True) for cell in cells]
            rows_data.append(cell_data)
        all_rows.extend(rows_data)
    
    if all_rows:
        all_rows.pop(-1)
    
    df = pd.concat([df, pd.DataFrame(all_rows, columns=Titles)], ignore_index=True)
    return df


# Exemple of url that could be used.
url = "https://sportune.20minutes.fr/sport-business/football/les-budgets-des-clubs-de-la-premier-league-2023-2024-312241/2"
budgets_df = scrape_premier_league_budgets(url)
print(budgets_df)


# Cleaning the data in a merging perspective.
team_stats_20.replace({'Tottenham Hotspur': 'Tottenham',
                       'Nottingham Forest **': 'Nottingham Forest',
                       'Everton *': 'Everton',
                       'West Ham United': 'West Ham',
                       'Wolverhampton Wanderers': 'Wolverhampton',
                       'Brighton and Hove Albion': 'Brighton',
                       'Newcastle United': 'Newcastle'}, inplace=True)

# Merging.
merged_df = pd.merge(budgets_df, team_stats_20, left_on='Club', right_on='team', how='inner')

#Import using relative path.
merged_df.to_csv('merged_2.csv', index=False)

# Getting rid of position column.
merged_df.drop('position', axis=1, inplace=True)

# Replacing the M€ to six digits. 
merged_df['Budget'] = pd.to_numeric(merged_df['Budget'].str.replace('M€', '')) * 1000000
merged_df.to_csv('merged_df')
print(merged_df)




