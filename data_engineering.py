import os
import numpy as np
import pandas as pd
import math
import datetime
from datetime import datetime, timedelta
import statistics

######## HELPER FUNCTIONS ########

# H.1
def helper(df, column):
    df[column] = df[column].replace([''], 0)
    df.loc[df[column] != 0, column] = df[column] - 1
    return

# H.2.1
def util(df, quote):
    if df.shape[0] == 0:
        df['min'][0] = 0
        df['max'][0] = 0
        df.at[0, quote] = 0
    else:
        if df['min_A'][0] < df['min_B'][0]:
            df['min'][0] = df['min_A'][0]
        else:
            df['min'][0] = df['min_B'][0]
        if df['max_A'][0] > df['max_B'][0]:
            df['max'][0] = df['max_A'][0]
        else:
            df['max'][0] = df['max_B'][0]

        if df['max_A'][0] <= df['min_A'][0]:
            df['min'][0] = df['max_A'][0]
        if df['max_B'][0] <= df['min_B'][0]:
            df['min'][0] = df['max_B'][0]

        if df['max'][0] == 0 & df['min'][0] == 0:
            df[quote][0] = 0
        else:
            df[quote][0] = df['max'][0] - df['min'][0] + 1
    #print(df)
    return df

# H.2.2
def helper_get_dataset(df, flag, period, winner, loser):
    df_winners = df.groupby('A_id').agg({'A_' + str(flag) + '_career': ['min', 'max']})
    df_winners.rename(columns={'min': 'min_A', 'max': 'max_A'}, inplace=True)
    df_losers = df.groupby('B_id').agg({'B_' + str(flag) + '_career': ['min', 'max']})
    df_losers.rename(columns={'min': 'min_B', 'max': 'max_B'}, inplace=True)
    concat = pd.concat([df_winners, df_losers], axis=1)
    concat.columns = ['min_A', 'max_A', 'min_B', 'max_B']
    concat.index.name = 'player_id'
    concat.reset_index(level=0, inplace=True)
    concat['min_A'].fillna(10000, inplace=True)
    concat['min_B'].fillna(10000, inplace=True)
    concat['max_A'].fillna(0, inplace=True)
    concat['max_B'].fillna(0, inplace=True)
    concat = concat.sort_values(['player_id'])
    concat[['min_A', 'min_B', 'max_A', 'max_B']] = concat[['min_A', 'min_B', 'max_A', 'max_B']].astype(int)
    concat['min'] = ""
    concat['max'] = ""
    concat[str(flag) + '_' + str(period)] = ""

    winner_df = concat.loc[concat['player_id'] == winner]
    winner_df.reset_index(level=0, inplace=True)
    loser_df = concat.loc[concat['player_id'] == loser]
    loser_df.reset_index(level=0, inplace=True)

    winner_df = util(winner_df, str(flag) + '_' + str(period))
    loser_df = util(loser_df, str(flag) + '_' + str(period))
    return winner_df, loser_df

# H.3
K = 32  # The k-factor in the Elo rating system
def helper_calculate_elo(rating1, rating2, score1, score2):
    """
    Calculates the new Elo ratings for two players based on their current ratings and the outcome of a match.

    Parameters:
    - rating1: The current Elo rating of player 1
    - rating2: The current Elo rating of player 2
    - score1: The number of wins for player 1 (1 for a win, 0 for a loss)
    - score2: The number of wins for player 2 (1 for a win, 0 for a loss)

    Returns:
    - A tuple containing the new ratings for player 1 and player 2, respectively.
    """
    # Calculate the expected score for each player
    exp1 = 1 / (1 + math.pow(10, (rating2 - rating1) / 400))
    exp2 = 1 / (1 + math.pow(10, (rating1 - rating2) / 400))

    # Calculate the new ratings
    new_rating1 = rating1 + K * (score1 - exp1)
    new_rating2 = rating2 + K * (score2 - exp2)

    return new_rating1, new_rating2

# H.4
def winning_streak(df, player, ID):
    win_streak = 0
    for i, row in df.iterrows():
        if row[ID] == player:
            win_streak = win_streak + 1
        else:
            break
    return win_streak

# H.5
def losing_streak(df, player, ID):
    los_streak = 0
    for i, row in df.iterrows():
        if row[ID] == player:
            los_streak = los_streak + 1
        else:
            break
    return los_streak

# H.6
def days_inactive(last_date, now_date):
    d1 = datetime.strptime(now_date, '%Y%m%d')
    d2 = datetime.strptime(last_date, '%Y%m%d')
    delta = d1 - d2
    return delta.days

######## UTIL FUNCTIONS ########

# 1. Home Advantage Effect
def get_home_advantage(row):
    """
    Home Advantage Effect plays a significant and quantitatively important role.
    This effect is strongest in matches between highly skilled opponents,
    and absent when we consider a between two weak players.
    See Paper: 2011_[Home Advantage in professional tennis]
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    if row['location'] == row['A_ioc']:
        return 1
    elif row['location'] == row['B_ioc']:
        return -1
    else:
        return 0

# 2. Rankings calculated by logarithms with base 2
def compute_log_rankings(row):
    """
    The model with difference of the logarithm of World Ranks provides a much better
    fit than difference of absolute levels of World Ranks.
    logWR ~ logWRa - logWRb
    The rankings are expressed on a log-scale since the differences in the
    "quality" of the players are not linear. The ranking difference is more critical
    for the top-ranked field and the log-transformation expresses this. The higher the
    difference in ranking between two players, the higher the probability of the favorite
    to win.
    The rank points difference in a log scale could contain additional information, since
    it provides a more fine-grained view of the strength difference between the players than
    the rankings alone.
    See Paper: 2011_[Home Advantage in professional tennis]
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    row['A_rank_log'] = math.log2(row['A_rank'])
    row['B_rank_log'] = math.log2(row['B_rank'])
    row['A_rank_points_log'] = math.log2(row['A_rank_points'])
    row['B_rank_points_log'] = math.log2(row['B_rank_points'])
    return row

# 3. Quality of the Match
def get_match_quality(df):
    """
    Quality of the Match is measured by the sum of the Rankings of both players
    See Paper: 2011_[Home Advantage in professional tennis]
    """
    df['match_quality1'] = df['A_rank'] + df['B_rank']
    df['match_quality2'] = df['A_rank_log'] + df['B_rank_log']
    return df

# 4. Surface Information 1
def combine_surface_court(row):
    surface_value = str(row['surface'])
    court_value = str(row['court'])
    row['surface_court'] = str(surface_value + '_' + court_value)
    return row

# 5. Betting Statistics
def betting_features(df):
    """
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    df[['A_B365', 'B_B365']].replace({971: 9.71, 967: 9.67, 67.0: 6.7}, inplace=True)

    df['B365_ratio'] = df['A_B365'] / df['B_B365']

    df['A_spread'] = 100 * (abs(df['A_Max'] - df['A_Avg']) / ((df['A_Max'] + df['A_Avg']) / 2))
    df['B_spread'] = 100 * (abs(df['B_Max'] - df['B_Avg']) / ((df['B_Max'] + df['B_Avg']) / 2))

    return df

# 6. Career Statistics
def career_features(df):
    """
    Calculate career statistics (since the year of the first used dataset)
    Wins, Losses, Matches, Titles of each player
    Better record indicates better player
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]
        winner = df['A_id'][num]
        winner_size = temp_df.groupby('A_id').size()

        loser = df['B_id'][num]
        loser_size = temp_df.groupby('B_id').size()

        finals = temp_df[(temp_df['round'] == 'The Final')]
        titles_size = finals.groupby('A_id').size()

        career = pd.DataFrame({'wins_career': winner_size, 'losses_career': loser_size}).fillna(0)
        career[['wins_career', 'losses_career']] = career[['wins_career', 'losses_career']].astype(int)
        career = career.reindex(['wins_career', 'losses_career'], axis=1)
        career['matches_career'] = career['wins_career'] + career['losses_career']
        career = career.join(pd.DataFrame(titles_size, columns=['titles_career'], )).fillna(0)
        career['titles_career'] = career['titles_career'].astype(int)
        career.index.name = 'player_id'
        career.reset_index(level=0, inplace=True)

        winner_career_df = career.loc[career['player_id'] == winner]
        if winner_career_df.shape[0] != 0:
            winner_career_df.reset_index(level=0, inplace=True)
            df.at[num, 'A_wins_career'] = winner_career_df['wins_career'][0] - 1
            df.at[num, 'A_losses_career'] = winner_career_df['losses_career'][0]
            df.at[num, 'A_matches_career'] = winner_career_df['matches_career'][0] - 1
            df.at[num, 'A_titles_career'] = winner_career_df['titles_career'][0] - 1

        loser_career_df = career.loc[career['player_id'] == loser]
        if loser_career_df.shape[0] != 0:
            loser_career_df.reset_index(level=0, inplace=True)
            df.at[num, 'B_wins_career'] = loser_career_df['wins_career'][0]
            df.at[num, 'B_losses_career'] = loser_career_df['losses_career'][0] - 1
            df.at[num, 'B_matches_career'] = loser_career_df['matches_career'][0] - 1
            df.at[num, 'B_titles_career'] = loser_career_df['titles_career'][0]

    df[['A_wins_career', 'A_losses_career', 'A_matches_career', 'A_titles_career',
        'B_wins_career', 'B_losses_career', 'B_matches_career', 'B_titles_career']].fillna(0, inplace=True)
    return df

