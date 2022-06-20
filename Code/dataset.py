import glob
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from operator import itemgetter
import csv
import math
import datetime
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

######### FUNCTIONS #########
def get_cleaned(file):
    '''
    remove retirements, walkovers, DavisCup etc
    save file as type_matches_year[cleaned].csv
    return cleaned file
    '''
    dt = pd.read_csv(file, index_col=None, header=0)
    dt = dt[dt['score'].str.contains(r'RET') == False]
    dt = dt[dt['score'].str.contains(r'W/O') == False]
    dt = dt[dt['score'].str.contains(r'DEF') == False]
    dt = dt[dt['tourney_level'].str.contains('D') == False]
    dt.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + str(file[72:75]) + "_matches_" + str(file[84:88]) + "[cleaned].csv")
    return dt
def get_data(files, players):
    '''
    get all match files together and save them cleaned
    also players in a better form (not cleaned yet)
    and return dataFrames matches, players
    '''
    matches_list = []
    for file in files:
        df = get_cleaned(file)
        matches_list.append(df)
    type = str(files[0][72:75])
    matches = pd.concat(matches_list)
    matches.sort_values(['tourney_date', 'tourney_id'], inplace=True)
    players['player_name'] = players['name_first'] + ' ' + players['name_last']
    players = players.sort_values(['player_name'])
    players = players[['player_id', 'player_name', 'hand', 'dob', 'ioc', 'height']]

    matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "_matches[cleaned].csv")
    players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "_players[raw].csv")
    return matches, players
def get_players(dt_matches, type, dt_players):
    '''
    clean players' file
    so as to contain players that participate
    in games since the desired date
    save the file as [cleaned]
    return the dataFrame
    '''
    winners = dt_matches.groupby('winner_name').size()
    losers = dt_matches.groupby('loser_name').size()
    df_matches = pd.DataFrame({'Wins': winners, 'Losses': losers}).fillna(0)
    df_matches[['Wins', 'Losses']] = df_matches[['Wins', 'Losses']].astype(int)
    df_matches = df_matches.reindex(['Wins', 'Losses'], axis=1)
    df_matches['Matches'] = df_matches['Wins'] + df_matches['Losses']
    df_matches.index.name = 'player_name'
    df_matches.reset_index(level=0, inplace=True)

    players_list = list(df_matches['player_name'])
    df_players = dt_players[dt_players.player_name.isin(players_list)]
    df_players.sort_values(['player_name'])
    df_players = df_players[['player_id', 'player_name', 'hand', 'dob', 'ioc', 'height']].fillna(0)
    df_players.replace(to_replace=0, value=(df_players['height'].loc[df_players['height'] != 0]).median(), inplace=True)

    df_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "_players[cleaned].csv")
    return df_players

def get_surface(dt_matches, surface_type):
    dt_surface = dt_matches[(dt_matches['surface'] == surface_type)]
    return dt_surface
def get_per_surface(dt_matches, surface_types, type):
    surfaces_list = []

    for t in surface_types:
        dt_surface = get_surface(dt_matches, t)
        winners = dt_surface.groupby('winner_name').size()
        losers = dt_surface.groupby('loser_name').size()
        dt_new_surface = pd.DataFrame({'wins_' + str(t): winners, 'losses_' + str(t): losers}).fillna(0)
        dt_new_surface[['wins_' + str(t), 'losses_' + str(t)]] = dt_new_surface[['wins_' + str(t), 'losses_' + str(t)]].astype(int)
        dt_new_surface = dt_new_surface.reindex(['wins_' + str(t), 'losses_' + str(t)], axis=1)
        dt_new_surface['matches_' + str(t)] = dt_new_surface['wins_' + str(t)] + dt_new_surface['losses_' + str(t)]
        dt_new_surface[str(t) + '(%)'] = np.round((dt_new_surface['wins_' + str(t)] / dt_new_surface['matches_' + str(t)]) * 100, 2)
        dt_new_surface.index.name = 'player_name'
        dt_new_surface = dt_new_surface.sort_values(['player_name'])
        dt_new_surface.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + str(type) + "[" + str(t) + "].csv")

        surfaces_list.append(dt_new_surface)
    return surfaces_list
def get_surfaces_together(dt_matches, type):
    surface_types = ['Hard', 'Grass', 'Clay', 'Carpet']

    pd_surfaces_list = get_per_surface(dt_matches, surface_types, type)
    type_1 = surface_types[0]
    type_2 = surface_types[1]
    type_3 = surface_types[2]
    type_4 = surface_types[3]

    pd_cat_1 = pd.concat([pd_surfaces_list[0], pd_surfaces_list[1]], axis=1).fillna(0)
    pd_cat_1['M1'] = pd_cat_1['matches_' + type_1] + pd_cat_1['matches_' + type_2]
    pd_cat_2 = pd.concat([pd_surfaces_list[2], pd_surfaces_list[3]], axis=1).fillna(0)
    pd_cat_2['M2'] = pd_cat_2['matches_' + type_3] + pd_cat_2['matches_' + type_4]

    pd_surfaces = pd.concat([pd_cat_1, pd_cat_2], axis=1).fillna(0)
    pd_surfaces['total_matches'] = pd_surfaces['M1'] + pd_surfaces['M2']
    pd_surfaces = pd_surfaces[['total_matches',
                               'wins_Hard', 'losses_Hard', 'Hard(%)',
                               'wins_Grass', 'losses_Grass', 'Grass(%)',
                               'wins_Clay', 'losses_Clay', 'Clay(%)',
                               'wins_Carpet', 'losses_Carpet', 'Carpet(%)']]
    pd_surfaces = pd_surfaces.reset_index(level=0)
    pd_surfaces.rename(columns={'index': 'player_name'}, inplace=True)
    pd_surfaces = pd_surfaces.sort_values(['player_name'])
    #pd_surfaces.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "[surfaces].csv")

    return pd_surfaces

def get_firstServeSucc(metrics):
    # Percentage of successful first serves
    metrics['w_1stS(%)'] = round((metrics['w_1stIn'] / metrics['w_svpt']) * 100, 2)
    metrics['l_1stS(%)'] = round((metrics['l_1stIn'] / metrics['l_svpt']) * 100, 2)
    return metrics
def get_secondServeSucc(metrics):
    # Percentage of successful second serves
    metrics['w_2ndIn'] = metrics['w_svpt'] - metrics['w_1stIn']
    metrics['l_2ndIn'] = metrics['l_svpt'] - metrics['l_1stIn']
    return metrics
def get_firstServePointsWon(metrics):
    # Percentage of first serve points won
    metrics['w_1st_svpt(%)'] = round((metrics['w_1stWon'] / metrics['w_1stIn']) * 100, 2)
    metrics['l_1st_svpt(%)'] = round((metrics['l_1stWon'] / metrics['l_1stIn']) * 100, 2)
    return metrics
