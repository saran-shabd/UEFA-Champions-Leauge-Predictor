"""UEFA Champions League Group Stage 2017-18
Data Pre-processor, extracts data from the HTML into CSVs, clean that dataset

@author Shabd Saran
"""

import pandas as pd
import numpy as np
from pandas import DataFrame


# import the tables from HTML file
with open('../data/html/group-stage-2017-18.html') as file:
    tables: list = pd.read_html(file)


def clean_group_stage_df(df: DataFrame) -> DataFrame:
    """remove unnecessary columns from the dataframe & add some useful ones"""
    
    # only include necessary columns
    df = df[['Pos', 'Team[ vte ]', 'GF', 'GA', 'Pts']]
    
    # add Goal Difference
    df['GD'] = df['GF'] - df['GA']
    df = df.drop(['GA', 'GF'], axis=1)
    
    # add if the team qualify for the round-16
    df['Qualify'] = [1, 1, 0, 0]
    
    # convert group-stage points of each team into integers
    pts: list = df['Pts'].values
    for i in range(4):
        if type(pts[i]) == np.int64:
            continue
        if len(pts[i]) > 2:
            pts[i] = int(pts[i][:-3])
        else:
            pts[i] = int(pts[i])
    df = df.astype({'Pts': np.int64})
    
    # invert group stage positions, so that they will favour more to those
    # having lower ranks (numerically) in real
    df['Pos'] = 4 - df['Pos']
    
    return df


# get all groups information
group_a: DataFrame = clean_group_stage_df(tables[9])
group_b: DataFrame = clean_group_stage_df(tables[22])
group_c: DataFrame = clean_group_stage_df(tables[35])
group_d: DataFrame = clean_group_stage_df(tables[48])
group_e: DataFrame = clean_group_stage_df(tables[61])
group_f: DataFrame = clean_group_stage_df(tables[74])
group_g: DataFrame = clean_group_stage_df(tables[87])
group_h: DataFrame = clean_group_stage_df(tables[100])

# put all the teams into a single dataframe
teams = group_a.append([group_b, group_c, group_d, group_e, group_f, 
                            group_g, group_h])

# remove not interested teams
teams = teams[teams['Team[ vte ]'].isin(['Real Madrid', 'Barcelona', 
                      'Bayern Munich', 'Atlético Madrid', 'Juventus', 
                      'Manchester City', 'Paris Saint-Germain', 'Liverpool',
                      'Tottenham Hotspur', 'Chelsea', 'Borussia Dortmund'])]

# change name of all the columns
teams.columns = ['Pos_2017-18', 'Club', 'Pts_2017-18', 'GD_2017-18', 
                 'Qualify_2017-18']
    
# set team name as the index
teams.set_index('Club', inplace=True)

# store the computed result in a CSV file
teams.to_csv('../data/data/group-stage-2017-18.csv')