# 7. Yearly Statistics
def yearly_features(df):
    """
    Calculate yearly statistics ( for a 12-month period )
    Wins, Losses, Matches, Finals, Titles of each player
    Calculate the Percentage of Games Won over Games Played over the
    past 12 months
    Better record indicates better player or a win streak
    Games Played over the past 12 months shows the Health
    Condition of the player
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """
    # there was an error. so I do the below:
    df.index.name = 'player_id'
    df.reset_index(level=0, inplace=True)
    df.drop(columns=['player_id'], inplace=True)

    #months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        if df['year'][num] == 2010:
            df.at[num, 'A_wins_year'] = 0
            df.at[num, 'A_losses_year'] = 0
            df.at[num, 'A_matches_year'] = 0
            df.at[num, 'A_titles_year'] = 0

            df.at[num, 'B_wins_year'] = 0
            df.at[num, 'B_losses_year'] = 0
            df.at[num, 'B_matches_year'] = 0
            df.at[num, 'B_titles_year'] = 0

        else:
            winner = df['A_id'][num]
            loser = df['B_id'][num]

            temp_df = df[df['match_index'] <= num]

            # find date before one year
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            one_year_ago = date_object - timedelta(days=365)
            new_date = str(one_year_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find the starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                day = 1
                month = 1
                year = year + 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 23):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]
            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            lastyear = df.iloc[starting_index:num]

            plA = lastyear.loc[(lastyear['A_id'] == winner) | (lastyear['B_id'] == winner)]
            if plA.shape[0] == 0:
                df.at[num, 'A_wins_year'] = 0
                df.at[num, 'A_losses_year'] = 0
                df.at[num, 'A_matches_year'] = 0
                df.at[num, 'A_titles_year'] = 0
            else:
                # the first row that player A appears
                first_index_A = plA.index[0]
                # the last row that player B appears
                last_index_A = plA.index[-1]

                df.at[num, 'A_wins_year'] = df['A_wins_career'][last_index_A] - df['A_wins_career'][first_index_A]
                df.at[num, 'A_losses_year'] = df['A_losses_career'][last_index_A] - df['A_losses_career'][first_index_A]
                df.at[num, 'A_matches_year'] = df['A_matches_career'][last_index_A] - df['A_matches_career'][first_index_A]
                df.at[num, 'A_titles_year'] = df['A_titles_career'][last_index_A] - df['A_titles_career'][first_index_A]

            plB = lastyear.loc[(lastyear['A_id'] == loser) | (lastyear['B_id'] == loser)]
            if plB.shape[0] == 0:
                df.at[num, 'B_wins_year'] = 0
                df.at[num, 'B_losses_year'] = 0
                df.at[num, 'B_matches_year'] = 0
                df.at[num, 'B_titles_year'] = 0
            else:
                # the first row that player A appears
                first_index_B = plB.index[0]
                # the last row that player B appears
                last_index_B = plB.index[-1]

                df.at[num, 'B_wins_year'] = df['B_wins_career'][last_index_B] - df['B_wins_career'][first_index_B]
                df.at[num, 'B_losses_year'] = df['B_losses_career'][last_index_B] - df['B_losses_career'][first_index_B]
                df.at[num, 'B_matches_year'] = df['B_matches_career'][last_index_B] - df['B_matches_career'][first_index_B]
                df.at[num, 'B_titles_year'] = df['B_titles_career'][last_index_B] - df['B_titles_career'][first_index_B]

    df['A_matches_year_per'] = (df['A_wins_year'] / df['A_matches_year'])
    df['B_matches_year_per'] = (df['B_wins_year'] / df['B_matches_year'])

    return df

# 8. Semesterly Statistics
def semester_features(df):
    """
    Calculate yearly statistics ( for a 12-month period )
    Wins, Losses, Matches, Finals, Titles of each player
    See Paper: 2020_[Predicting Tennis Matches Using Machine Learning]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        if (df['year'][num] == 2010) and (df['month'][num] <= 6):
            df.at[num, 'A_wins_semester'] = 0
            df.at[num, 'A_losses_semester'] = 0
            df.at[num, 'A_matches_semester'] = 0
            df.at[num, 'A_titles_semester'] = 0

            df.at[num, 'B_wins_semester'] = 0
            df.at[num, 'B_losses_semester'] = 0
            df.at[num, 'B_matches_semester'] = 0
            df.at[num, 'B_titles_semester'] = 0
        else:
            winner = df['A_id'][num]
            loser = df['B_id'][num]

            temp_df = df[df['match_index'] <= num]

            # find date before six months ( one semester )
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            six_months_ago = date_object - timedelta(days=182)
            new_date = str(six_months_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find the starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                day = 1
                month = 1
                year = year + 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 23):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]
            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            lastsemester = df.iloc[starting_index:num]

            plA = lastsemester.loc[(lastsemester['A_id'] == winner) | (lastsemester['B_id'] == winner)]
            if plA.shape[0] == 0:
                df.at[num, 'A_wins_semester'] = 0
                df.at[num, 'A_losses_semester'] = 0
                df.at[num, 'A_matches_semester'] = 0
                df.at[num, 'A_titles_semester'] = 0
            else:
                # the first row that player A appears
                first_index_A = plA.index[0]
                # the last row that player A appears
                last_index_A = plA.index[-1]

                df.at[num, 'A_wins_semester'] = df['A_wins_career'][last_index_A] - df['A_wins_career'][first_index_A]
                df.at[num, 'A_losses_semester'] = df['A_losses_career'][last_index_A] - df['A_losses_career'][first_index_A]
                df.at[num, 'A_matches_semester'] = df['A_matches_career'][last_index_A] - df['A_matches_career'][first_index_A]
                df.at[num, 'A_titles_semester'] = df['A_titles_career'][last_index_A] - df['A_titles_career'][first_index_A]

            plB = lastsemester.loc[(lastsemester['A_id'] == loser) | (lastsemester['B_id'] == loser)]
            if plB.shape[0] == 0:
                df.at[num, 'B_wins_semester'] = 0
                df.at[num, 'B_losses_semester'] = 0
                df.at[num, 'B_matches_semester'] = 0
                df.at[num, 'B_titles_semester'] = 0
            else:
                # the first row that player B appears
                first_index_B = plB.index[0]
                # the last row that player B appears
                last_index_B = plB.index[-1]

                df.at[num, 'B_wins_semester'] = df['B_wins_career'][last_index_B] - df['B_wins_career'][first_index_B]
                df.at[num, 'B_losses_semester'] = df['B_losses_career'][last_index_B] - df['B_losses_career'][first_index_B]
                df.at[num, 'B_matches_semester'] = df['B_matches_career'][last_index_B] - df['B_matches_career'][first_index_B]
                df.at[num, 'B_titles_semester'] = df['B_titles_career'][last_index_B] - df['B_titles_career'][first_index_B]

    return df

# 9. Recent Matches Statistics
def recent_features(df):
    """
    Calculate Recent Statistics from last two weeks
    Calculate Wins, Losses, Matches
    See Paper: 2020_[Predicting Tennis Matches Using Machine Learning]
    """
    df.index.name = 'player_id'
    df.reset_index(level=0, inplace=True)
    df.drop(columns=['player_id'], inplace=True)

    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
          print('Working on it (', num, ')..')

        if (df['year'][num] == 2010) and (df['month'][num] == 1) and (df['day'][num] < 18):
            df.at[num, 'A_wins_recent'] = 0
            df.at[num, 'A_losses_recent'] = 0
            df.at[num, 'A_matches_recent'] = 0
            df.at[num, 'A_titles_recent'] = 0

            df.at[num, 'B_wins_recent'] = 0
            df.at[num, 'B_losses_recent'] = 0
            df.at[num, 'B_matches_recent'] = 0
            df.at[num, 'B_titles_recent'] = 0
        else:
            winner = df['A_id'][num]
            loser = df['B_id'][num]

            temp_df = df[df['match_index'] <= num]

            # find date before 15 days
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            two_weeks_ago = date_object - timedelta(days=15)
            new_date = str(two_weeks_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find the starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 17):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]

            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            recent = df.iloc[starting_index:num]

            plA = recent.loc[(recent['A_id'] == winner) | (recent['B_id'] == winner)]
            if plA.shape[0] == 0:
                df.at[num, 'A_wins_recent'] = 0
                df.at[num, 'A_losses_recent'] = 0
                df.at[num, 'A_matches_recent'] = 0
                df.at[num, 'A_titles_recent'] = 0

            else:
                # the first row that player A appears
                first_index_A = plA.index[0]
                # the last row that player B appears
                last_index_A = plA.index[-1]

                df.at[num, 'A_wins_recent'] = df['A_wins_career'][last_index_A] - df['A_wins_career'][first_index_A]
                df.at[num, 'A_losses_recent'] = df['A_losses_career'][last_index_A] - df['A_losses_career'][first_index_A]
                df.at[num, 'A_matches_recent'] = df['A_matches_career'][last_index_A] - df['A_matches_career'][first_index_A]
                df.at[num, 'A_titles_recent'] = df['A_titles_career'][last_index_A] - df['A_titles_career'][first_index_A]

            plB = recent.loc[(recent['A_id'] == loser) | (recent['B_id'] == loser)]
            if plB.shape[0] == 0:
                df.at[num, 'B_wins_recent'] = 0
                df.at[num, 'B_losses_recent'] = 0
                df.at[num, 'B_matches_recent'] = 0
                df.at[num, 'B_titles_recent'] = 0
            else:
                # the first row that player A appears
                first_index_B = plB.index[0]
                # the last row that player B appears
                last_index_B = plB.index[-1]

                df.at[num, 'B_wins_recent'] = df['B_wins_career'][last_index_B] - df['B_wins_career'][first_index_B]
                df.at[num, 'B_losses_recent'] = df['B_losses_career'][last_index_B] - df['B_losses_career'][first_index_B]
                df.at[num, 'B_matches_recent'] = df['B_matches_career'][last_index_B] - df['B_matches_career'][first_index_B]
                df.at[num, 'B_titles_recent'] = df['B_titles_career'][last_index_B] - df['B_titles_career'][first_index_B]
    return df

# 10. Surface Information 2
def get_surface_features(df):
    """
    Some players are better at particular courts
    Calculate Wins, Losses, Matches, Finals and Titles per Surface
    Calculate the Percentage of Games Won on the same type of surface
    Calculate the Surface Advantage
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    surfaces_list = ['Hard_Outdoor', 'Hard_Indoor', 'Grass_Outdoor', 'Clay_Outdoor', 'Clay_Indoor']
    for surface in surfaces_list:
        print(surface)
        df_surface = df[(df['surface_court'] == surface)]
        size = df_surface.shape[0]

        df_surface.index.name = 'i'
        df_surface.reset_index(level=0, inplace=True)
        df_surface.index.name = 'surface_index'
        df_surface.reset_index(level=0, inplace=True)

        for num in range(0, size):
            if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                       11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                       21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
                print('Working on it (', num, ')..')
            temp_df = df_surface[df_surface['surface_index'] <= num]

            winner = df['A_id'][num]
            winner_size = temp_df.groupby('A_id').size()

            loser = df['B_id'][num]
            loser_size = temp_df.groupby('B_id').size()

            finals = temp_df[(temp_df['round'] == 'The Final')]
            titles_size = finals.groupby('A_id').size()

            surface_df = pd.DataFrame({'wins_' + str(surface): winner_size, 'losses_' + str(surface): loser_size}).fillna(0)
            surface_df[['wins_' + str(surface), 'losses_' + str(surface)]] = surface_df[['wins_' + str(surface), 'losses_' + str(surface)]].astype(int)
            surface_df = surface_df.reindex(['wins_' + str(surface), 'losses_' + str(surface)], axis=1)
            surface_df['matches_' + str(surface)] = surface_df['wins_' + str(surface)] + surface_df['losses_' + str(surface)]
            surface_df = surface_df.join(pd.DataFrame(titles_size, columns=['titles_' + str(surface)], )).fillna(0)
            surface_df['titles_' + str(surface)] = surface_df['titles_' + str(surface)].astype(int)
            surface_df.index.name = 'player_id'
            surface_df.reset_index(level=0, inplace=True)

            winner_df = surface_df.loc[surface_df['player_id'] == winner]

            if winner_df.shape[0] != 0:
                winner_df.reset_index(level=0, inplace=True)
                df.at[num, 'A_wins_' + str(surface)] = winner_df['wins_' + str(surface)][0] - 1
                df.at[num, 'A_losses_' + str(surface)] = winner_df['losses_' + str(surface)][0]
                df.at[num, 'A_matches_' + str(surface)] = winner_df['matches_' + str(surface)][0] - 1
                df.at[num, 'A_titles_' + str(surface)] = winner_df['titles_' + str(surface)][0] - 1
            else:
                df.at[num, 'A_wins_' + str(surface)] = 0
                df.at[num, 'A_losses_' + str(surface)] = 0
                df.at[num, 'A_matches_' + str(surface)] = 0
                df.at[num, 'A_titles_' + str(surface)] = 0

            loser_df = surface_df.loc[surface_df['player_id'] == loser]

            if loser_df.shape[0] != 0:
                loser_df.reset_index(level=0, inplace=True)
                df.at[num, 'B_wins_' + str(surface)] = loser_df['wins_' + str(surface)][0]
                df.at[num, 'B_losses_' + str(surface)] = loser_df['losses_' + str(surface)][0] - 1
                df.at[num, 'B_matches_' + str(surface)] = loser_df['matches_' + str(surface)][0] - 1
                df.at[num, 'B_titles_' + str(surface)] = loser_df['titles_' + str(surface)][0]
            else:
                df.at[num, 'B_wins_' + str(surface)] = 0
                df.at[num, 'B_losses_' + str(surface)] = 0
                df.at[num, 'B_matches_' + str(surface)] = 0
                df.at[num, 'B_titles_' + str(surface)] = 0

    return df