def get_secondServePointsWon(metrics):
    # Percentage of second serve points won
    metrics['w_2nd_svpt(%)'] = round((metrics['w_2ndWon'] / metrics['w_2ndIn']) * 100, 2)
    metrics['l_2nd_svpt(%)'] = round((metrics['l_2ndWon'] / metrics['l_2ndIn']) * 100, 2)
    return metrics
def get_firstServeReturnPointsWon(metrics):
    # Number of first serve return points won
    metrics['w_1stS_rtpWon'] = metrics['l_1stIn'] - metrics['l_1stWon']
    metrics['l_1stS_rtpWon'] = metrics['w_1stIn'] - metrics['w_1stWon']
    return metrics
def get_secondServeReturnPointsWon(metrics):
    # Number of second serve return points won
    metrics['w_2ndS_rtpWon'] = metrics['l_2ndIn'] - metrics['l_2ndWon']
    metrics['l_2ndS_rtpWon'] = metrics['w_2ndIn'] - metrics['w_2ndWon']
    return metrics
def get_percFirstServeReturnPointsWon(metrics):
    # Percentage of first serve return points won
    metrics['w_1stS_rtpWon(%)'] = round((metrics['w_1stS_rtpWon'] / metrics['l_1stIn']) * 100, 2)
    metrics['l_1stS_rtpWon(%)'] = round((metrics['l_1stS_rtpWon'] / metrics['w_1stIn']) * 100, 2)
    return metrics
def get_percSecondServeReturnPointsWon(metrics):
    # Percentage of second serve return points won
    metrics['w_2ndS_rtpWon(%)'] = round((metrics['w_2ndS_rtpWon'] / metrics['l_2ndIn']) * 100, 2)
    metrics['l_2ndS_rtpWon(%)'] = round((metrics['l_2ndS_rtpWon'] / metrics['w_2ndIn']) * 100, 2)
    return metrics
def get_percBreakPointsWon(metrics):
    # Percentage of break points won
    metrics['w_bpWon(%)'] = round((metrics['w_bpSaved'] / metrics['w_bpFaced']) * 100, 2)
    metrics['l_bpWon(%)'] = round((metrics['l_bpSaved'] / metrics['l_bpFaced']) * 100, 2)
    return metrics
def get_breakPointsWon(metrics):
    # Number of break points won
    metrics['w_bpWon'] = metrics['l_bpFaced'] - metrics['l_bpSaved']
    metrics['l_bpWon'] = metrics['w_bpFaced'] - metrics['w_bpSaved']
    return metrics
def get_percBreakPointsConverted(metrics):
    # Percentage of break points converted
    metrics['w_bpConv(%)'] = round((metrics['w_bpWon'] / metrics['l_bpFaced']) * 100, 2)
    metrics['l_bpConv(%)'] = round((metrics['l_bpWon'] / metrics['w_bpFaced']) * 100, 2)
    return metrics
def get_metrics(dt_matches, type):
    dt_matches = get_firstServeSucc(dt_matches)
    dt_matches = get_secondServeSucc(dt_matches)
    dt_matches = get_firstServePointsWon(dt_matches)
    dt_matches = get_secondServePointsWon(dt_matches)
    dt_matches = get_firstServeReturnPointsWon(dt_matches)
    dt_matches = get_secondServeReturnPointsWon(dt_matches)
    dt_matches = get_percFirstServeReturnPointsWon(dt_matches)
    dt_matches = get_percSecondServeReturnPointsWon(dt_matches)
    dt_matches = get_percBreakPointsWon(dt_matches)
    dt_matches = get_breakPointsWon(dt_matches)
    dt_matches = get_percBreakPointsConverted(dt_matches)

    dt_metrics = dt_matches[['tourney_id', 'tourney_name', 'tourney_date', 'match_num', 'winner_name', 'loser_name',
                             'score', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms',
                             'w_bpSaved', 'w_bpFaced', 'w_1stS(%)', 'w_2ndIn', 'w_1st_svpt(%)', 'w_2nd_svpt(%)',
                             'w_1stS_rtpWon', 'w_2ndS_rtpWon', 'w_1stS_rtpWon(%)', 'w_2ndS_rtpWon(%)', 'w_bpWon(%)',
                             'w_bpWon', 'w_bpConv(%)', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon',
                             'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'l_1stS(%)', 'l_2ndIn', 'l_1st_svpt(%)',
                             'l_2nd_svpt(%)', 'l_1stS_rtpWon',  'l_2ndS_rtpWon', 'l_1stS_rtpWon(%)', 'l_2ndS_rtpWon(%)',
                             'l_bpWon(%)', 'l_bpWon', 'l_bpConv(%)']]

    dt_metrics.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "[PerformanceMetrics].csv")
    return dt_matches

def get_date(dt_matches):
    dt_matches['year'] = dt_matches['tourney_date'].astype(str).str[0:4].astype(int)
    dt_matches['month'] = dt_matches['tourney_date'].astype(str).str[4:6].astype(int)
    dt_matches['date'] = dt_matches['tourney_date'].astype(str).str[6:8].astype(int)
    return dt_matches
def get_last_two_weeks_date(time_now):
    # format: time_now = '03/10/07 00:00:00'
    # time_now is a string and i want to convert it to datetime object
    date = datetime.datetime.strptime(time_now, '%d/%m/%y %H:%M:%S')
    # get the date of the start of 2 last weeks
    last2weeks = date - timedelta(weeks=2)
    year = str(last2weeks)[0:4]
    month = str(last2weeks)[5:7]
    day = str(last2weeks)[8:10]
    return year, month, day
def get_last_two_weeks(dt_matches, time_now):
    dt_matches.sort_values(['tourney_date', 'match_num'], ascending=True, inplace=True)
    year, month, day = get_last_two_weeks_date(time_now)
    date = int(str(year)+ str(month) + str(day))
    dt = dt_matches[(dt_matches['tourney_date'] >= date)]
    return dt
