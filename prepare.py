import pandas as pd
import numpy as np 
import os

from sklearn.model_selection import train_test_split
import sklearn.preprocessing

from requests import get
from bs4 import BeautifulSoup



############################### origninal dataframe functions ###########################

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

    #dropping unnecessary columns
    nba = nba.drop(columns = ['Unnamed: 0', 'Home', 'WINorLOSS', 'WINorLOSS', 'Date', 'Game', 'OpponentPoints', 'FieldGoals', 'Opp.FieldGoals', 'FieldGoalsAttempted', 'Opp.FieldGoalsAttempted', 'X3PointShots', 'Opp.3PointShots', 'X3PointShotsAttempted', 'Opp.3PointShotsAttempted', 'FreeThrows', 'Opp.FreeThrows', 'FreeThrowsAttempted', 'Opp.FreeThrowsAttempted', 'Conference', 'Opp.Conference'])

    #adding dummy variables back into the main dataframe
    nba = pd.concat([nba, conference, oppconference, home], axis = 1)

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
    train_and_validate, test = train_test_split(df, train_size=.8, random_state=123)
    train, validate = train_test_split(train_and_validate, train_size = .7, random_state=123)
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



############################# advanced metrics functions ###############################

def get_url_pages():
    '''
    This function creates a list of url pages 
    of teams within a range of seasons
    '''
    urls = []
    years = ['2015', '2016', '2017', '2018']
    teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    for year in years:
        for team in teams:
            urls.append(f"https://www.basketball-reference.com/teams/{team}/{year}/gamelog-advanced/")
    return urls

def make_soup(url=''):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'NLP3'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def scrape_advanced_metrics(urls=[]):
    '''
    This function takes in a list of urls
    and returns the advanced data metrics
    of each game for each team, 
    in a specified number of seasons
    '''
    total_data = pd.DataFrame()
    requests = 0
    for url in urls:
        requests += 1
        print(requests)
        soup = make_soup(url)
        team = pd.read_html(str(soup.find_all('table')[0]), header=1)[0]
        total_data = total_data.append(team, ignore_index=True)
    return total_data

def get_advanced_metrics():
    '''
    This function scrapes the advanced metrics from
    Basketball Reference and saves it as a CSV
    '''
    # creates a list of url pages 
    # of teams within a range of seasons
    urls = get_url_pages()
    # takes in a list of urls
    # and returns the advanced data metrics
    adv_metrics = scrape_advanced_metrics(urls)
    # saves advanced metrics as a CSV
    adv_metrics.to_csv('advanced_metrics_data.csv')

def prep_advanced_metrics():
    '''
    This function cleans the advanced_metrics_data_csv 
    and saves it into another csv
    '''
    # reads in csv
    teams = pd.read_csv('advanced_metrics_data.csv', index_col = 0)
    # deleting empty columns
    del teams['Unnamed: 3']
    del teams['Unnamed: 18']
    del teams['Unnamed: 23']
    # dropping rows with null values(column headers)
    teams.dropna(axis=0, inplace=True)
    # resetting the index
    teams = teams.reset_index(drop=True)
    # finding rows that are dupplicate of column headers
    rows_to_drop = [row for row in teams[teams.Tm.isin(['Tm'])].index]
    # reversing the order of the list
    rows_to_drop.reverse()
    # dropping extra headers
    teams.drop(rows_to_drop, inplace = True)
    # restting the index
    teams = teams.reset_index(drop=True)
    # save the cleaned dataframe as a csv
    teams.to_csv('cleaned_advanced_metrics_data.csv')

def advanced_metrics_dataframe():
    '''
    This function combines the original dataframe with
    the cleaned advanced metrics dataframe
    '''
    # importing original dataframe
    df = pd.read_csv('nba.games.stats.csv', index_col = 0)
    #resstting the index
    df = df.reset_index()
    #importing the cleaned advanced metrics
    teams = pd.read_csv('cleaned_advanced_metrics_data.csv', index_col = 0)
    # deleting duplicate columns
    teams = teams.iloc[:, 7:]
    # renaming columns
    teams = teams.rename(columns = {'eFG%.1': 'Opp.eFG%', 'TOV%.1': 'Opp.TOV%', 'FT/FGA.1':'Opp.FT/FGA'})
    #combining dataframes
    teams = pd.concat([df, teams], axis=1)
    # deleting index column
    teams = teams.drop(columns = {'index'})
    return teams

def prep_nba_advanced_metrics(season):
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

    #dropping unnecessary columns
    nba = nba.drop(columns = ['Home', 'WINorLOSS', 'WINorLOSS', 'Date', 'Game', 'OpponentPoints', 'FieldGoals', 'Opp.FieldGoals', 'FieldGoalsAttempted', 'Opp.FieldGoalsAttempted', 'X3PointShots', 'Opp.3PointShots', 'X3PointShotsAttempted', 'Opp.3PointShotsAttempted', 'FreeThrows', 'Opp.FreeThrows', 'FreeThrowsAttempted', 'Opp.FreeThrowsAttempted', 'Conference', 'Opp.Conference'])

    #adding dummy variables back into the main dataframe
    nba = pd.concat([nba, conference, oppconference, home], axis = 1)

    return nba



def scaled_advanced_metrics():
    '''
    This function scales the data and splits 
    the nba seasons into train, validate, and test sets
    '''
    # importing advanced metrics
    df = advanced_metrics_dataframe()
    # prepping df
    df = prep_nba_advanced_metrics(df)
    #splitting into train, validate test
    train, validate, test = nba_split(df)
    #assigns the scaling method as min-max scaler
    scaler = sklearn.preprocessing.MinMaxScaler()
    #identifies the columns to scale
    columns_to_scale = ['FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp.eFG%', 'Opp.TOV%', 'DRB%', 'Opp.FT/FGA']
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
    train = train.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp.eFG%', 'Opp.TOV%', 'DRB%', 'Opp.FT/FGA'})
    validate = validate.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp.eFG%', 'Opp.TOV%', 'DRB%', 'Opp.FT/FGA'})
    test = test.drop(columns = {'FieldGoals.', 'X3PointShots.', 'FreeThrows.', 'OffRebounds', 'TotalRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'TotalFouls', 'Opp.FieldGoals.', 'Opp.3PointShots.', 'Opp.FreeThrows.', 'Opp.OffRebounds', 'Opp.TotalRebounds', 'Opp.Assists', 'Opp.Steals', 'Opp.Blocks', 'Opp.Turnovers', 'Opp.TotalFouls', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp.eFG%', 'Opp.TOV%', 'DRB%', 'Opp.FT/FGA'})
    return train, validate, test