# 11. Surface Information 3
def calculate_per_surface(df):
    df['A_matches_per_surface'] = df['A_matches_Hard_Outdoor'] + df['A_matches_Hard_Indoor'] + df['A_matches_Grass_Outdoor'] + df['A_matches_Clay_Outdoor'] + df['A_matches_Clay_Indoor']
    df['A_wins_per_surface'] = df['A_wins_Hard_Outdoor'] + df['A_wins_Hard_Indoor'] + df['A_wins_Grass_Outdoor'] + df['A_wins_Clay_Outdoor'] + df['A_wins_Clay_Indoor']
    df['A_losses_per_surface'] = df['A_losses_Hard_Outdoor'] + df['A_losses_Hard_Indoor'] + df['A_losses_Grass_Outdoor'] + df['A_losses_Clay_Outdoor'] + df['A_losses_Clay_Indoor']
    df['A_titles_per_surface'] = df['A_titles_Hard_Outdoor'] + df['A_titles_Hard_Indoor'] + df['A_titles_Grass_Outdoor'] + df['A_titles_Clay_Outdoor'] + df['A_titles_Clay_Indoor']

    df['B_matches_per_surface'] = df['B_matches_Hard_Outdoor'] + df['B_matches_Hard_Indoor'] + df['B_matches_Grass_Outdoor'] + df['B_matches_Clay_Outdoor'] + df['B_matches_Clay_Indoor']
    df['B_wins_per_surface'] = df['B_wins_Hard_Outdoor'] + df['B_wins_Hard_Indoor'] + df['B_wins_Grass_Outdoor'] + df['B_wins_Clay_Outdoor'] + df['B_wins_Clay_Indoor']
    df['B_losses_per_surface'] = df['B_losses_Hard_Outdoor'] + df['B_losses_Hard_Indoor'] + df['B_losses_Grass_Outdoor'] + df['B_losses_Clay_Outdoor'] + df['B_losses_Clay_Indoor']
    df['B_titles_per_surface'] = df['B_titles_Hard_Outdoor'] + df['B_titles_Hard_Indoor'] + df['B_titles_Grass_Outdoor'] + df['B_titles_Clay_Outdoor'] + df['B_titles_Clay_Indoor']

    df['A_surface_per'] = (df['A_wins_per_surface'] / df['A_matches_per_surface'])
    df['B_surface_per'] = (df['B_wins_per_surface'] / df['B_matches_per_surface'])

    df.drop(columns=['A_wins_Hard_Outdoor', 'A_losses_Hard_Outdoor', 'A_matches_Hard_Outdoor', 'A_titles_Hard_Outdoor',
                     'B_wins_Hard_Outdoor', 'B_losses_Hard_Outdoor', 'B_matches_Hard_Outdoor', 'B_titles_Hard_Outdoor',
                     'A_wins_Hard_Indoor', 'A_losses_Hard_Indoor', 'A_matches_Hard_Indoor', 'A_titles_Hard_Indoor',
                     'B_wins_Hard_Indoor', 'B_losses_Hard_Indoor', 'B_matches_Hard_Indoor', 'B_titles_Hard_Indoor',
                     'A_wins_Grass_Outdoor', 'A_losses_Grass_Outdoor', 'A_matches_Grass_Outdoor', 'A_titles_Grass_Outdoor',
                     'B_wins_Grass_Outdoor', 'B_losses_Grass_Outdoor', 'B_matches_Grass_Outdoor', 'B_titles_Grass_Outdoor',
                     'A_wins_Clay_Outdoor', 'A_losses_Clay_Outdoor', 'A_matches_Clay_Outdoor',  'A_titles_Clay_Outdoor',
                     'B_wins_Clay_Outdoor', 'B_losses_Clay_Outdoor', 'B_matches_Clay_Outdoor', 'B_titles_Clay_Outdoor',
                     'A_wins_Clay_Indoor', 'A_losses_Clay_Indoor', 'A_matches_Clay_Indoor', 'A_titles_Clay_Indoor',
                     'B_wins_Clay_Indoor', 'B_losses_Clay_Indoor', 'B_matches_Clay_Indoor', 'B_titles_Clay_Indoor'],
            inplace=True)
    return df

# 12. Tournament Statistics
def tournament_features(df):
    """
    Calculate tournament statistics ( for lifetime period )
    Wins, Losses, Matches, Titles of each player
    Calculate the Percentage of Games Won in the same tournament
    Some players play better in certain tournaments
    Previous success in a tournament may make a player more determined
    in future editions of the same tournament.
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    See Paper: 2020_[Predicting Tennis Matches Using Machine Learning]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]

        winner = df['A_id'][num]
        loser = df['B_id'][num]

        A_tour_wins = temp_df.loc[(temp_df['A_id'] == winner) & (temp_df['tourney_id'] == temp_df['tourney_id'][num])]
        A_tour_losses = temp_df.loc[(temp_df['B_id'] == winner) & (temp_df['tourney_id'] == temp_df['tourney_id'][num])]
        A_tour_titles = A_tour_wins.loc[A_tour_wins['round'] == 'The Final']

        if A_tour_wins.shape[0] == 0:
            A_wins = 0
        else:
            A_wins = A_tour_wins.shape[0] - 1

        if A_tour_losses.shape[0] == 0:
            A_losses = 0
        else:
            A_losses = A_tour_losses.shape[0]

        if A_tour_titles.shape[0] == 0:
            A_titles = 0
        else:
            last_row_index = A_tour_titles.index[-1]
            if last_row_index == num:
                A_titles = A_tour_titles.shape[0] - 1
            else:
                A_titles = A_tour_titles.shape[0]

        df.at[num, 'A_wins_tour'] = A_wins
        df.at[num, 'A_losses_tour'] = A_losses
        df.at[num, 'A_matches_tour'] = A_wins + A_losses
        df.at[num, 'A_titles_tour'] = A_titles

        B_tour_wins = temp_df.loc[(temp_df['A_id'] == loser) & (temp_df['tourney_id'] == temp_df['tourney_id'][num])]
        B_tour_losses = temp_df.loc[(temp_df['B_id'] == loser) & (temp_df['tourney_id'] == temp_df['tourney_id'][num])]
        B_tour_titles = B_tour_wins.loc[B_tour_wins['round'] == 'The Final']

        if B_tour_wins.shape[0] == 0:
            B_wins = 0
        else:
            B_wins = B_tour_wins.shape[0]

        if B_tour_losses.shape[0] == 0:
            B_losses = 0
        else:
            B_losses = B_tour_losses.shape[0] - 1

        if B_tour_titles.shape[0] == 0:
            B_titles = 0
        else:
            B_titles = B_tour_titles.shape[0]

        df.at[num, 'B_wins_tour'] = B_wins
        df.at[num, 'B_losses_tour'] = B_losses
        df.at[num, 'B_matches_tour'] = B_wins + B_losses
        df.at[num, 'B_titles_tour'] = B_titles

    # Calculate the percentage of games won in the same tournament
    df['A_tour_per'] = (df['A_wins_tour'] / df['A_matches_tour']) * 100.0
    df['B_tour_per'] = (df['B_wins_tour'] / df['B_matches_tour']) * 100.0

    return df

# 13. Round Statistics
def round_features(df):
    """
    Calculate round statistics ( for lifetime period )
    Wins, Losses, Matches of each player
    Calculate the Percentage of Games Won in the same round
    Some players play better in final rounds
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]

        winner = df['A_id'][num]
        loser = df['B_id'][num]

        A_round_wins = temp_df.loc[(temp_df['A_id'] == winner) & (temp_df['round'] == temp_df['round'][num])]
        A_round_losses = temp_df.loc[(temp_df['B_id'] == winner) & (temp_df['round'] == temp_df['round'][num])]

        if A_round_wins.shape[0] == 0:
            A_wins = 0
        else:
            A_wins = A_round_wins.shape[0] - 1

        if A_round_losses.shape[0] == 0:
            A_losses = 0
        else:
            A_losses = A_round_losses.shape[0]

        df.at[num, 'A_round_wins'] = A_wins
        df.at[num, 'A_round_losses'] = A_losses
        df.at[num, 'A_round_matches'] = A_wins + A_losses

        if A_wins + A_losses == 0:
            df.at[num, 'A_round_per'] = 0
        else:
            df.at[num, 'A_round_per'] = (A_wins / (A_wins + A_losses)) * 100.0

        B_round_wins = temp_df.loc[(temp_df['A_id'] == loser) & (temp_df['round'] == temp_df['round'][num])]
        B_round_losses = temp_df.loc[(temp_df['B_id'] == loser) & (temp_df['round'] == temp_df['round'][num])]

        if B_round_wins.shape[0] == 0:
            B_wins = 0
        else:
            B_wins = B_round_wins.shape[0]

        if B_round_losses.shape[0] == 0:
            B_losses = 0
        else:
            B_losses = B_round_losses.shape[0] - 1

        df.at[num, 'B_round_wins'] = B_wins
        df.at[num, 'B_round_losses'] = B_losses
        df.at[num, 'B_round_matches'] = B_wins + B_losses

        if B_wins + B_losses == 0:
            df.at[num, 'B_round_per'] = 0
        else:
            df.at[num, 'B_round_per'] = (B_wins / (B_wins + B_losses)) * 100.0

    return df