def get_last_semester(dt_matches, current_year, current_month):
    dt = dt_matches[(dt_matches['year'].isin([current_year-1, current_year]))]
    last_months = [6, 7, 8, 9, 10, 11, 12]
    if current_month in last_months:
        dt = dt[(dt['year']==current_year)]
        dt = dt[dt['month'].isin([current_month-5, current_month-4, current_month-3,
                                  current_month-2, current_month-1, current_month])]
    elif current_month == 5:
        dt1 = dt[(dt['year'] == current_year)]
        dt1 = dt1[(dt1['month'].isin([5, 4, 3, 2, 1]))]
        dt2 = dt[(dt['year'] == current_year-1)]
        dt2 = dt2[(dt2['month'] == 12)]
        dt = pd.concat([dt1, dt2])
    elif current_month == 4:
        dt1 = dt[(dt['year'] == current_year)]
        dt1 = dt1[(dt1['month'].isin([4, 3, 2, 1]))]
        dt2 = dt[(dt['year'] == current_year-1)]
        dt2 = dt2[(dt2['month'].isin([11, 12]))]
        dt = pd.concat([dt1, dt2])
    elif current_month == 3:
        dt1 = dt[(dt['year']==current_year)]
        dt1 = dt1[(dt1['month'].isin([3, 2, 1]))]
        dt2 = dt[(dt['year']==current_year-1)]
        dt2 = dt2[(dt2['month'].isin([10, 11, 12]))]
        dt = pd.concat([dt1, dt2])
    elif current_month == 2:
        dt1 = dt[(dt['year'] == current_year)]
        dt1 = dt1[(dt1['month'].isin([2, 1]))]
        dt2 = dt[(dt['year'] == current_year-1)]
        dt2 = dt2[(dt2['month'].isin([9, 10, 11, 12]))]
        dt = pd.concat([dt1, dt2])
    elif current_month == 1:
        dt1 = dt[(dt['year'] == current_year)]
        dt1 = dt1[(dt1['month'] == 1)]
        dt2 = dt[(dt['year'] == current_year-1)]
        dt2 = dt2[(dt2['month'].isin([8, 9, 10, 11, 12]))]
        dt = pd.concat([dt1, dt2])
    dt.sort_values(['tourney_date', 'match_num'], ascending=True, inplace=True)
    return dt
def get_last_year(dt_matches, current_year, current_month):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    dt = dt_matches[(dt_matches['year'].isin([current_year - 1, current_year]))]
    dt1 = dt[(dt['year'] == current_year)]
    dt1 = dt1[(dt1['month'].isin(months[0:current_month]))]
    dt2 = dt[(dt['year'] == current_year - 1)]
    dt2 = dt2[(dt2['month'].isin(months[current_month-1::]))]
    dt = pd.concat([dt1, dt2])
    dt.sort_values(['tourney_date', 'match_num'], ascending=True, inplace=True)
    return dt
def get_totalWinsLosses(dt_matches, type, period):
    finals = dt_matches[(dt_matches['round'] == 'F')]
    semifinals = dt_matches[(dt_matches['round'] == 'SF')]
    titles_ = finals.groupby('winner_name').size()
    finals_ = semifinals.groupby('winner_name').size()
    winners = dt_matches.groupby('winner_name').size()
    losers = dt_matches.groupby('loser_name').size()

    pd_total = pd.DataFrame({'Wins_' + period: winners, 'Losses_' + period: losers}).fillna(0)
    pd_total[['Wins_' + period, 'Losses_' + period]] = pd_total[['Wins_' + period, 'Losses_' + period]].astype(int)
    pd_total = pd_total.reindex(['Wins_' + period, 'Losses_' + period], axis=1)
    pd_total['Matches_' + period] = pd_total['Wins_' + period] + pd_total['Losses_' + period]
    pd_total['Wins(%)_' + period] = np.round(pd_total['Wins_' + period] * 100 / pd_total['Matches_' + period], 2)
    pd_total.index.name = 'player_name'
    pd_total = pd_total.join(pd.DataFrame(finals_, columns=['Finals_' + period], )).fillna(0)
    pd_total = pd_total.join(pd.DataFrame(titles_, columns=['Titles_' + period], )).fillna(0)
    pd_total['Titles_' + period] = pd_total['Titles_' + period].astype(int)
    pd_total['Finals_' + period] = pd_total['Finals_' + period].astype(int)
    pd_total = pd_total.sort_values(['player_name'])
    pd_total.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + str(type) + "[WinsLossesTitles" + period + "].csv")
    return pd_total

