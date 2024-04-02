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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Trying a linear regression on the previously rumerged table.
merged_df = pd.read_csv('merged_df')
X = merged_df[['wins', 'loses', 'drawns', 'goals_for', 'goals_against', 'Budget']]

y = merged_df['points']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print("Coefficient de détermination R^2 :", score)

# Now trying a poisson distribution 
import statsmodels.api as sm

X = merged_df[['wins', 'loses', 'drawns', 'goals_for', 'goals_against', 'Budget']]
y = merged_df['points']
X = sm.add_constant(X)
poisson_model = sm.GLM(y, X, family=sm.families.Poisson())
poisson_results = poisson_model.fit()
print(poisson_results.summary())

# Counting points.
nb_matchs = 38

coefficients = poisson_results.params

predicted_points = poisson_results.predict(X)

predicted_wins_points = coefficients['wins'] * nb_matchs * 3
predicted_draws_points = coefficients['drawns'] * nb_matchs
predicted_losses_points = 0  

predicted_points += predicted_wins_points + predicted_draws_points + predicted_losses_points

predicted_points_ranking = predicted_points.sort_values(ascending=False)
print(predicted_points_ranking)

# concatenate team names for a better visualisation.
predicted_points_with_teams = pd.concat([merged_df['team'], predicted_points], axis=1)
predicted_points_with_teams.columns = ['Team', 'Predicted Points']

# Sorting by predicted points
predicted_points_ranking = predicted_points_with_teams.sort_values(by='Predicted Points', ascending=False)
predicted_points_with_teams['Predicted Points'] = predicted_points_with_teams['Predicted Points'].astype(int)

print(predicted_points_ranking)