# 14. Ratings
def elo_rating_system(df):
    """
    Calculate Elo Ratings
    See Paper: 2020_[Predicting Tennis Matches Using Machine Learning]
    """
    df['A_elo_rating'] = 1500.0
    df['B_elo_rating'] = 1500.0

    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        winner = df['A_id'][num]
        loser = df['B_id'][num]

        temp_df = df[df['match_index'] <= num]

        winner_df = temp_df[(temp_df['A_id'] == winner) | (temp_df['B_id'] == winner)]
        loser_df = temp_df[(df['A_id'] == loser) | (temp_df['B_id'] == loser)]

        if winner_df.shape[0] == 1:
            first_time_flag_winner = True

        else:
            first_time_flag_winner = False
            winner_l1 = winner_df.iloc[-1, :]  # last row
            winner_l2 = winner_df.iloc[-2, :]  # second from last row

            if winner_l1['A_id'] == winner_l2['A_id']:
                A_previous = winner_l2['A_elo_rating']

            elif winner_l1['A_id'] == winner_l2['B_id']:
                A_previous = winner_l2['B_elo_rating']

        if loser_df.shape[0] == 1:
            first_time_flag_loser = True

        else:
            first_time_flag_loser = False
            loser_l1 = loser_df.iloc[-1, :]  # last row
            loser_l2 = loser_df.iloc[-2, :]  # second from last row

            if loser_l1['B_id'] == loser_l2['B_id']:
                B_previous = loser_l2['B_elo_rating']

            elif loser_l1['B_id'] == loser_l2['A_id']:
                B_previous = loser_l2['A_elo_rating']

        if first_time_flag_winner == False & first_time_flag_loser == False:
            A_current, B_current = helper_calculate_elo(A_previous, B_previous, 1, 0)

            df.at[num, 'A_elo_rating'] = round(A_current, 2)
            df.at[num, 'B_elo_rating'] = round(B_current, 2)

    return df

