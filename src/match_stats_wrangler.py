import pandas as pd
from datetime import datetime
from src.utils import *
from icecream import ic
from tabulate import tabulate
import os

data = pd.read_csv('data/raw_tables/raw_match_stats.csv')
team_name_abbr = {
    'BD': 'Bangladesh',
    'WI': 'West Indies',
    'NZ': 'New Zealand',
    'ZIM': 'Zimbabwe',
    'AFG': 'Afghanistan',
    'SA': 'South Africa',
    'IND': 'India',
    'ENG': 'England',
    'IRE': 'Ireland',
    'PAK': 'Pakistan',
    'NED': 'Netherlands',
    'AUS': 'Australia'
}
home_venues = [
    "Mirpur",
    "Chattogram",
    "Sylhet"
]
output_columns = ['opponent', 'is_home', 'venue', 'bd_captain', 'bd_won', 'abandoned', 'bd_won_toss', 'bd_bat_first', 'player_of_the_match', 'bd_won_series',
                    'date'
                ]

# fix captain names
data.loc[:,'bd_captain'] = data.loc[:,'bd_captain'].str.replace('\xa0(c)', '').str.replace('†', '')
# expand other team names
data.loc[:,'opponent'] = data.loc[:,'match_title'].str.replace('BAN','').str.replace(' vs ', '').map(team_name_abbr)
# check if game is played in home
data.loc[:,'is_home'] = data.loc[:,'venue'].str.contains("|".join(home_venues))
# check if bd won/lost/draw
data.loc[:,'bd_won'] = (data.loc[:,'summary_result'].str.contains('Bangladesh won'))
# abandon check
data.loc[:,'abandoned'] = data.loc[:,'summary_result'].str.contains('won') != True
# from raw nested tables
for i in (range(data.shape[0])):
    details_df = collect_df('details', i)
    if details_df is None:
        continue
    # Toss result, bat fist
    toss_result = details_df['Toss'].item()
    bd_won_toss = 'Bangladesh' in toss_result
    data.loc[i,'bd_won_toss'] = bd_won_toss
    bd_bat_first = (bd_won_toss and 'bat' in toss_result) or (not bd_won_toss and 'field' in toss_result)

    data.loc[i, 'bd_bat_first'] = bd_bat_first
    #Player of the match
    data.loc[i, 'player_of_the_match'] = details_df['Player Of The Match'].item()
    #BD won series
    if 'Series result' in details_df.columns:
        data.loc[i, 'bd_won_series'] = 'Bangladesh' in details_df['Series result'].item()
    #time
    date_str = (details_df['Match days'].item().split(' - ')[0])
    date = datetime.strptime(date_str, "%d %B %Y")
    data.loc[i, 'date'] = date

    #ic (details_df.columns)



df = data[output_columns]
df.to_csv('data/match_stats.csv')