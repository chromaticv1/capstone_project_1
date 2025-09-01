import pandas as pd
df = pd.read_csv('data/match_stats.csv')

df = df[df['match_result']!= 'Abandoned game']

#VS STADIUM
venue_stats = []
venue_names = df['venue'].unique().tolist()
for v in venue_names:
    o = {   'venue': v,
            'total_played' : df.loc[df['venue']==v].shape[0],
            'total_won' : df.loc[(df['venue']==v) & (df['bd_won']==True)].shape[0],
        }
    o['winrate']= o['total_won']/o['total_played']*100
    venue_stats.append(o)
pd.DataFrame(venue_stats).to_csv('data/stadium_stats.csv')

#VS OPPONENT
opponent_stats = []
opponent_names = df['opponent'].unique().tolist()
for v in opponent_names:
    o = {   'opponent': v,
            'total_played' : df.loc[df['opponent']==v].shape[0],
            'total_won' : df.loc[(df['opponent']==v) & (df['bd_won']==True)].shape[0],
        }
    o['winrate']= None if o['total_played'] == 0 else o['total_won']/o['total_played']*100
    opponent_stats.append(o)
pd.DataFrame(opponent_stats).to_csv('data/opponent_stats.csv')