# 15. Aces Vs Double Faults
def ace_vs_df(df):
    """
    Calculate the Percentage of Ace over Double Faults over the Past 12 Months
    Higher Value means Higher Serving Speed and Accuracy
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        if df['year'][num] == 2010:
            df.at[num, 'A_ratio_ace/df_year'] = 0
            df.at[num, 'B_ratio_ace/df_year'] = 0
        else:
            temp_df = df[df['match_index'] <= num]

            winner = df['A_id'][num]
            loser = df['B_id'][num]

            # find date before one year
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            one_year_ago = date_object - timedelta(days=365)
            new_date = str(one_year_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                day = 1
                month = 1
                year = year + 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 23):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]
            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            lastyear = df.iloc[starting_index:num]

            # Calculate percentage
            winner_df1 = lastyear[(lastyear['A_id'] == winner)]
            winner_df2 = lastyear[(lastyear['B_id'] == winner)]

            mean_value_aces_of_winner = (winner_df1['A_ace'].sum() + winner_df2['B_ace'].sum()) / (winner_df1.shape[0] + winner_df2.shape[0])
            mean_value_dfs_of_winner = (winner_df1['A_df'].sum() + winner_df2['B_df'].sum()) / (winner_df1.shape[0] + winner_df2.shape[0])
            df.at[num, 'A_ratio_ace/df_year'] = (mean_value_aces_of_winner / mean_value_dfs_of_winner) * 100.0

            loser_df1 = lastyear[(lastyear['B_id'] == loser)]
            loser_df2 = lastyear[(lastyear['A_id'] == loser)]

            mean_value_aces_of_loser = (loser_df1['B_ace'].sum() + loser_df2['A_ace'].sum()) / (loser_df1.shape[0] + loser_df2.shape[0])
            mean_value_dfs_of_loser = (loser_df1['B_df'].sum() + loser_df2['A_df'].sum()) / (loser_df1.shape[0] + loser_df2.shape[0])
            df.at[num, 'B_ratio_ace/df_year'] = (mean_value_aces_of_loser / mean_value_dfs_of_loser) * 100.0
    return df

# 16. Performance
def performance_helper_features(df):
    """
    Calculate the Percentage of successful First Serves
    Calculate the Number of successful Second Serves
    Calculate the Percentage of First Serve Points Won
    Calculate the Percentage of Second Serve Points Won
    Calculate the Number of First Serve Return Points Won
    Calculate the Number of Second Serve Return Points Won
    Calculate the Percentage of First Serve Return Points Won
    Calculate the Percentage of Second Serve Return Points Won
    Calculate the Percentage of Break Points Won
    Calculate the Number of Break Points Won
    Calculate the Percentage of Break Points Converted
    See Paper: 2019_[Predicting the Outcome of a Tennis Tournament/ Based on Both Data and Judgments]
    """
    df['A_2ndIn'] = df['A_svpt'] - df['A_1stIn']
    df['B_2ndIn'] = df['B_svpt'] - df['B_1stIn']

    # Calculate the Number of Break Points Won
    df['A_bpWon'] = df['B_bpFaced'] - df['B_bpSaved']
    df['B_bpWon'] = df['A_bpFaced'] - df['A_bpSaved']

    # Calculate the Percentage of Break Points Converted
    df['A_bpConv'] = (df['A_bpWon'] / df['B_bpFaced'])
    df['B_bpConv'] = (df['B_bpWon'] / df['A_bpFaced'])

    # Calculate the Number of First Serve Return Points Won
    df['A_1stSvrptWon'] = df['B_1stIn'] - df['B_1stWon']
    df['B_1stSvrptWon'] = df['A_1stIn'] - df['A_1stWon']

    # Calculate the Number of Second Serve Return Points Won
    df['A_2ndSvrptWon'] = df['B_2ndIn'] - df['B_2ndWon']
    df['B_2ndSvrptWon'] = df['A_2ndIn'] - df['A_2ndWon']

    # Calculate the percentage of making first serve and winning
    df['A_1stServeWon'] = df['A_1stWon'] / df['A_1stIn']
    df['B_1stServeWon'] = df['B_1stWon'] / df['B_1stIn']

    # Calculate the percentage of making second serve and winning
    df['A_2ndServeWon'] = df['A_2ndWon'] / df['A_2ndIn']
    df['B_2ndServeWon'] = df['B_2ndWon'] / df['B_2ndIn']

    # Calculate the percentage of making the first serve
    df['A_1stServe'] = df['A_1stIn'] / df['A_svpt']
    df['B_1stServe'] = df['B_1stIn'] / df['B_svpt']

    # Calculate the Percentage of Break Points Saved
    df['A_bpSavedratio'] = df['A_bpSaved'] / df['A_bpFaced']
    df['B_bpSavedratio'] = df['B_bpSaved'] / df['B_bpFaced']

    return df

# 17. Performance Metrics Mean Values per Career and Year
def performance_mean_values_career_year(df):
    """
       Calculate serve statistics ( for lifetime period )
       Calculate the percentage of making the First Serve
           First Serves' accuracy
       Calculate the percentage of making First Serve and Winning
           First Serves' power
       Calculate the Percentage of making Second Serve and Winning.
           Second Serves' power
       Some players play better in final rounds
       Calculate mental strength statistics ( for lifetime period )
       Calculate the percentage of Break Points Saved
       See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """

    print('Career')
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]

        winner = df['A_id'][num]
        winner_df1 = temp_df[(temp_df['A_id'] == winner)]
        winner_df2 = temp_df[(temp_df['B_id'] == winner)]
        # drop last row which includes current num - only for winner_df1
        winner_df1 = winner_df1.drop(winner_df1.index[-1])

        size1 = winner_df1.shape[0]
        size2 = winner_df2.shape[0]

        mean_value_aces_win = (winner_df1['A_ace'].sum() + winner_df2['B_ace'].sum()) / (size1 + size2)
        mean_value_dfs_win = (winner_df1['A_df'].sum() + winner_df2['B_df'].sum()) / (size1 + size2)
        mean_value_svpt_win = (winner_df1['A_svpt'].sum() + winner_df2['B_svpt'].sum()) / (size1 + size2)
        mean_value_1stIn_win = (winner_df1['A_1stIn'].sum() + winner_df2['B_1stIn'].sum()) / (size1 + size2)
        mean_value_1stWon_win = (winner_df1['A_1stWon'].sum() + winner_df2['B_1stWon'].sum()) / (size1 + size2)
        mean_value_2ndWon_win = (winner_df1['A_2ndWon'].sum() + winner_df2['B_2ndWon'].sum()) / (size1 + size2)
        mean_value_SvGms_win = (winner_df1['A_SvGms'].sum() + winner_df2['B_SvGms'].sum()) / (size1 + size2)
        mean_value_bpSaved_win = (winner_df1['A_bpSaved'].sum() + winner_df2['B_bpSaved'].sum()) / (size1 + size2)
        mean_value_bpFaced_win = (winner_df1['A_bpFaced'].sum() + winner_df2['B_bpFaced'].sum()) / (size1 + size2)
        mean_value_bpWon_win = (winner_df1['A_bpWon'].sum() + winner_df2['B_bpWon'].sum()) / (size1 + size2)
        mean_value_bpConv_win = (winner_df1['A_bpConv'].sum() + winner_df2['B_bpConv'].sum()) / (size1 + size2)
        mean_value_2ndIn_win = (winner_df1['A_2ndIn'].sum() + winner_df2['B_2ndIn'].sum()) / (size1 + size2)
        mean_value_1stSvrptWon_win = (winner_df1['A_1stSvrptWon'].sum() + winner_df2['B_1stSvrptWon'].sum()) / (size1 + size2)
        mean_value_2ndSvrptWon_win = (winner_df1['A_2ndSvrptWon'].sum() + winner_df2['B_2ndSvrptWon'].sum()) / (size1 + size2)
        mean_value_1stServeWon_win = (winner_df1['A_1stServeWon'].sum() + winner_df2['B_1stServeWon'].sum()) / (size1 + size2)
        mean_value_2ndServeWon_win = (winner_df1['A_2ndServeWon'].sum() + winner_df2['B_2ndServeWon'].sum()) / (size1 + size2)
        mean_value_1stServe_win = (winner_df1['A_1stServe'].sum() + winner_df2['B_1stServe'].sum()) / (size1 + size2)
        mean_value_bpSavedratio_win = (winner_df1['A_bpSavedratio'].sum() + winner_df2['B_bpSavedratio'].sum()) / (size1 + size2)

        df.at[num, 'A_ace_career'] = mean_value_aces_win
        df.at[num, 'A_df_career'] = mean_value_dfs_win
        df.at[num, 'A_svpt_career'] = mean_value_svpt_win
        df.at[num, 'A_1stIn_career'] = mean_value_1stIn_win
        df.at[num, 'A_1stWon_career'] = mean_value_1stWon_win
        df.at[num, 'A_2ndWon_career'] = mean_value_2ndWon_win
        df.at[num, 'A_SvGms_career'] = mean_value_SvGms_win
        df.at[num, 'A_bpSaved_career'] = mean_value_bpSaved_win
        df.at[num, 'A_bpFaced_career'] = mean_value_bpFaced_win
        df.at[num, 'A_2ndIn_career'] = mean_value_2ndIn_win
        df.at[num, 'A_1stSvrptWon_career'] = mean_value_1stSvrptWon_win
        df.at[num, 'A_2ndSvrptWon_career'] = mean_value_2ndSvrptWon_win
        df.at[num, 'A_1stServeWon_career'] = mean_value_1stServeWon_win
        df.at[num, 'A_2ndServeWon_career'] = mean_value_2ndServeWon_win
        df.at[num, 'A_1stServe_career'] = mean_value_1stServe_win
        df.at[num, 'A_bpSavedratio_career'] = mean_value_bpSavedratio_win
        df.at[num, 'A_bpWon_career'] = mean_value_bpWon_win
        df.at[num, 'A_bpConv_career'] = mean_value_bpConv_win

        loser = df['B_id'][num]
        loser_df1 = temp_df[(temp_df['A_id'] == loser)]
        loser_df2 = temp_df[(temp_df['B_id'] == loser)]

        # drop last row which includes current num - only for loser_df2
        loser_df2 = loser_df2.drop(loser_df2.index[-1])

        size1 = loser_df1.shape[0]
        size2 = loser_df2.shape[0]

        mean_value_aces_los = (loser_df1['A_ace'].sum() + loser_df2['B_ace'].sum()) / (size1 + size2)
        mean_value_dfs_los = (loser_df1['A_df'].sum() + loser_df2['B_df'].sum()) / (size1 + size2)
        mean_value_svpt_los = (loser_df1['A_svpt'].sum() + loser_df2['B_svpt'].sum()) / (size1 + size2)
        mean_value_1stIn_los = (loser_df1['A_1stIn'].sum() + loser_df2['B_1stIn'].sum()) / (size1 + size2)
        mean_value_1stWon_los = (loser_df1['A_1stWon'].sum() + loser_df2['B_1stWon'].sum()) / (size1 + size2)
        mean_value_2ndWon_los = (loser_df1['A_2ndWon'].sum() + loser_df2['B_2ndWon'].sum()) / (size1 + size2)
        mean_value_SvGms_los = (loser_df1['A_SvGms'].sum() + loser_df2['B_SvGms'].sum()) / (size1 + size2)
        mean_value_bpSaved_los = (loser_df1['A_bpSaved'].sum() + loser_df2['B_bpSaved'].sum()) / (size1 + size2)
        mean_value_bpFaced_los = (loser_df1['A_bpFaced'].sum() + loser_df2['B_bpFaced'].sum()) / (size1 + size2)
        mean_value_bpWon_los = (loser_df1['A_bpWon'].sum() + loser_df2['B_bpWon'].sum()) / (size1 + size2)
        mean_value_bpConv_los = (loser_df1['A_bpConv'].sum() + loser_df2['B_bpConv'].sum()) / (size1 + size2)
        mean_value_2ndIn_los = (loser_df1['A_2ndIn'].sum() + loser_df2['B_2ndIn'].sum()) / (size1 + size2)
        mean_value_1stSvrptWon_los = (loser_df1['A_1stSvrptWon'].sum() + loser_df2['B_1stSvrptWon'].sum()) / (size1 + size2)
        mean_value_2ndSvrptWon_los = (loser_df1['A_2ndSvrptWon'].sum() + loser_df2['B_2ndSvrptWon'].sum()) / (size1 + size2)
        mean_value_1stServeWon_los = (loser_df1['A_1stServeWon'].sum() + loser_df2['B_1stServeWon'].sum()) / (size1 + size2)
        mean_value_2ndServeWon_los = (loser_df1['A_2ndServeWon'].sum() + loser_df2['B_2ndServeWon'].sum()) / (size1 + size2)
        mean_value_1stServe_los = (loser_df1['A_1stServe'].sum() + loser_df2['B_1stServe'].sum()) / (size1 + size2)
        mean_value_bpSavedratio_los = (loser_df1['A_bpSavedratio'].sum() + loser_df2['B_bpSavedratio'].sum()) / (size1 + size2)

        df.at[num, 'B_ace_career'] = mean_value_aces_los
        df.at[num, 'B_df_career'] = mean_value_dfs_los
        df.at[num, 'B_svpt_career'] = mean_value_svpt_los
        df.at[num, 'B_1stIn_career'] = mean_value_1stIn_los
        df.at[num, 'B_1stWon_career'] = mean_value_1stWon_los
        df.at[num, 'B_2ndWon_career'] = mean_value_2ndWon_los
        df.at[num, 'B_SvGms_career'] = mean_value_SvGms_los
        df.at[num, 'B_bpSaved_career'] = mean_value_bpSaved_los
        df.at[num, 'B_bpFaced_career'] = mean_value_bpFaced_los
        df.at[num, 'B_2ndIn_career'] = mean_value_2ndIn_los
        df.at[num, 'B_1stSvrptWon_career'] = mean_value_1stSvrptWon_los
        df.at[num, 'B_2ndSvrptWon_career'] = mean_value_2ndSvrptWon_los
        df.at[num, 'B_1stServeWon_career'] = mean_value_1stServeWon_los
        df.at[num, 'B_2ndServeWon_career'] = mean_value_2ndServeWon_los
        df.at[num, 'B_1stServe_career'] = mean_value_1stServe_los
        df.at[num, 'B_bpSavedratio_career'] = mean_value_bpSavedratio_los
        df.at[num, 'B_bpWon_career'] = mean_value_bpWon_los
        df.at[num, 'B_bpConv_career'] = mean_value_bpConv_los


    print('Year')
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        if df['year'][num] == 2010:
            df.at[num, 'A_wins_year'] = 0
            df.at[num, 'A_losses_year'] = 0
            df.at[num, 'A_matches_year'] = 0
            df.at[num, 'A_titles_year'] = 0

            df.at[num, 'B_wins_year'] = 0
            df.at[num, 'B_losses_year'] = 0
            df.at[num, 'B_matches_year'] = 0
            df.at[num, 'B_titles_year'] = 0

        else:
            winner = df['A_id'][num]
            loser = df['B_id'][num]

            temp_df = df[df['match_index'] <= num]

            # find date before one year
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            one_year_ago = date_object - timedelta(days=365)
            new_date = str(one_year_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find the starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                day = 1
                month = 1
                year = year + 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 23):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]
            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            lastyear = df.iloc[starting_index:num]

            winner_df1 = lastyear[(lastyear['A_id'] == winner)]
            winner_df2 = lastyear[(lastyear['B_id'] == winner)]

            size1 = winner_df1.shape[0]
            size2 = winner_df2.shape[0]

            mean_value_aces_win = (winner_df1['A_ace'].sum() + winner_df2['B_ace'].sum()) / (size1 + size2)
            mean_value_dfs_win = (winner_df1['A_df'].sum() + winner_df2['B_df'].sum()) / (size1 + size2)
            mean_value_svpt_win = (winner_df1['A_svpt'].sum() + winner_df2['B_svpt'].sum()) / (size1 + size2)
            mean_value_1stIn_win = (winner_df1['A_1stIn'].sum() + winner_df2['B_1stIn'].sum()) / (size1 + size2)
            mean_value_1stWon_win = (winner_df1['A_1stWon'].sum() + winner_df2['B_1stWon'].sum()) / (size1 + size2)
            mean_value_2ndWon_win = (winner_df1['A_2ndWon'].sum() + winner_df2['B_2ndWon'].sum()) / (size1 + size2)
            mean_value_SvGms_win = (winner_df1['A_SvGms'].sum() + winner_df2['B_SvGms'].sum()) / (size1 + size2)
            mean_value_bpSaved_win = (winner_df1['A_bpSaved'].sum() + winner_df2['B_bpSaved'].sum()) / (size1 + size2)
            mean_value_bpFaced_win = (winner_df1['A_bpFaced'].sum() + winner_df2['B_bpFaced'].sum()) / (size1 + size2)
            mean_value_bpWon_win = (winner_df1['A_bpWon'].sum() + winner_df2['B_bpWon'].sum()) / (size1 + size2)
            mean_value_bpConv_win = (winner_df1['A_bpConv'].sum() + winner_df2['B_bpConv'].sum()) / (size1 + size2)
            mean_value_2ndIn_win = (winner_df1['A_2ndIn'].sum() + winner_df2['B_2ndIn'].sum()) / (size1 + size2)
            mean_value_1stSvrptWon_win = (winner_df1['A_1stSvrptWon'].sum() + winner_df2['B_1stSvrptWon'].sum()) / (size1 + size2)
            mean_value_2ndSvrptWon_win = (winner_df1['A_2ndSvrptWon'].sum() + winner_df2['B_2ndSvrptWon'].sum()) / (size1 + size2)
            mean_value_1stServeWon_win = (winner_df1['A_1stServeWon'].sum() + winner_df2['B_1stServeWon'].sum()) / (size1 + size2)
            mean_value_2ndServeWon_win = (winner_df1['A_2ndServeWon'].sum() + winner_df2['B_2ndServeWon'].sum()) / (size1 + size2)
            mean_value_1stServe_win = (winner_df1['A_1stServe'].sum() + winner_df2['B_1stServe'].sum()) / (size1 + size2)
            mean_value_bpSavedratio_win = (winner_df1['A_bpSavedratio'].sum() + winner_df2['B_bpSavedratio'].sum()) / (size1 + size2)

            df.at[num, 'A_ace_year'] = mean_value_aces_win
            df.at[num, 'A_df_year'] = mean_value_dfs_win
            df.at[num, 'A_svpt_year'] = mean_value_svpt_win
            df.at[num, 'A_1stIn_year'] = mean_value_1stIn_win
            df.at[num, 'A_1stWon_year'] = mean_value_1stWon_win
            df.at[num, 'A_2ndWon_year'] = mean_value_2ndWon_win
            df.at[num, 'A_SvGms_year'] = mean_value_SvGms_win
            df.at[num, 'A_bpSaved_year'] = mean_value_bpSaved_win
            df.at[num, 'A_bpFaced_year'] = mean_value_bpFaced_win
            df.at[num, 'A_bpWon_year'] = mean_value_bpWon_win
            df.at[num, 'A_bpConv_year'] = mean_value_bpConv_win
            df.at[num, 'A_2ndIn_year'] = mean_value_2ndIn_win
            df.at[num, 'A_1stSvrptWon_year'] = mean_value_1stSvrptWon_win
            df.at[num, 'A_2ndSvrptWon_year'] = mean_value_2ndSvrptWon_win
            df.at[num, 'A_1stServeWon_year'] = mean_value_1stServeWon_win
            df.at[num, 'A_2ndServeWon_year'] = mean_value_2ndServeWon_win
            df.at[num, 'A_1stServe_year'] = mean_value_1stServe_win
            df.at[num, 'A_bpSavedratio_year'] = mean_value_bpSavedratio_win


            loser_df1 = lastyear[(lastyear['A_id'] == loser)]
            loser_df2 = lastyear[(lastyear['B_id'] == loser)]

            size1 = loser_df1.shape[0]
            size2 = loser_df2.shape[0]

            mean_value_aces_los = (loser_df1['A_ace'].sum() + loser_df2['B_ace'].sum()) / (size1 + size2)
            mean_value_dfs_los = (loser_df1['A_df'].sum() + loser_df2['B_df'].sum()) / (size1 + size2)
            mean_value_svpt_los = (loser_df1['A_svpt'].sum() + loser_df2['B_svpt'].sum()) / (size1 + size2)
            mean_value_1stIn_los = (loser_df1['A_1stIn'].sum() + loser_df2['B_1stIn'].sum()) / (size1 + size2)
            mean_value_1stWon_los = (loser_df1['A_1stWon'].sum() + loser_df2['B_1stWon'].sum()) / (size1 + size2)
            mean_value_2ndWon_los = (loser_df1['A_2ndWon'].sum() + loser_df2['B_2ndWon'].sum()) / (size1 + size2)
            mean_value_SvGms_los = (loser_df1['A_SvGms'].sum() + loser_df2['B_SvGms'].sum()) / (size1 + size2)
            mean_value_bpSaved_los = (loser_df1['A_bpSaved'].sum() + loser_df2['B_bpSaved'].sum()) / (size1 + size2)
            mean_value_bpFaced_los = (loser_df1['A_bpFaced'].sum() + loser_df2['B_bpFaced'].sum()) / (size1 + size2)
            mean_value_bpWon_los = (loser_df1['A_bpWon'].sum() + loser_df2['B_bpWon'].sum()) / (size1 + size2)
            mean_value_bpConv_los = (loser_df1['A_bpConv'].sum() + loser_df2['B_bpConv'].sum()) / (size1 + size2)
            mean_value_2ndIn_los = (loser_df1['A_2ndIn'].sum() + loser_df2['B_2ndIn'].sum()) / (size1 + size2)
            mean_value_1stSvrptWon_los = (loser_df1['A_1stSvrptWon'].sum() + loser_df2['B_1stSvrptWon'].sum()) / (size1 + size2)
            mean_value_2ndSvrptWon_los = (loser_df1['A_2ndSvrptWon'].sum() + loser_df2['B_2ndSvrptWon'].sum()) / (size1 + size2)
            mean_value_1stServeWon_los = (loser_df1['A_1stServeWon'].sum() + loser_df2['B_1stServeWon'].sum()) / (size1 + size2)
            mean_value_2ndServeWon_los = (loser_df1['A_2ndServeWon'].sum() + loser_df2['B_2ndServeWon'].sum()) / (size1 + size2)
            mean_value_1stServe_los = (loser_df1['A_1stServe'].sum() + loser_df2['B_1stServe'].sum()) / (size1 + size2)
            mean_value_bpSavedratio_los = (loser_df1['A_bpSavedratio'].sum() + loser_df2['B_bpSavedratio'].sum()) / (size1 + size2)

            df.at[num, 'B_ace_year'] = mean_value_aces_los
            df.at[num, 'B_df_year'] = mean_value_dfs_los
            df.at[num, 'B_svpt_year'] = mean_value_svpt_los
            df.at[num, 'B_1stIn_year'] = mean_value_1stIn_los
            df.at[num, 'B_1stWon_year'] = mean_value_1stWon_los
            df.at[num, 'B_2ndWon_year'] = mean_value_2ndWon_los
            df.at[num, 'B_SvGms_year'] = mean_value_SvGms_los
            df.at[num, 'B_bpSaved_year'] = mean_value_bpSaved_los
            df.at[num, 'B_bpFaced_year'] = mean_value_bpFaced_los
            df.at[num, 'B_bpWon_year'] = mean_value_bpWon_los
            df.at[num, 'B_bpConv_year'] = mean_value_bpConv_los
            df.at[num, 'B_2ndIn_year'] = mean_value_2ndIn_los
            df.at[num, 'B_1stSvrptWon_year'] = mean_value_1stSvrptWon_los
            df.at[num, 'B_2ndSvrptWon_year'] = mean_value_2ndSvrptWon_los
            df.at[num, 'B_1stServeWon_year'] = mean_value_1stServeWon_los
            df.at[num, 'B_2ndServeWon_year'] = mean_value_2ndServeWon_los
            df.at[num, 'B_1stServe_year'] = mean_value_1stServe_los
            df.at[num, 'B_bpSavedratio_year'] = mean_value_bpSavedratio_los
    return df

# 18. Mental Strength Statistics
def mental_strength_features(df):
    """
    Calculate mental strength statistics ( for lifetime period )
    Calculate Head - to - Head results (Games Won against the same opponent)
    Calculate the Percentage of Games Won against the same opponent
    See Paper: 2019_[Random forest model identifies serve strength as a key predictor of tennis match outcome]
    """
    # Calculate Head - to - Head results
    # Games Won against the same opponent
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]

        winner = temp_df['A_id'][num]
        loser = temp_df['B_id'][num]

        h2h_1 = temp_df.loc[(temp_df['A_id'] == winner) & (temp_df['B_id'] == loser)]
        h2h_2 = temp_df.loc[(temp_df['A_id'] == loser) & (temp_df['B_id'] == winner)]

        df.at[num, 'A_over_B'] = (h2h_1.shape[0] - 1)
        df.at[num, 'B_over_A'] = h2h_2.shape[0]

    # Calculate the Percentage of games won against the same opponent
    df['A_Win_oppon'] = (df['A_over_B'] / df['A_over_B'] + df['B_over_A'])
    df['B_Win_oppon'] = (df['B_over_A'] / df['A_over_B'] + df['B_over_A'])

    return df

# 19. Winning Streak, Losing Streak, Inactivity
def streaks_and_inactivity(df):
    """
    Calculate winning streak (consecutive wins)
    Calculate losing streak (consecutive losses)
    Calculate inactivity (number of weeks inactive)
    See Paper: 2020_[Predicting Tennis Matches Using Machine Learning]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] <= num]
        winner = temp_df['A_id'][num]
        loser = temp_df['B_id'][num]
        date_now = str(temp_df['tourney_date'][num])

        w = temp_df[(temp_df['A_id'] == winner) | (temp_df['B_id'] == winner)]
        w = w.drop(w.index[-1])

        # revert dataset to read from latest data
        w = w.sort_index(ascending=False)

        df.at[num, 'A_wstreak'] = winning_streak(w, winner, 'A_id')
        df.at[num, 'A_lstreak'] = losing_streak(w, winner, 'B_id')

        if w.shape[0]==0:
            # number for entry players
            df.at[num, 'A_days_inactive'] = 150
        else:
            # get last match date of player A
            last_date_w = str(w.iloc[0]['tourney_date'])
            df.at[num, 'A_days_inactive'] = days_inactive(last_date_w, date_now)

        l = temp_df[(temp_df['A_id'] == loser) | (temp_df['B_id'] == loser)]
        l = l.drop(l.index[-1])

        # reverted datase to read from latest data
        l = l.sort_index(ascending=False)
        df.at[num, 'B_wstreak'] = winning_streak(l, loser, 'A_id')
        df.at[num, 'B_lstreak'] = losing_streak(l, loser, 'B_id')
        if l.shape[0]==0:
            # number for entry players
            df.at[num, 'B_days_inactive'] = 150
        else:
            # get last match date of player B
            last_date_l = str(l.iloc[0]['tourney_date'])
            df.at[num, 'B_days_inactive'] = days_inactive(last_date_l, date_now)

    return df