def get_home_advantage(dt_matches, type):
    home = dt_matches
    conditions = [
        (home['tourney_name'] == 'Adelaide'), (home['tourney_name'] == 'Doha'),
        (home['tourney_name'] == 'Chennai'), (home['tourney_name'] == 'Auckland'),
        (home['tourney_name'] == 'Sydney'), (home['tourney_name'] == 'Australian Open'),
        (home['tourney_name'] == 'San Jose'), (home['tourney_name'] == 'Dubai'),
        (home['tourney_name'] == 'Marseille'), (home['tourney_name'] == 'Memphis'),
        (home['tourney_name'] == 'Rotterdam'), (home['tourney_name'] == 'London'),
        (home['tourney_name'] == 'Mexico City'), (home['tourney_name'] == 'Copenhagen'),
        (home['tourney_name'] == 'Delray Beach'), (home['tourney_name'] == 'Santiago'),
        (home['tourney_name'] == 'Bogota'), (home['tourney_name'] == 'Scottsdale'),
        (home['tourney_name'] == 'Indian Wells Masters'),
        (home['tourney_name'] == 'Miami Masters'), (home['tourney_name'] == 'Casablanca'),
        (home['tourney_name'] == 'Atlanta'), (home['tourney_name'] == 'Estoril'),
        (home['tourney_name'] == 'Monte Carlo Masters'), (home['tourney_name'] == 'Barcelona'),
        (home['tourney_name'] == 'Munich'), (home['tourney_name'] == 'Mallorca'),
        (home['tourney_name'] == 'Orlando'), (home['tourney_name'] == 'Rome Masters'),
        (home['tourney_name'] == 'Hamburg Masters'), (home['tourney_name'] == 'Dusseldorf'),
        (home['tourney_name'] == 'St. Poelten'), (home['tourney_name'] == 'Roland Garros'),
        (home['tourney_name'] == "Queen's Club"), (home['tourney_name'] == 'Halle'),
        (home['tourney_name'] == 's Hertogenbosch'), (home['tourney_name'] == 'Nottingham'),
        (home['tourney_name'] == 'Wimbledon'), (home['tourney_name'] == 'Gstaad'),
        (home['tourney_name'] == 'Newport'), (home['tourney_name'] == 'Bastad'),
        (home['tourney_name'] == 'Amsterdam'), (home['tourney_name'] == 'Stuttgart Outdoor'),
        (home['tourney_name'] == 'Umag'), (home['tourney_name'] == 'Kitzbuhel'),
        (home['tourney_name'] == 'Los Angeles'), (home['tourney_name'] == 'San Marino'),
        (home['tourney_name'] == 'Canada Masters'), (home['tourney_name'] == 'Cincinnati Masters'),
        (home['tourney_name'] == 'Washington'), (home['tourney_name'] == 'Indianapolis'),
        (home['tourney_name'] == 'Long Island'), (home['tourney_name'] == 'US Open'),
        (home['tourney_name'] == 'Tashkent'), (home['tourney_name'] == 'Bucharest'),
        (home['tourney_name'] == 'Sydney Olympics'), (home['tourney_name'] == 'Palermo'),
        (home['tourney_name'] == 'Hong Kong'), (home['tourney_name'] == 'Tokyo'),
        (home['tourney_name'] == 'Vienna'), (home['tourney_name'] == 'Toulouse'),
        (home['tourney_name'] == 'Shanghai'), (home['tourney_name'] == 'Basel'),
        (home['tourney_name'] == 'Moscow'), (home['tourney_name'] == 'Stuttgart Masters'),
        (home['tourney_name'] == 'Lyon'), (home['tourney_name'] == 'St. Petersburg'),
        (home['tourney_name'] == 'Paris Masters'), (home['tourney_name'] == 'Stockholm'),
        (home['tourney_name'] == 'Brighton'), (home['tourney_name'] == 'Masters Cup'),
        (home['tourney_name'] == 'Milan'), (home['tourney_name'] == 'Vina del Mar'),
        (home['tourney_name'] == 'Buenos Aires'), (home['tourney_name'] == 'Acapulco'),
        (home['tourney_name'] == 'Houston'), (home['tourney_name'] == 'Stuttgart'),
        (home['tourney_name'] == 'Sopot'), (home['tourney_name'] == 'Costa Do Sauipe'),
        (home['tourney_name'] == 'Amersfoort'), (home['tourney_name'] == 'Madrid Masters'),
        (home['tourney_name'] == 'Valencia'), (home['tourney_name'] == 'Bangkok'),
        (home['tourney_name'] == 'Metz'), (home['tourney_name'] == 'Athens Olympics'),
        (home['tourney_name'] == 'Beijing'), (home['tourney_name'] == 'New Haven'),
        (home['tourney_name'] == 'Ho Chi Minh City'), (home['tourney_name'] == 'Zagreb'),
        (home['tourney_name'] == 'Las Vegas'), (home['tourney_name'] == 'Poertschach'),
        (home['tourney_name'] == 'Mumbai'), (home['tourney_name'] == 'Warsaw'),
        (home['tourney_name'] == 'Beijing Olympics'), (home['tourney_name'] == 'Brisbane'),
        (home['tourney_name'] == 'Johannesburg'), (home['tourney_name'] == 'Belgrade'),
        (home['tourney_name'] == 'Eastbourne'), (home['tourney_name'] == 'Hamburg'),
        (home['tourney_name'] == 'Kuala Lumpur'), (home['tourney_name'] == 'Shanghai Masters'),
        (home['tourney_name'] == 'Nice'), (home['tourney_name'] == 'Montpellier'),
        (home['tourney_name'] == 'Winston-Salem'), (home['tourney_name'] == 'Sao Paulo'),
        (home['tourney_name'] == 'London Olympics'), (home['tourney_name'] == 'Rio de Janeiro'),
        (home['tourney_name'] == 'Shenzhen'), (home['tourney_name'] == 'Quito'),
        (home['tourney_name'] == 'Istanbul'), (home['tourney_name'] == 'Geneva'),
        (home['tourney_name'] == 'Sofia'), (home['tourney_name'] == 'Marrakech'),
        (home['tourney_name'] == 'Los Cabos'), (home['tourney_name'] == 'Rio Olympics'),
        (home['tourney_name'] == 'Chengdu'), (home['tourney_name'] == 'Antwerp'),
        (home['tourney_name'] == 'Budapest'), (home['tourney_name'] == 'Antalya'),
        (home['tourney_name'] == 'NextGen Finals'), (home['tourney_name'] == 'Pune'),
        (home['tourney_name'] == 'New York'), (home['tourney_name'] == 'Cordoba'),
        (home['tourney_name'] == 'Zhuhai'), (home['tourney_name'] == 'Atp Cup'),
        (home['tourney_name'] == 'ATP Rio de Janeiro'), (home['tourney_name'] == 'Us Open'),
        (home['tourney_name'] == 'St Petersburg'), (home['tourney_name'] == 'Cologne 1'),
        (home['tourney_name'] == 'Sardinia'), (home['tourney_name'] == 'Cologne 2'),
        (home['tourney_name'] == 'Nur-Sultan'), (home['tourney_name'] == 'San Diego'),
        (home['tourney_name'] == 'Great Ocean Road Open'), (home['tourney_name'] == 'Murray River Open'),
        (home['tourney_name'] == 'Singapore'), (home['tourney_name'] == 'Marbella'),
        (home['tourney_name'] == 'Cagliari'), (home['tourney_name'] == 'Parma'),
        (home['tourney_name'] == 'Belgrade 2'), (home['tourney_name'] == 'Tokyo Olympics')
    ]
    values = [
        'AUS', 'QAT', 'IND', 'NZL', 'AUS', 'AUS', 'CRI', 'UAE', 'FRA', 'USA',
        'NDL', 'GBR', 'MEX', 'DNK', 'USA', 'CHI', 'COL', 'USA', 'USA', 'USA',
        'MAR', 'USA', 'PRT', 'MON', 'ESP', 'GER', 'ESP', 'USA', 'ITA', 'GER',
        'GER', 'AUT', 'FRA', 'GBR', 'GER', 'NLD', 'GBR', 'GBR', 'SUI', 'GBR',
        'SWE', 'NLD', 'GER', 'CRO', 'AUT', 'USA', 'SMR', 'CAN', 'USA', 'USA',
        'USA', 'USA', 'USA', 'UZB', 'ROU', 'AUS', 'ITA', 'CHN', 'JPN', 'AUT',
        'FRA', 'CHN', 'SUI', 'RUS', 'GER', 'FRA', 'RUS', 'FRA', 'SWE', 'GBR',
        'USA', 'ITA', 'CHI', 'ARG', 'MEX', 'USA', 'GER', 'POL', 'BRA', 'NDL',
        'ESP', 'ESP', 'THA', 'FRA', 'GRE', 'CHN', 'USA', 'VNM', 'CRO', 'USA',
        'AUT', 'IND', 'POL', 'CHN', 'AUS', 'RSA', 'SRB', 'GBR', 'GER', 'MAS',
        'CHN', 'FRA', 'FRA', 'USA', 'BRA', 'GBR', 'BRA', 'CHN', 'ECU', 'TUR',
        'SUI', 'BGR', 'MAR', 'MEX', 'BRA', 'CHN', 'BEL', 'HUN', 'TUR', 'ITA',
        'IND', 'USA', 'ESP', 'CHN', 'AUS', 'BRA', 'USA', 'RUS', 'GER', 'ITA',
        'GER', 'KAZ', 'AUS', 'AUS', 'SGP', 'ESP', 'ITA', 'ITA', 'SRB', 'JPN',
        'USA'
    ]
    home['location_country'] = np.select(conditions, values)

    # 1 is for the win, 2 is for the loss in homeCountry
    home['home_advantage'] = np.select([(home['winner_ioc'] == home['location_country'])], [1])
    home['home_advantage'] = np.select([(home['loser_ioc'] == home['location_country'])], [2])

    home_tosave = home[['tourney_id', 'tourney_name', 'location_country', 'winner_id',
                 'winner_name', 'winner_ioc', 'loser_id', 'loser_name', 'loser_ioc',
                 'score', 'round', 'winner_rank', 'winner_rank_points', 'loser_rank',
                 'loser_rank_points', 'home_advantage']]

    home_tosave.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/" + type + "[homeAdv].csv")
    return home

