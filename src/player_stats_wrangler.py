import pandas as pd
import os
from src.utils import *
from icecream import ic

batting_path = 'data/raw_tables/batting/'
bowling_path = 'data/raw_tables/bowling/'
match_stats = pd.read_csv('data/match_stats.csv', index_col=0)
batting_player_records = {}
bowling_player_records = {}
for match in (os.listdir(batting_path)):
    i = int((match).replace('.csv', ''))
    batting_df = collect_df('batting', i)
    bowling_df = collect_df('bowling', i)
    details_df = collect_df('details', i)

    #fix names:
    batting_df.loc[:,'Batting'] = (batting_df.loc[:,'Batting']
    .str.replace('(c)','', regex=False)
    .str.replace('†', '', regex=False)
    .str.strip())
    bowling_df.loc[:,'Bowling'] = (bowling_df.loc[:,'Bowling']
    .str.replace('(c)','', regex=False)
    .str.replace('†', '', regex=False)
    .str.strip())
    
    #Player batting stats:
    total = str(batting_df.loc[batting_df.shape[0]-1,'R'])
    if '/' in total: total_runs = total.split('/')[0]
    total_runs = int(total) if '/' not in total else int(total.split('/')[0])
    wickets_yeeted = 10 if '/' not in total else int(total.split('/')[1])
    batting_players = (batting_df.loc[0:batting_df.shape[0]-3, 'Batting'].tolist())
    for  p in (batting_players):
        if p not in batting_player_records: batting_player_records[p] = []
        a = batting_df[batting_df['Batting'] == p]
        a_cols = a.columns.tolist()
        a_values = a.squeeze().tolist()
        b = match_stats.loc[i]
        b_cols = b.index.tolist()
        b_values = b.squeeze().tolist()
        # print(
        #     f"""
        #     {a_cols = }
        #     {b_cols = }
        #     {a_values = }
        #     {b_values = }
        #     """
        # )
        record = pd.Series(a_values+b_values+[total_runs], index = a_cols+b_cols+['total_runs'])
        batting_player_records[p].append(record)
    bowling_players = (bowling_df.loc[:, 'Bowling'].tolist())
    for p in bowling_players:
        if p not in bowling_player_records: bowling_player_records[p] = []
        a = bowling_df[bowling_df['Bowling'] == p]
        a_cols = a.columns.tolist()
        a_values = a.squeeze().tolist()
        record = pd.Series(a_values+b_values, index = a_cols+b_cols)
        bowling_player_records[p].append(record)

if 'json' not in os.listdir('data/player_tables'): os.mkdir('data/player_tables/json')
for p in batting_player_records.keys():
    p_df= (pd.DataFrame(batting_player_records[p])
        .drop(columns=['Batting']))
    p_df.to_csv(f'data/player_tables/batting/{p}.csv')


for p in bowling_player_records.keys():
    p_df= (pd.DataFrame(bowling_player_records[p])
        .drop(columns=['Bowling']))
    p_df.to_csv(f'data/player_tables/bowling/{p}.csv')

# PVP
# Name, Run rate, Run variance, Run mean
# Ball rate, Ball variance, ball mean
#
#
#
#

# PVP BAT
bat_comparative_records = []
for p, p_df in batting_player_records.items():
    df = pd.DataFrame(p_df)
    #ic(df.columns)
    #remove -
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if (df.iloc[i,j]) == '-': df.iloc[i,j] = 0
    
    run_std = (df['R'].astype(float).std())
    run_median = (df['R'].astype(float).median())
    run_max = (df['R'].astype(float).max())
    fours_median = (df['4s'].astype(float).median())
    sixes_median = (df['6s'].astype(float).median())
    fours_max = (df['4s'].astype(float).max())
    sixes_max = (df['6s'].astype(float).max())
    #ic(f'{p = }, {i = }, {j = }, {balls_when_run_max= } {run_max= },')
    bat_comparative_records.append(
        {
            'Name': p,
            'run_median': run_median,
            'run_std': run_std,
            'run_max': run_max,
            'fours_median': fours_median,
            'sixes_median': sixes_median,
            'fours_max': fours_max,
            'sixes_max': sixes_max,
        }
    )

pd.DataFrame(bat_comparative_records).to_csv('data/batting_comparison_table.csv')

# PVP boll
bowl_comparative_records = []
for p, p_df in bowling_player_records.items():
    df = pd.DataFrame(p_df)
    #ic(df.columns)
    #remove -
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if (df.iloc[i,j]) == '-': df.iloc[i,j] = 0
    
    wicket_std = (df['W'].astype(float).std())
    wicket_median = (df['W'].astype(float).median())
    wicket_max = (df['W'].astype(float).max())
    economy_median = (df['ECON'].astype(float).median())
    economy_std = (df['ECON'].astype(float).std())
    #ic(f'{p = }, {i = }, {j = }, {balls_when_run_max= } {run_max= },')
    bowl_comparative_records.append(
        {
            'Name': p,
            'wicket_std': wicket_std,
            'wicket_median': wicket_median,
            'wicket_max': wicket_max,
            'economy_median': economy_median,
            'economy_std': economy_std,
        }
    )

pd.DataFrame(bowl_comparative_records).to_csv('data/bowling_comparison_table.csv')