# 20. Player Momentum
def player_momentum(df):
    """
    The player momentum is the current Form of a player and it is calculated by
    the player's average ranking (on a log-scale) over the previous six months
    minus his or her current ranking. A positive value hence indicates that the
    player has been on a winning streak, and one can postulate that this "momentum"
    has an influence on the match at hand.
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        if (df['year'][num] == 2010) and (df['month'][num] <= 6):
            df.at[num, 'A_momentum'] = 0
            df.at[num, 'B_momentum'] = 0
        else:
            winner = df['A_id'][num]
            loser = df['B_id'][num]
            winner_rank = df['A_rank'][num]
            loser_rank = df['B_rank'][num]
            temp_df = df[df['match_index'] <= num]

            # find date before six months ( one semester )
            date = str(temp_df['tourney_date'][num])
            date_object = datetime.strptime(date, "%Y%m%d")
            six_months_ago = date_object - timedelta(days=182)
            new_date = str(six_months_ago)
            year = int(new_date[0:4])
            month = int(new_date[5:7])
            day = int(new_date[8:10])

            # find the starting index
            to_start = temp_df.loc[(temp_df['year'] == year)]
            test_start = to_start.loc[to_start['month'] >= month]
            test_start = test_start.loc[to_start['day'] >= day]

            if (test_start.shape[0] == 0) and (month == 12):
                day = 1
                month = 1
                year = year + 1
            elif (test_start.shape[0] == 0) and (month == 11):
                year = year + 1
                month = 1
                day = 1
            elif (test_start.shape[0] == 0) and (day >= 23):
                month = month + 1
                day = 1

            to_start = temp_df.loc[temp_df['year'] == year]
            to_start = to_start.loc[to_start['month'] >= month]
            to_start = to_start.loc[to_start['day'] >= day]

            starting_index = to_start.index[0]

            lastsemester = df.iloc[starting_index:num]

            winner_df1 = lastsemester[(lastsemester['A_id'] == winner)]
            winner_df2 = lastsemester[(lastsemester['B_id'] == winner)]

            loser_df1 = lastsemester[(lastsemester['B_id'] == loser)]
            loser_df2 = lastsemester[(lastsemester['A_id'] == loser)]

            rank_win1 = winner_df1['A_rank'].sum()
            shape_win1 = winner_df1.shape[0]
            rank_win2 = winner_df2['B_rank'].sum()
            shape_win2 = winner_df2.shape[0]

            rank_los1 = loser_df1['B_rank'].sum()
            shape_los1 = loser_df1.shape[0]
            rank_los2 = loser_df2['A_rank'].sum()
            shape_los2 = loser_df2.shape[0]

            A_momentum = math.log((rank_win1 + rank_win2) / (shape_win1 + shape_win2)) - math.log(winner_rank)
            B_momentum = math.log((rank_los1 + rank_los2) / (shape_los1 + shape_los2)) - math.log(loser_rank)

            df.at[num, 'A_momentum'] = round(A_momentum, 4)
            df.at[num, 'B_momentum'] = round(B_momentum, 4)

    return df

# 21. Preferred Hand
def preferred_hand(df):
    """
    Player's Preferred Hand
    There are four possible combinations (RR, LL, RL, LR)
    See Paper: 2021_[Sports prediction and betting models in the machine learning age/ The case of tennis]
    """
    df[['A_hand', 'B_hand']].fillna('R', inplace=True)
    for num in range(0, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        values = {'A_hand': {'U': 'R'}, 'B_hand': {'U': 'R'}}
        df.replace(values, inplace=True)

        if df['A_hand'][num] == 'R' and df['B_hand'][num] == 'R':
            df.at[num, 'preferred_hand'] = 'RR'
        elif df['A_hand'][num] == 'L' and df['B_hand'][num] == 'L':
            df.at[num, 'preferred_hand'] = 'LL'
        elif df['A_hand'][num] == 'R' and df['B_hand'][num] == 'L':
            df.at[num, 'preferred_hand'] = 'RL'
        elif df['A_hand'][num] == 'L' and df['B_hand'][num] == 'R':
            df.at[num, 'preferred_hand'] = 'LR'

    return df

####### RUN FUNCTIONS #######
def run_feature_engineering_1(df):
    # 1
    print('Home Advantage')
    start_time = datetime.now()
    df['home_advantage'] = df.apply(get_home_advantage, axis=1)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 2
    print('Log Rankings')
    start_time = datetime.now()
    df = df.apply(compute_log_rankings, axis=1)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 3
    print('Match Quality')
    start_time = datetime.now()
    df = get_match_quality(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 4
    print('Surface - create variable')
    start_time = datetime.now()
    df = df.apply(combine_surface_court, axis=1)
    #df = get_surface_features(df)
    #df = calculate_percentage(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 5
    print('Betting Features')
    start_time = datetime.now()
    df = betting_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    return df

def run_feature_engineering_2(df):
    # 6
    print('Career Statistics')
    start_time = datetime.now()
    df = career_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 7
    print('Yearly Statistics')
    start_time = datetime.now()
    df = yearly_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 8
    print('Semesterly Statistics')
    start_time = datetime.now()
    df = semester_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 9
    print('Recent Matches Statistics')
    start_time = datetime.now()
    df = recent_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    return df

def run_feature_engineering_3(df):
    # 10
    print('Surface information 2')
    start_time = datetime.now()
    df = get_surface_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 11
    print('Surface information 3')
    start_time = datetime.now()
    df = calculate_per_surface(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 12
    print('Tournament Statistics')
    start_time = datetime.now()
    df = tournament_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 13
    print('Round Statistics')
    start_time = datetime.now()
    df = round_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 14
    print('Elo Ratings')
    start_time = datetime.now()
    df = elo_rating_system(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    return df

def run_feature_engineering_4(df):
    # 15
    print('ace vs df')
    start_time = datetime.now()
    df = ace_vs_df(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 16
    print('Performance Metrics 1')
    start_time = datetime.now()
    df = performance_helper_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 17
    print('Performance Metrics 2')
    start_time = datetime.now()
    df = performance_mean_values_career_year(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))
    return df

def run_feature_engineering_5(df):
    # 18. Mental Strength Statistics
    print('Mental Strength Statistics')
    start_time = datetime.now()
    df = mental_strength_features(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 19. Winning Streak, Losing Streak, Inactivity
    print('Winning Streak, Losing Streak, Inactivity')
    start_time = datetime.now()
    df = streaks_and_inactivity(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 20. Player Momentum
    print('Player Momentum')
    start_time = datetime.now()
    df = player_momentum(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))

    # 21. Preferred Hand
    print('Preferred Hand')
    start_time = datetime.now()
    df = preferred_hand(df)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('---Execution time:', str(elapsed_time))
    return df

def run_feat_eng(df):
    path_fe1 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_1.csv"
    isFile_fe1 = os.path.isfile(path=path_fe1)
    print('Part 1')
    if not isFile_fe1:
        df = run_feature_engineering_1(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_1.csv")
    else:
        print('***COMPLETED***')

    path_fe2 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_2.csv"
    print('Part 2')
    isFile_fe2 = os.path.isfile(path=path_fe2)
    if not isFile_fe2:
        df = pd.read_csv(path_fe1, low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df.sort_values(['match_index'], inplace=True)
        df = run_feature_engineering_2(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_2.csv")
    else:
        print('***COMPLETED***')

    path_fe3 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_3.csv"
    print('Part 3')
    isFile_fe3 = os.path.isfile(path=path_fe3)
    if not isFile_fe3:
        df = pd.read_csv(path_fe2, low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df = run_feature_engineering_3(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_3.csv")
    else:
        print('***COMPLETED***')

    path_fe4 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_4.csv"
    print('Part 4')
    isFile_fe4 = os.path.isfile(path=path_fe4)
    if not isFile_fe4:
        df = pd.read_csv(path_fe3, low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df = run_feature_engineering_4(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_4.csv")
    else:
        print('***COMPLETED***')

    path_fe5 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_5.csv"
    print('Part 5')
    isFile_fe5 = os.path.isfile(path=path_fe5)
    if not isFile_fe5:
        df = pd.read_csv(path_fe4, low_memory=False)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df = run_feature_engineering_5(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_5.csv")
    else:
        print('***COMPLETED***')
        df = pd.read_csv(path_fe5, low_memory=False)

    return df

####### DIFFERENCES #######
def get_differences_features(df):
    df.fillna(0, inplace=True)
    df.replace(np.inf, 0, inplace=True)
    df.replace(-np.inf, 0, inplace=True)

    df['rank'] = df['A_rank'] - df['B_rank']
    df['rank_points'] = df['A_rank_points'] - df['B_rank_points']
    df['rank_log'] = df['A_rank_log'] - df['B_rank_log']
    df['rank_points_log'] = df['A_rank_points_log'] - df['B_rank_points_log']
    df['age'] = df['A_age'] - df['B_age']
    df['height'] = df['A_ht'] - df['B_ht']

    df['spread'] = df['A_spread'] - df['B_spread']
    df['B365'] = df['A_B365'] - df['B_B365']
    df['wins_career'] = df['A_wins_career'] - df['B_wins_career']
    df['losses_career'] = df['A_losses_career'] - df['B_losses_career']
    df['matches_career'] = df['A_matches_career'] - df['B_matches_career']
    df['titles_career'] = df['A_titles_career'] - df['B_titles_career']
    df['wins_year'] = df['A_wins_year'] - df['B_wins_year']
    df['losses_year'] = df['A_losses_year'] - df['B_losses_year']
    df['matches_year'] = df['A_matches_year'] - df['B_matches_year']
    df['titles_year'] = df['A_titles_year'] - df['B_titles_year']
    df['matches_year_per'] = df['A_matches_year_per'] - df['B_matches_year_per']

    df['wins_semester'] = df['A_wins_semester'] - df['B_wins_semester']
    df['losses_semester'] = df['A_losses_semester'] - df['B_losses_semester']
    df['matches_semester'] = df['A_matches_semester'] - df['B_matches_semester']
    df['titles_semester'] = df['A_titles_semester'] - df['B_titles_semester']
    df['wins_recent'] = df['A_wins_recent'] - df['B_wins_recent']
    df['losses_recent'] = df['A_losses_recent'] - df['B_losses_recent']
    df['matches_recent'] = df['A_matches_recent'] - df['B_matches_recent']
    df['titles_recent'] = df['A_titles_recent'] - df['B_titles_recent']
    df['matches_per_surface'] = df['A_matches_per_surface'] - df['B_matches_per_surface']
    df['wins_per_surface'] = df['A_wins_per_surface'] - df['B_wins_per_surface']
    df['losses_per_surface'] = df['A_losses_per_surface'] - df['B_losses_per_surface']
    df['titles_per_surface'] = df['A_titles_per_surface'] - df['B_titles_per_surface']

    df['surface_per'] = df['A_surface_per'] - df['B_surface_per']
    df['wins_tour'] = df['A_wins_tour'] - df['B_wins_tour']
    df['losses_tour'] = df['A_losses_tour'] - df['B_losses_tour']
    df['matches_tour'] = df['A_matches_tour'] - df['B_matches_tour']
    df['titles_tour'] = df['A_titles_tour'] - df['B_titles_tour']
    df['tour_per'] = df['A_tour_per'] - df['B_tour_per']
    df['round_wins'] = df['A_round_wins'] - df['B_round_wins']
    df['round_losses'] = df['A_round_losses'] - df['B_round_losses']
    df['round_matches'] = df['A_round_matches'] - df['B_round_matches']
    df['round_per'] = df['A_round_per'] - df['B_round_per']
    df['elo_rating'] = df['A_elo_rating'] - df['B_elo_rating']
    df['ratio_ace/df_year'] = df['A_ratio_ace/df_year'] - df['B_ratio_ace/df_year']

    df['ace_career'] = df['A_ace_career'] - df['B_ace_career']
    df['df_career'] = df['A_df_career'] - df['B_df_career']
    df['svpt_career'] = df['A_svpt_career'] - df['B_svpt_career']
    df['1stIn_career'] = df['A_1stIn_career'] - df['B_1stIn_career']
    df['1stWon_career'] = df['A_1stWon_career'] - df['B_1stWon_career']
    df['2ndWon_career'] = df['A_2ndWon_career'] - df['B_2ndWon_career']
    df['SvGms_career'] = df['A_SvGms_career'] - df['B_SvGms_career']
    df['bpSaved_career'] = df['A_bpSaved_career'] - df['B_bpSaved_career']
    df['bpFaced_career'] = df['A_bpFaced_career'] - df['B_bpFaced_career']
    df['bpWon_career'] = df['A_bpWon_career'] - df['B_bpWon_career']
    df['bpConv_career'] = df['A_bpConv_career'] - df['B_bpConv_career']
    df['2ndIn_career'] = df['A_2ndIn_career'] - df['B_2ndIn_career']
    df['1stSvrptWon_career'] = df['A_1stSvrptWon_career'] - df['B_1stSvrptWon_career']
    df['2ndSvrptWon_career'] = df['A_2ndSvrptWon_career'] - df['B_2ndSvrptWon_career']
    df['1stServeWon_career'] = df['A_1stServeWon_career'] - df['B_1stServeWon_career']
    df['2ndServeWon_career'] = df['A_2ndServeWon_career'] - df['B_2ndServeWon_career']
    df['1stServe_career'] = df['A_1stServe_career'] - df['B_1stServe_career']
    df['bpSavedratio_career'] = df['A_bpSavedratio_career'] - df['B_bpSavedratio_career']

    df['ace_year'] = df['A_ace_year'] - df['B_ace_year']
    df['df_year'] = df['A_df_year'] - df['B_df_year']
    df['svpt_year'] = df['A_svpt_year'] - df['B_svpt_year']
    df['1stIn_year'] = df['A_1stIn_year'] - df['B_1stIn_year']
    df['1stWon_year'] = df['A_1stWon_year'] - df['B_1stWon_year']
    df['2ndWon_year'] = df['A_2ndWon_year'] - df['B_2ndWon_year']
    df['SvGms_year'] = df['A_SvGms_year'] - df['B_SvGms_year']
    df['bpSaved_year'] = df['A_bpSaved_year'] - df['B_bpSaved_year']
    df['bpFaced_year'] = df['A_bpFaced_year'] - df['B_bpFaced_year']
    df['bpWon_year'] = df['A_bpWon_year'] - df['B_bpWon_year']
    df['bpConv_year'] = df['A_bpConv_year'] - df['B_bpConv_year']
    df['2ndIn_year'] = df['A_2ndIn_year'] - df['B_2ndIn_year']
    df['1stSvrptWon_year'] = df['A_1stSvrptWon_year'] - df['B_1stSvrptWon_year']
    df['2ndSvrptWon_year'] = df['A_2ndSvrptWon_year'] - df['B_2ndSvrptWon_year']
    df['1stServeWon_year'] = df['A_1stServeWon_year'] - df['B_1stServeWon_year']
    df['2ndServeWon_year'] = df['A_2ndServeWon_year'] - df['B_2ndServeWon_year']
    df['1stServe_year'] = df['A_1stServe_year'] - df['B_1stServe_year']
    df['bpSavedratio_year'] = df['A_bpSavedratio_year'] - df['B_bpSavedratio_year']

    df['headtohead'] = df['A_over_B'] - df['B_over_A']
    df['Win_oppon'] = df['A_Win_oppon'] - df['B_Win_oppon']
    df['wstreak'] = df['A_wstreak'] - df['B_wstreak']
    df['lstreak'] = df['A_lstreak'] - df['B_lstreak']
    df['days_inactive'] = df['A_days_inactive'] - df['B_days_inactive']
    df['momentum'] = df['A_momentum'] - df['B_momentum']
    return df

######## HELPER FUNCTIONS ########

# H.1
def calculate_opponents(df, player):
    df = df[(df['A_id'] == player) | (df['B_id'] == player)]
    op_1 = df['A_id'].tolist()
    op_2 = df['B_id'].tolist()
    op = []
    for p in op_1:
        if p != player:
            if p not in op:
                op.append(p)
    for p in op_2:
        if p != player:
            if p not in op:
                op.append(p)
    return op

"""
# H.2
def calc_mean(temp_df, player, opponent, flag):
    df1 = temp_df[(temp_df['A_id'] == player) & (temp_df['B_id'] == opponent)]
    df2 = temp_df[(temp_df['A_id'] == opponent) & (temp_df['B_id'] == player)]
    l1 = df1['A_' + flag].tolist()
    l2 = df2['B_' + flag].tolist()
    l = l1 + l2
    return statistics.mean(l)