def get_stats_per_tournament(dt_matches, type, tour):
    matches = dt_matches[(dt_matches['tourney_name'] == tour)]

    finals = matches[(matches['round'] == 'F')]
    semifinals = matches[(matches['round'] == 'SF')]
    titles_ = finals.groupby('winner_name').size()
    finals_ = semifinals.groupby('winner_name').size()
    winners = matches.groupby('winner_name').size()
    losers = matches.groupby('loser_name').size()

    df = pd.DataFrame({'Wins':winners, 'Losses':losers}).fillna(0)
    df[['Wins', 'Losses']] = df[['Wins', 'Losses']].astype(int)
    df = df.reindex(['Wins', 'Losses'], axis=1)
    df['Matches'] = df['Wins'] + df['Losses']
    df['Wins(%)'] = np.round(df['Wins'] * 100 / df['Matches'], 2)
    df.index.name = 'player_name'
    df = df.join(pd.DataFrame(finals_, columns=['Finals'], )).fillna(0)
    df = df.join(pd.DataFrame(titles_, columns=['Titles'], )).fillna(0)
    df['Titles'] = df['Titles'].astype(int)
    df['Finals'] = df['Finals'].astype(int)
    df = df.sort_values(['player_name'])
    df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Tournament/" + type + "[" + str(tour) + "].csv")
    return
def get_tour(dt_matches, type):
    tourlist = ['Acapulco', 'Adelaide 1', 'Adelaide 2', 'Antalya', 'Atlanta', 'Antwerp', 'Atp Cup', 'Abu Dhabi',
                'ATP Rio de Janeiro', 'Auckland', 'Australian Open', 'Bangkok', 'Birmingham', 'Bol', 'Biel', 'Bad Homburg',
                'Barcelona', 'Basel', 'Bastad', 'Beijing', 'Bogota', 'Belgrade', 'Belgrade 2', 'Brisbane', 'Berlin',
                'Bucharest', 'Budapest', 'Buenos Aires', 'Calvia', 'Charleston', 'Cincinnati', 'Charleston 1', 'Charleston 2',
                'Cagliari', 'Canada Masters', 'Casablanca', 'Chengdu', 'Chennai', 'Chicago 1', 'Chicago 2',
                'Cincinnati Masters', 'Cologne 1', 'Cologne 2', 'Cordoba', 'Costa Do Sauipe', 'Cleveland',
                'Courmayeur', 'Cluj-Napoca 1', 'Cluj-Napoca 2', 'Dallas', 'Delray Beach', 'Doha', 'Gdynia',
                'Dubai', 'Dusseldorf', 'Eastbourne', 'Estoril', 'Florianopolis', 'Guadalajara', 'Grampians Trophy',
                'Geneva', 'Gstaad', 'Guangzhou', 'Great Ocean Road Open', 'Halle', 'Hobart', 'Hong Kong', 'Hua Hin',
                'Hamburg', 'Hiroshima', 'Houston', 'Indian Wells', 'Indian Wells Masters', 'Istanbul', 'Jurmala',
                'Johannesburg', 'Japan Open Tokyo', 'Kitzbuhel', 'Kuala Lumpur', 'Kaohsiung', 'Katowice',
                'Lausanne', 'Limoges', 'Linz', 'Los Angeles', 'Los Cabos', 'London Olympics',
                'Lyon', 'Luxembourg', 'Lugano', 'Lexington', 'Melbourne 2', 'Melbourne 1',
                'Madrid', 'Madrid Masters', 'Mallorca', 'Marbella', 'Miami', 'Monterrey', 'Montreal',
                'Marrakech', 'Marseille', 'Memphis', 'Melbourne', 'Metz', 'Miami Masters', 'Monte Carlo Masters',
                'Montpellier', 'Moscow', 'Munich', 'Murray River Open', 'New Haven', 'Nanchang',
                'Newport', 'New York', 'Nur-Sultan', 'NextGen Finals', 'Nice', 'Nottingham', 'Nurnberg',
                'Paris Masters', 'Pune', 'Parma', 'Palermo', 'Prague', 'Portoroz', 'Phillip Island Trophy',
                'Olympics', 'Osaka', 'Ostrava', "Queen's Club", 'Quebec City',
                'Quito', 'Rio de Janeiro', 'Rio Olympics', 'Roland Garros', 'Rome', 'Rome Masters', 'Rabat',
                'Rotterdam', 's Hertogenbosch', "s Hertogenbosch", 'San Antonio', 'Shenzhen Finals',
                'San Jose', 'Santiago', 'Singapore', 'Sardinia', 'Sao Paulo', 'Shanghai Masters', 'Seoul',
                'Shenzhen', 'Sofia', 'St. Petersburg', 'Stockholm', 'Stuttgart', 'Stanford',
                'Strasbourg', 'Sydney', 'Tashkent', 'Tianjin', 'Tokyo', 'Taipei', 'Toronto', 'Tenerife',
                'Tokyo Olympics', 'Tour Finals', 'Umag', 'US Open', 'Us Open', 'Valencia', 'Vienna',
                'Vina del Mar', 'Washington', 'Wimbledon', 'Winston-Salem', 'Wuhan', 'Yarra Valley Classic',
                'Zagreb', 'Zhuhai', 'Zhengzhou']
    for tour in tourlist:
        get_stats_per_tournament(dt_matches, type, tour)
    return

def get_handedness(dt_matches):
    dt_matches.loc[(dt_matches['winner_hand'] == dt_matches['loser_hand']), 'handedness'] = 1
    dt_matches.loc[((dt_matches['winner_hand'] == 'R') & (dt_matches['loser_hand'] == 'L')), 'handedness'] = 2
    dt_matches.loc[((dt_matches['winner_hand'] == 'L') & (dt_matches['loser_hand'] == 'R')), 'handedness'] = 3
    return dt_matches

def get_age_diff(dt_matches):
    dt_matches['age_dif'] = round(abs(dt_matches['winner_age'] - dt_matches['loser_age']))
    return dt_matches

