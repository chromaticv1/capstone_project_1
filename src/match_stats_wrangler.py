import pandas as pd
from icecream import ic
from tabulate import tabulate

data = pd.read_csv('data/raw_match_stats.csv')
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
output_columns = ['opponent', 'isHome', 'venue', 'bd_captain', 'bd_won', 'abandoned',
                    #TOSS RESULT, MATCH DATE
                ]

#fix captain names
data.loc[:,'bd_captain'] = data.loc[:,'bd_captain'].str.replace('\xa0(c)', '').str.replace('†', '')
#expand other team names
data.loc[:,'opponent'] = data.loc[:,'match_title'].str.replace('BAN','').str.replace(' vs ', '').map(team_name_abbr)
#check if game is played in home
data.loc[:,'isHome'] = data.loc[:, 'venue'].str.contains("|".join(home_venues))
#check if bd won/lost/draw
data.loc[:,'bd_won'] = (data.loc[:,'summary_result'].str.contains('Bangladesh won'))
#abandon check
data.loc[:,'abandoned'] = data.loc[:,'summary_result'].str.contains('won') != True


df = data[output_columns]
df.to_csv('data/match_stats.csv')