# H.3
def common_opponent_calculator(df, common_op, plA, plB, feature):
    A_feature_mean_value = 0
    B_feature_mean_value = 0

    num_of_opponents = len(common_op)
    for opponent in common_op:
        A_feature_mean_value = A_feature_mean_value + calc_mean(df, plA, opponent, feature)
        B_feature_mean_value = B_feature_mean_value + calc_mean(df, plB, opponent, feature)

    A_mean = A_feature_mean_value / num_of_opponents
    B_mean = B_feature_mean_value / num_of_opponents
    difference = A_mean - B_mean
    return difference
"""
######## UTIL FUNCTIONS ########

# Get differences if players have common opponents
def get_differences_for_common_opponent(df):
    for num in range(1, df.shape[0]):
        if num in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                   11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                   21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]:
            print('Working on it (', num, ')..')

        temp_df = df[df['match_index'] < num]

        winner = df['A_id'][num]
        loser = df['B_id'][num]

        A_opponents = calculate_opponents(temp_df, winner)
        B_opponents = calculate_opponents(temp_df, loser)

        common_opponents = set(A_opponents) & set(B_opponents)

        # df for winner
        df_w1 = temp_df[temp_df['A_id'] == winner]
        df_w1 = df_w1[df_w1['B_id'].isin(common_opponents)]

        df_w2 = temp_df[temp_df['B_id'] == winner]
        df_w2 = df_w2[df_w2['A_id'].isin(common_opponents)]

        # df for loser
        df_l1 = temp_df[temp_df['A_id'] == loser]
        df_l1 = df_l1[df_l1['B_id'].isin(common_opponents)]

        df_l2 = temp_df[temp_df['B_id'] == loser]
        df_l2 = df_l2[df_l2['A_id'].isin(common_opponents)]

        performance_metrics = ['ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon', 'SvGms', 'bpSaved', 'bpFaced',
                               '2ndIn', 'bpWon', 'bpConv', '1stSvrptWon', '2ndSvrptWon', '1stServeWon',
                               '2ndServeWon', '1stServe', 'bpSavedratio']

        if len(common_opponents) >= 10:
            for metric in performance_metrics:
                val_w1 = df_w1['A_' + metric].sum()
                val_w2 = df_w2['B_' + metric].sum()

                mean_value_w = (val_w1 + val_w2) / (df_w1.shape[0] + df_w2.shape[0])

                val_l1 = df_l1['A_' + metric].sum()
                val_l2 = df_l2['B_' + metric].sum()

                mean_value_l = (val_l1 + val_l2) / (df_l1.shape[0] + df_l2.shape[0])

                difference = mean_value_w - mean_value_l
                df.at[num, metric + '_common_op'] = difference

        else:
            for metric in performance_metrics:
                df.at[num, metric + '_common_op'] = df[metric + '_career'][num]

    return df

######## RUN FUNCTIONS ########
def run_differences(df):
    path_1 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Differences.csv"
    print('Part 1')
    isFile_1 = os.path.isfile(path=path_1)
    if not isFile_1:
        df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
        df = get_differences_features(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Differences.csv")
    else:
        print('***COMPLETED***')

    path_2 = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/CommonOpponents.csv"
    print('Part 2')
    isFile_2 = os.path.isfile(path=path_2)
    if not isFile_2:
        df = pd.read_csv(path_1, low_memory=False)
        df = get_differences_for_common_opponent(df)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/CommonOpponents.csv")
    else:
        print('***COMPLETED***')
        df = pd.read_csv(path_2, low_memory=False)

    return df