def get_h2hforplayerA(dt_matches, playerA):
    """
    if name = 'Roger Federer' then the result ['Sergi Bruguera', 0, 1] means that
    Roger Federer had 0 wins over Bruguera and Sergi Bruguera had 1 win over Federer.
    """
    dt_matches = dt_matches[(dt_matches['winner_name'] == playerA) | (dt_matches['loser_name'] == playerA)]
    h2hs = {}
    for index, match in dt_matches.iterrows():
        if match['winner_name'] == playerA:
            if match['loser_name'] not in h2hs:
                h2hs[match['loser_name']] = {}
                h2hs[match['loser_name']]['l'] = 0
                h2hs[match['loser_name']]['w'] = 1
            else:
                h2hs[match['loser_name']]['w'] = h2hs[match['loser_name']]['w'] + 1
        elif match['loser_name'] == playerA:
            if match['winner_name'] not in h2hs:
                h2hs[match['winner_name']] = {}
                h2hs[match['winner_name']]['w'] = 0
                h2hs[match['winner_name']]['l'] = 1
            else:
                h2hs[match['winner_name']]['l'] = h2hs[match['winner_name']]['l'] + 1

    h2hlist = []
    for k, v in h2hs.items():
        h2hlist.append([k, v['w'], v['l']])

    if len(h2hlist) == 0:
        return ''
    else:
        return sorted(h2hlist, key=itemgetter(1, 2))
def get_h2hforplayerB(tuple, playerA, playerB):
    for item in tuple:
        if playerB in item:
            print('Player ' + playerA + ' has ' + str(item[1]) + ' wins over ' + playerB + ' and ' + str(item[2]) + ' losses.')
            return item[1], item[2]
def get_h2h(playerA, playerB, dt_matches):
    h2hList = get_h2hforplayerA(dt_matches, playerA)
    wins, losses = get_h2hforplayerB(h2hList, playerA, playerB)
    return wins, losses

def get_difference_in_ranking(dt_matches):
    dt_matches['rankingDifference'] = round(abs(dt_matches['winner_rank'] - dt_matches['loser_rank']))
    return dt_matches
def get_difference_in_ranking_points(dt_matches):
    dt_matches['rank_points_diff'] = round(abs(dt_matches['winner_rank_points'] - dt_matches['loser_rank_points']))
    return dt_matches

def k_factor(matches_played):
    K = 250
    offset = 5
    shape = 0.4
    return K/(matches_played + offset)**shape
def calc_exp_score(playerA_rating, playerB_rating):
    '''
    calculate the expected score of playerA
    expected score of playerB = 1 - expected score of playerA
    '''
    exp_score = 1/(1+(10**((playerB_rating - playerA_rating)/400)))
    return exp_score
def update_elo(old_elo, k, actual_score, expected_score):
    '''
    calculate new elo score
    '''
    new_elo = old_elo + k *(actual_score - expected_score)
    return new_elo
def get_Elo(dtP, type, now, score):
    player = DataFrame(dtP, columns=['player_id', 'player_name', 'ioc'])
    player['current_elo'] = Series(1500, index=player.index)
    player['last_tourney_date'] = Series('N/A', index=player.index)
    player['matches_played'] = Series(0, index=player.index)
    player['peak_elo'] = Series(1500, index=player.index)
    player['peak_elo_date'] = Series('N/A', index=player.index)
    #player.drop([0], axis=0, inplace=True)
    # Convert objects within DataFrame to numeric
    player = player._convert(numeric=True)
    # read through matches file for each year to update players data frame starting from current_year
    if type == 'atp':
        current_year = 2010
    else:
        current_year = 2016

    for i in range((now - current_year)+1):
        current_year_file_name = '/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/' + type + '_matches_' + str(current_year) + '[cleaned].csv'
        with open(current_year_file_name) as file:
            readCSV = csv.reader(file, delimiter=',')
            col_index = [1,6,8,16,24,25,26]
            all_matches = []
            for row in readCSV:
                match_info = []
                for i in col_index:
                    match_info.append(row[i])
                all_matches.append(match_info)

            # separate column names and match info
            header_info = all_matches[0]
            all_matches = all_matches[1:]

            # Create a dataframe to store match info
            matches = DataFrame(all_matches, columns=header_info)
            matches = matches._convert(numeric=True)

            # Sort matches dataframe by tourney_date and then by round
            sorter = ['RR', 'R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']
            matches['round'] = matches['round'].astype('category')
            matches['round'].cat.set_categories(sorter, inplace=True)
            matches = matches.sort_values(['tourney_date', 'round'])

            for index, row in matches.iterrows():
                winner_id = row['winner_id']
                loser_id = row['loser_id']
                tourney_date = row['tourney_date']
                index_winner = player[player['player_id'] == winner_id].index.tolist()
                index_loser = player[player['player_id'] == loser_id].index.tolist()
                old_elo_winner = player.loc[index_winner[0], 'current_elo']
                old_elo_loser = player.loc[index_loser[0], 'current_elo']
                exp_score_winner = calc_exp_score(old_elo_winner, old_elo_loser)
                exp_score_loser = 1 - exp_score_winner
                matches_played_winner = player.loc[index_winner[0], 'matches_played']
                matches_played_loser = player.loc[index_loser[0], 'matches_played']
                new_elo_winner = update_elo(old_elo_winner, k_factor(matches_played_winner), score, exp_score_winner)
                new_elo_loser = update_elo(old_elo_loser, k_factor(matches_played_loser), score - 1, exp_score_loser)
                player.loc[index_winner[0], 'current_elo'] = new_elo_winner
                player.loc[index_winner[0], 'last_tourney_date'] = tourney_date
                player.loc[index_winner[0], 'matches_played'] = player.loc[index_winner[0], 'matches_played'] + 1
                player.loc[index_loser[0], 'current_elo'] = new_elo_loser
                player.loc[index_loser[0], 'last_tourney_date'] = tourney_date
                player.loc[index_loser[0], 'matches_played'] = player.loc[index_loser[0], 'matches_played'] + 1
                if new_elo_winner > player.loc[index_winner[0], 'peak_elo']:
                    player.loc[index_winner[0], 'peak_elo'] = new_elo_winner
                    player.loc[index_winner[0], 'peak_elo_date'] = row['tourney_date']

            player.to_csv('/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/' + str(type) + '_' + str(current_year) + '_yr_end_elo_ranking.csv')
            current_year = current_year + 1
    return player

def get_winning_streak_till_today(dtM, player):
    dtM = dtM[(dtM['winner_name'] == player) | (dtM['loser_name'] == player)]
    dtM.sort_values(['tourney_date', 'match_num'],ascending=False, inplace=True)
    dtM = dtM[['tourney_id', 'tourney_name', 'tourney_date', 'winner_name']]

    streak = 0
    for i,row in dtM.iterrows():
        if row[3] == player:
            streak = streak + 1
        else:
            break
    return streak
def get_losing_streak_till_today(dtM, player):
    dtM = dtM[(dtM['winner_name'] == player) | (dtM['loser_name'] == player)]
    dtM.sort_values(['tourney_date', 'match_num'],ascending=False, inplace=True)
    dtM = dtM[['tourney_id', 'tourney_name', 'tourney_date', 'loser_name']]

    streak = 0
    for i, row in dtM.iterrows():
        if row[3] == player:
            streak = streak + 1
        else:
            break
    return streak
