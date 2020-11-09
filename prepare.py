import pandas as pd
import numpy as np 
import os

from sklearn.model_selection import train_test_split
import sklearn.preprocessing



def prep_nba(season):
    '''
    This function creates new columns and deletes unneeded columns
    '''
    #splits teams and opponents into respective conferences
    nba = conference_split(season)

    #changing conference into dummy variable
    conference = pd.get_dummies(nba.Conference, drop_first = True)

    #changing Opp.Conference into dummy variable
    oppconference = pd.get_dummies(nba['Opp.Conference'], drop_first = True)
    
    #changing home into dummy variable
    home = pd.get_dummies(nba.Home, drop_first = True)

    #changing target variable into dummy variable
    wins = pd.get_dummies(nba.WINorLOSS, drop_first = True)

    #dropping unnecessary columns
    nba = nba.drop(columns = ['Unnamed: 0', 'Home', 'WINorLOSS', 'Date', 'Game', 'OpponentPoints', 'FieldGoals', 'Opp.FieldGoals', 'FieldGoalsAttempted', 'Opp.FieldGoalsAttempted', 'X3PointShots', 'Opp.3PointShots', 'X3PointShotsAttempted', 'Opp.3PointShotsAttempted', 'FreeThrows', 'Opp.FreeThrows', 'FreeThrowsAttempted', 'Opp.FreeThrowsAttempted', 'Conference', 'Opp.Conference'])

    #adding dummy variables back into the main dataframe
    nba = pd.concat([nba, conference, oppconference, home, wins], axis = 1)

    return nba


def conference_split(nba):
    '''
    This functioin splits the Team and Opponent into Conferences.
    '''
    #setting conditions for conference
    conditions = [
        #west teams
        (nba.Team.isin(['LAL', 'LAC', 'DEN', 'HOU', 'OKC', 'UTA', 'DAL', 'POR', 'MEM', 'PHO', 'SAS', 'SAC', 'NOP', 'MIN', 'GSW'])),
        #east teams
        (nba.Team.isin(['MIL', 'TOR', 'BOS', 'IND', 'MIA', 'PHI', 'BRK', 'ORL', 'WAS', 'CHO', 'CHI', 'NYK', 'DET', 'ATL', 'CLE']))]
    choices = ['home_is_west', 'home_is_east']
    #creating conference column for home team
    nba['Conference'] = np.select(conditions, choices, default='west')
    #setting conditions for oppConference
    conditions2 = [
        #west teams
        (nba.Opponent.isin(['LAL', 'LAC', 'DEN', 'HOU', 'OKC', 'UTA', 'DAL', 'POR', 'MEM', 'PHO', 'SAS', 'SAC', 'NOP', 'MIN', 'GSW'])),
        #east teams
        (nba.Opponent.isin(['MIL', 'TOR', 'BOS', 'IND', 'MIA', 'PHI', 'BRK', 'ORL', 'WAS', 'CHO', 'CHI', 'NYK', 'DET', 'ATL', 'CLE']))]
    choices2 = ['away_is_west', 'away_is_east']
    #creating oppConference column for away team
    nba['Opp.Conference'] = np.select(conditions2, choices2, default='west')
    return nba


def nba_split(df):
    '''
    This function splits a dataframe into train, validate, and test sets
    '''
    train_and_validate, test = train_test_split(df, train_size=.8, random_state=123, stratify=df.W)
    train, validate = train_test_split(train_and_validate, train_size = .7, random_state=123, stratify=train_and_validate.W)
    return train, validate, test

def wrangle_nba():
    '''
    This function splits the nba seasons into train, validate, and test sets
    '''
    #save csv as a dataframe
    nba = pd.read_csv('nba.games.stats.csv')
    #preppring dataframe nba stats
    nba = prep_nba(nba)
    #splitting into train, validate test
    train, validate, test = nba_split(nba)
    return train, validate, test

def scaled_wrangle_nba():
    '''
    This function scales the data and splits 
    the nba seasons into train, validate, and test sets
    '''
    #save csv as a dataframe
    nba = pd.read_csv('nba.games.stats.csv')
    #preppring dataframe nba stats
    nba = prep_nba(nba)
    #splitting into train, validate test
    train, validate, test = nba_split(nba)
    #assigns the scaling method as min-max scaler
    scaler = sklearn.preprocessing.MinMaxScaler()
    #identifies the columns to scale
    columns_to_scale = ['FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls']
    #adds '_scaled' to the end of the newly scaled columns to identify differences
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    #fts the columns to the scaler
    scaler.fit(train[columns_to_scale])
    #concatonates the newly created scaled columns to their respective data sets,
    #adds 'new_column_names' as the label to the added columns
    #uses the original index since the new columns no longer have an index
    train = pd.concat([
        train,
        pd.DataFrame(scaler.transform(train[columns_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler.transform(validate[columns_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    test = pd.concat([
        test,
        pd.DataFrame(scaler.transform(test[columns_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)
    #drops non-scaled data
    train = train.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls'})
    validate = validate.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls'})
    test = test.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls'})
    return train, validate, test