def get_weeks_inactive_till_today(dtM, player, now):
    dtM = dtM[(dtM['winner_name'] == player) | (dtM['loser_name'] == player)]
    dtM.sort_values(['tourney_date', 'match_num'],ascending=False, inplace=True)
    dtM = dtM[['tourney_id', 'tourney_name', 'tourney_date', 'match_num']]

    this_day = datetime.datetime.strptime(now, '%d/%m/%y %H:%M:%S')
    year_now = str(this_day)[0:4]
    month_now = str(this_day)[5:7]
    day_now = str(this_day)[8:10]

    for i, row in dtM.iterrows():
        last_day = row[2]
        break

    year_then = str(last_day)[0:4]
    month_then = str(last_day)[4:6]
    day_then = str(last_day)[6:8]

    start_date = datetime.date(int(year_now), int(month_now), int(day_now))
    start_date_monday = (start_date - datetime.timedelta(days=start_date.weekday()))

    end_date = datetime.date(int(year_then), int(month_then), int(day_then))
    num_of_weeks = math.ceil((end_date - start_date_monday).days / 7.0)

    return abs(num_of_weeks)

current_year = 2022
current_month = 5

# Read Files from ATP and WTA Matches
atpFiles_raw = glob.glob("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/ATP/atp_matches_" + "????.csv")
wtaFiles_raw = glob.glob("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/WTA/wta_matches_" + "????.csv")
atpPlayers_raw = pd.read_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/ATP/atp_players.csv")
wtaPlayers_raw = pd.read_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/WTA/wta_players.csv")

atpMatches, atpPlayers_r = get_data(atpFiles_raw, atpPlayers_raw)
wtaMatches, wtaPlayers_r = get_data(wtaFiles_raw, wtaPlayers_raw)
atpPlayers = get_players(atpMatches, 'atp', atpPlayers_r)
wtaPlayers = get_players(wtaMatches, 'wta', wtaPlayers_r)

a_surfaces = get_surfaces_together(atpMatches, 'atp')
a_players = pd.merge(left=atpPlayers, right=a_surfaces, right_on='player_name', left_on='player_name').fillna(0)
a_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_players[update].csv")
w_surfaces = get_surfaces_together(wtaMatches, 'wta')
w_players = pd.merge(left=wtaPlayers, right=w_surfaces, right_on='player_name', left_on='player_name').fillna(0)
w_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_players[update].csv")


a_matches = get_metrics(atpMatches, 'atp').fillna(0)
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[update].csv")
w_matches = get_metrics(wtaMatches, 'wta').fillna(0)
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[update].csv")


a_career = get_totalWinsLosses(atpMatches, 'atp', 'Career')
a_players = pd.merge(left=a_players, right=a_career, right_on='player_name', left_on='player_name').fillna(0)
a_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_players[update].csv")

w_career = get_totalWinsLosses(wtaMatches, 'wta', 'Career')
w_players = pd.merge(left=w_players, right=w_career, right_on='player_name', left_on='player_name').fillna(0)
w_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_players[update].csv")

a_matches = get_date(a_matches)
a_last_year = get_last_year(a_matches, current_year, current_month)
a_last_year = get_totalWinsLosses(a_last_year, 'atp', 'LastYear')
a_players = pd.merge(left=a_players, right=a_last_year, how='left', right_on='player_name', left_on='player_name').fillna(0)
a_last_semester = get_last_semester(a_matches, current_year, current_month)
a_last_semester = get_totalWinsLosses(a_last_semester, 'atp', 'LastSemester')
a_players = pd.merge(left=a_players, right=a_last_semester, how='left', right_on='player_name', left_on='player_name').fillna(0)
a_last_two_weeks = get_last_two_weeks(a_matches, '23/05/22 00:00:00')
a_last_two_weeks = get_totalWinsLosses(a_last_two_weeks, 'atp', 'LastTwoWeeks')
a_players = pd.merge(left=a_players, right=a_last_two_weeks,how='left', right_on='player_name', left_on='player_name').fillna(0)
a_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_players[update].csv")

w_matches = get_date(w_matches)
w_last_year = get_last_year(w_matches, current_year, current_month)
w_last_year = get_totalWinsLosses(w_last_year, 'wta', 'LastYear')
w_players = pd.merge(left=w_players, right=w_last_year, how='left', right_on='player_name', left_on='player_name').fillna(0)
w_last_semester = get_last_semester(w_matches, current_year, current_month)
w_last_semester = get_totalWinsLosses(w_last_semester, 'wta', 'LastSemester')
w_players = pd.merge(left=w_players, right=w_last_semester, how='left', right_on='player_name', left_on='player_name').fillna(0)
w_last_two_weeks = get_last_two_weeks(w_matches, '23/05/22 00:00:00')
w_last_two_weeks = get_totalWinsLosses(w_last_two_weeks, 'wta', 'LastTwoWeeks')
w_players = pd.merge(left=w_players, right=w_last_two_weeks,how='left', right_on='player_name', left_on='player_name').fillna(0)
w_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_players[update].csv")

a_matches = get_home_advantage(a_matches, 'atp')
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[update].csv")
w_matches = get_home_advantage(w_matches, 'wta')
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[update].csv")

get_tour(atpMatches, 'atp')
get_tour(wtaMatches, 'wta')

a_matches = get_handedness(a_matches)
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[update].csv")
w_matches = get_handedness(w_matches)
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[update].csv")

a_matches = get_age_diff(a_matches)
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[update].csv")
w_matches = get_age_diff(w_matches)
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[update].csv")

get_h2h('Roger Federer', 'Stefanos Tsitsipas', a_matches)

a_matches = get_difference_in_ranking(a_matches)
a_matches = get_difference_in_ranking_points(a_matches)
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[update].csv")
w_matches = get_difference_in_ranking(w_matches)
w_matches = get_difference_in_ranking_points(w_matches)
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[update].csv")

a_elo = get_Elo(a_players, 'atp', 2022, 1)
a_players = pd.merge(left=a_players, right=a_elo, how='left', right_on='player_name', left_on='player_name').fillna(0)
a_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_players[update].csv")

w_elo = get_Elo(w_players, 'wta', 2022, 1)
w_players = pd.merge(left=w_players, right=w_elo, how='left', right_on='player_name', left_on='player_name').fillna(0)
w_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_players[update].csv")

winning = get_winning_streak_till_today(a_matches, 'Stefanos Tsitsipas')
losing = get_losing_streak_till_today(a_matches, 'Stefanos Tsitsipas')
inactive = get_weeks_inactive_till_today(a_matches, 'Stefanos Tsitsipas', '23/05/22 00:00:00')


############## AT LAST
#### we are going to have 3 general files
#### matches, stats, players

a_stats = a_matches[['tourney_id', 'location_country', 'surface', 'tourney_level', 'tourney_date',
                     'year', 'month', 'date', 'match_num', 'best_of',
                     'winner_id', 'winner_name', 'winner_age',
                     'home_advantage', 'handedness',
                     'loser_id', 'loser_name', 'loser_age', 'age_dif',
                     'score', 'round', 'minutes',
                     'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_1stS(%)', 'w_2ndIn',
                     'w_2ndWon', 'w_1st_svpt(%)', 'w_2nd_svpt(%)', 'w_SvGms',
                     'w_1stS_rtpWon', 'w_2ndS_rtpWon', 'w_1stS_rtpWon(%)', 'w_2ndS_rtpWon(%)',
                     'w_bpSaved', 'w_bpFaced', 'w_bpWon(%)', 'w_bpWon', 'w_bpConv(%)',
                     'winner_rank', 'winner_rank_points',
                     'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_1stS(%)', 'l_2ndIn',
                     'l_2ndWon', 'l_1st_svpt(%)', 'l_2nd_svpt(%)', 'l_SvGms',
                     'l_1stS_rtpWon', 'l_2ndS_rtpWon', 'l_1stS_rtpWon(%)', 'l_2ndS_rtpWon(%)',
                     'l_bpSaved', 'l_bpFaced', 'l_bpWon(%)', 'l_bpWon', 'l_bpConv(%)',
                     'loser_rank', 'loser_rank_points', 'rankingDifference', 'rank_points_diff']]
a_stats.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_stats[final].csv")

w_stats = w_matches[['tourney_id', 'location_country', 'surface', 'tourney_level', 'tourney_date',
                     'year', 'month', 'date', 'match_num', 'best_of',
                     'winner_id', 'winner_name', 'winner_age',
                     'home_advantage', 'handedness',
                     'loser_id', 'loser_name', 'loser_age', 'age_dif',
                     'score', 'round', 'minutes',
                     'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_1stS(%)', 'w_2ndIn',
                     'w_2ndWon', 'w_1st_svpt(%)', 'w_2nd_svpt(%)', 'w_SvGms',
                     'w_1stS_rtpWon', 'w_2ndS_rtpWon', 'w_1stS_rtpWon(%)', 'w_2ndS_rtpWon(%)',
                     'w_bpSaved', 'w_bpFaced', 'w_bpWon(%)', 'w_bpWon', 'w_bpConv(%)',
                     'winner_rank', 'winner_rank_points',
                     'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_1stS(%)', 'l_2ndIn',
                     'l_2ndWon', 'l_1st_svpt(%)', 'l_2nd_svpt(%)', 'l_SvGms',
                     'l_1stS_rtpWon', 'l_2ndS_rtpWon', 'l_1stS_rtpWon(%)', 'l_2ndS_rtpWon(%)',
                     'l_bpSaved', 'l_bpFaced', 'l_bpWon(%)', 'l_bpWon', 'l_bpConv(%)',
                     'loser_rank', 'loser_rank_points', 'rankingDifference', 'rank_points_diff']]
w_stats.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_stats[final].csv")

a_matches = a_matches[['tourney_id', 'tourney_name', 'location_country', 'surface', 'tourney_level',
                       'tourney_date',
                       'year', 'month', 'date', 'match_num', 'winner_id', 'winner_name', 'winner_rank',
                       'winner_rank_points', 'loser_id', 'loser_name', 'loser_rank', 'loser_rank_points',
                       'score', 'round', 'minutes']]
a_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_matches[final].csv")

w_matches = w_matches[['tourney_id', 'tourney_name', 'location_country', 'surface', 'tourney_level',
                       'tourney_date',
                       'year', 'month', 'date', 'match_num', 'winner_id', 'winner_name', 'winner_rank',
                       'winner_rank_points', 'loser_id', 'loser_name', 'loser_rank', 'loser_rank_points',
                       'score', 'round', 'minutes']]
w_matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_matches[final].csv")

a_players = a_players[['player_id_x', 'player_name', 'hand', 'dob', 'ioc_x', 'height', 'total_matches',
                       'wins_Hard', 'losses_Hard', 'Hard(%)', 'wins_Grass', 'losses_Grass', 'Grass(%)',
                       'wins_Clay', 'losses_Clay', 'Clay(%)', 'wins_Carpet', 'losses_Carpet', 'Carpet(%)',
                       'Wins_Career', 'Losses_Career', 'Matches_Career', 'Wins(%)_Career', 'Finals_Career',
                       'Titles_Career', 'Wins_LastYear', 'Losses_LastYear', 'Matches_LastYear',
                       'Wins(%)_LastYear', 'Finals_LastYear', 'Titles_LastYear', 'Wins_LastSemester',
                       'Losses_LastSemester', 'Matches_LastSemester', 'Wins(%)_LastSemester',
                       'Finals_LastSemester', 'Titles_LastSemester', 'Wins_LastTwoWeeks', 'Losses_LastTwoWeeks',
                       'Matches_LastTwoWeeks', 'Wins(%)_LastTwoWeeks', 'Finals_LastTwoWeeks', 'Titles_LastTwoWeeks',
                       'current_elo', 'last_tourney_date', 'matches_played', 'peak_elo', 'peak_elo_date']]
a_players.rename(columns={'player_id_x': 'player_id', 'ioc_x': 'ioc'}, inplace=True)
a_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/atp_players[final].csv")


w_players = w_players[['player_id_x', 'player_name', 'hand', 'dob', 'ioc_x', 'height', 'total_matches',
                       'wins_Hard', 'losses_Hard', 'Hard(%)', 'wins_Grass', 'losses_Grass', 'Grass(%)',
                       'wins_Clay', 'losses_Clay', 'Clay(%)', 'wins_Carpet', 'losses_Carpet', 'Carpet(%)',
                       'Wins_Career', 'Losses_Career', 'Matches_Career', 'Wins(%)_Career', 'Finals_Career',
                       'Titles_Career', 'Wins_LastYear', 'Losses_LastYear', 'Matches_LastYear',
                       'Wins(%)_LastYear', 'Finals_LastYear', 'Titles_LastYear', 'Wins_LastSemester',
                       'Losses_LastSemester', 'Matches_LastSemester', 'Wins(%)_LastSemester',
                       'Finals_LastSemester', 'Titles_LastSemester', 'Wins_LastTwoWeeks', 'Losses_LastTwoWeeks',
                       'Matches_LastTwoWeeks', 'Wins(%)_LastTwoWeeks', 'Finals_LastTwoWeeks', 'Titles_LastTwoWeeks',
                       'current_elo', 'last_tourney_date', 'matches_played', 'peak_elo', 'peak_elo_date']]
w_players.rename(columns={'player_id_x': 'player_id', 'ioc_x': 'ioc'}, inplace=True)
w_players.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/wta_players[final].csv")
