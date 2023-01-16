# *-*-*-*-*-*-*-*-*-*-*-*-*-*-#
#        MAIN FUNCTION        #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-#

""" Πρόκειται για Classification Problem """
import datetime
import glob
import os
import warnings
import time
import numpy as np

import pandas as pd
from sklearn import set_config
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OrdinalEncoder

import data_loader
import data_null_handing
import data_engineering
import data_processor

import data_modeler
import data_eda_analysis
import data_feature_selection

pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
set_config(display="diagram")
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore')

SEED = 16

""" FIX IT TO WORK AS PIPELINE. ALL TOGETHER """


# 3. Revert dataset and get the final dataset
def get_final_dataset(df):
    print('\n🏁 🏁 🏁 REVERT DATASET')
    isFile = os.path.isfile(
        path="/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/extraction_final_reverted.csv")

    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(
            "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/extraction_final_reverted.csv",
            low_memory=False)

    else:
        df = data_engineering.get_reverted_dataset(df)
        df.to_csv(
            "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/extraction_final_reverted.csv")

    return df


# 4. Explanatory Data Analysis
def eda_analysis(df):
    print('\n🏁 🏁 🏁 EDA ANALYSIS')
    df = data_eda_analysis.eda_analysis(df)
    return df


# 5. Encode Categorical Values
def encode_features(df):
    print('\n🏁 🏁 🏁 ENCODE CATEGORICAL VALUES')
    df = data_feature_selection.encoder(df)

    return df


# 6. Create Datasets - the one with differences.
def create_datasets(df):
    df1 = df[['year', 'A_rank', 'B_rank',
              'Label']]
    # 'A_ace', 'B_ace', 'A_df', 'B_df', 'A_2ndWon', 'B_2ndWon', 'A_bpFaced', 'B_bpFaced',
    # 'A_2ndServeReturnPointsWon', 'B_2ndServeReturnPointsWon', 'A_bpWon', 'B_bpWon',
    # 'A_Wins_LastTwoWeeks', 'B_Wins_LastTwoWeeks', 'A_Losses_LastTwoWeeks', 'B_Losses_LastTwoWeeks',
    # 'A_Wins_tour', 'B_Wins_tour', 'A_Losses_tour', 'B_Losses_tour','Wins_of_A_over_B', 'Wins_of_B_over_A',
    # 'A_Surface_Percentage', 'B_Surface_Percentage', 'A_B365', 'B_B365',
    # 'A_Winning_Streak', 'B_Winning_Streak', 'A_Lossing_Streak', 'B_Lossing_Streak',
    # 'A_rank_points', 'B_rank_points',
    # 'series', 'round', 'A_hand', 'B_hand', 'surface_court', 'A_id', 'B_id', 'money_prize',
    # 'tourney_id', 'best_of', 'month', 'day_cos', 'day', 'A_ht', 'B_ht', 'A_age', 'B_age',
    # 'A_homeAdv', 'B_homeAdv', 'A_Wins_Career', 'B_Wins_Career', 'A_Losses_Career', 'B_Losses_Career',
    # 'A_Matches_Career', 'B_Matches_Career', 'A_Finals_Career', 'B_Finals_Career',
    # 'A_Titles_Career', 'B_Titles_Career', 'A_Wins_LastYear', 'B_Wins_LastYear',
    # 'A_Losses_LastYear', 'B_Losses_LastYear', 'A_Matches_LastYear', 'B_Matches_LastYear',
    # 'A_Finals_LastYear', 'B_Finals_LastYear', 'A_Titles_LastYear', 'B_Titles_LastYear',
    # 'A_Wins_LastSemester', 'B_Wins_LastSemester', 'A_Losses_LastSemester', 'B_Losses_LastSemester',
    # 'A_Matches_LastSemester', 'B_Matches_LastSemester', 'A_Finals_LastSemester', 'B_Finals_LastSemester',
    # 'A_Titles_LastSemester', 'B_Titles_LastSemester', 'A_Matches_LastTwoWeeks', 'B_Matches_LastTwoWeeks',
    # 'A_Finals_LastTwoWeeks', 'B_Finals_LastTwoWeeks', 'A_Titles_LastTwoWeeks', 'B_Titles_LastTwoWeeks',
    # 'A_Matches_tour', 'B_Matches_tour', 'A_Finals_tour', 'B_Finals_tour', 'A_Titles_tour', 'B_Titles_tour',
    # 'A_Wins_surface', 'B_Wins_surface', 'A_Losses_surface', 'B_Losses_surface',
    # 'A_Matches_surface', 'B_Matches_surface', 'A_Finals_surface', 'B_Finals_surface',
    # 'A_Titles_surface', 'B_Titles_surface', 'A_Inactivity', 'B_Inactivity', 'A_Elo', 'B_Elo',
    # 'A_Max', 'B_Max', 'A_Avg', 'B_Avg', 'A_spread_MaxAvg', 'B_spread_MaxAvg',
    # 'A_1stWon', 'B_1stWon', 'A_svpt', 'B_svpt', 'A_1stIn', 'B_1stIn',
    # 'A_bpSaved', 'B_bpSaved', 'A_SvGms', 'B_SvGms', 'A_2ndIn', 'B_2ndIn',
    # 'A_1stServeReturnPointsWon', 'B_1stServeReturnPointsWon',

    df2 = df[['series',
              'round',
              'surface_court',
              'money_prize',
              'best_of',
              'year',
              'month',
              'day_cos',
              'day',
              'Rank_Difference',
              'Rank_Difference_Log',
              'Rank_Points_Difference',
              'Rank_Points_Difference_Log',
              'Height_Difference',
              'Age_Difference',
              'Ace_Difference',
              'Df_Difference',
              'Svpt_Difference',
              '1stIn_Difference',
              '1stWon_Difference',
              '2ndWon_Difference',
              'SvGms_Difference',
              'bpSaved_Difference',
              'bpFaced_Difference',
              '2ndIn_Difference',
              '1stServeReturnPointsWon_Difference',
              '2ndServeReturnPointsWon_Difference',
              'bpWon_Difference',
              'Home_Advantage',
              'Wins_Career_Difference',
              'Losses_Career_Difference',
              'Matches_Career_Difference',
              'Finals_Career_Difference',
              'Titles_Career_Difference',
              'Wins_LastYear_Difference',
              'Losses_LastYear_Difference',
              'Matches_LastYear_Difference',
              'Finals_LastYear_Difference',
              'Titles_LastYear_Difference',
              'Wins_LastSemester_Difference',
              'Losses_LastSemester_Difference',
              'Matches_LastSemester_Difference',
              'Finals_LastSemester_Difference',
              'Titles_LastSemester_Difference',
              'Momentum_Difference',
              'Wins_LastTwoWeeks_Difference',
              'Losses_LastTwoWeeks_Difference',
              'Matches_LastTwoWeeks_Difference',
              'Finals_LastTwoWeeks_Difference',
              'Titles_LastTwoWeeks_Difference',
              'Winning_Streak_Difference',
              'Lossing_Streak_Difference',
              'Inactivity_Difference',
              'Proba_Elo',
              'Elo_Difference',
              'HeadToHead_Difference',
              'Duels',
              'Wins_Tournament_Difference',
              'Losses_Tournament_Difference',
              'Matches_Tournament_Difference',
              'Finals_Tournament_Difference',
              'Titles_Tournament_Difference',
              'Wins_Surface_Difference',
              'Losses_Surface_Difference',
              'Matches_Surface_Difference',
              'Finals_Surface_Difference',
              'Titles_Surface_Difference',
              'SurfaceAdv',
              'SpreadDif',
              'Label']]
    return df1, df2


# 7. Correlation with Target Value
def correlation_with_target(df, bool):
    print('\n🏁 🏁 🏁 CORRELATION WITH TARGET VALUE')
    data_feature_selection.corr_target(df, bool)
    return df


# 8. Correlation between all Variables
def correlation(df, bool):
    print('\n🏁 🏁 🏁 CORRELATION WITH ALL VARIABLES')
    data_feature_selection.corr_all(df, bool)
    return df


# Από την στιγμή που χρησιμοποιούμε features με ιστορικό περιεχόμενο τότε
# μάλλον θα πρέπει κατά το train_test_split να χωρίσουμε τα data ανά χρονιές (??)

# 9. Logistic Regression
def Logistic_Regression(df, split_method, scaler, pcaer, components, intercept, intercept_scaling):
    print('\n🏁 🏁 🏁 LOGISTIC REGRESSION')
    data_modeler.LogisticRegression_Modeler(df, split_method, scaler, pcaer, components, intercept, intercept_scaling)
    return


# 10. Decision Tree
def Decision_Tree(df, split_method, scaler, pcaer, components):
    print('\n🏁 🏁 🏁 BASELINE MODEL - DECISION TREE')
    data_modeler.DecisionTree_Modeler(df, split_method, scaler, pcaer, components)
    return


# 11. Random Forest
def Random_Forest(df, split_method, scaler, pcaer, components):
    print('\n🏁 🏁 🏁 BASELINE MODEL - RANDOM FOREST')
    data_modeler.RandomForest_Modeler(df, split_method, scaler, pcaer, components)
    return


# 12. Support Vector Machine
def Support_Vector_Machine(df, split_method, scaler, pcaer, components):
    print('\n🏁 🏁 🏁 BASELINE MODEL - SUPPORT VECTOR MACHINE')
    data_modeler.SVM_Modeler(df, split_method, scaler, pcaer, components)
    return


# 13. ADA Boost
def ADA_Boost(df, split_method, scaler, pcaer, components):
    print('\n🏁 🏁 🏁 BASELINE MODEL - ADA BOOOST')
    data_modeler.ADABoost_Modeler(df, split_method, scaler, pcaer, components)
    return


def Gradient_Boost_Machine(df, split_method, scaler, pcaer, components):
    print('\n🏁 🏁 🏁 BASELINE MODEL - GRADIENT BOOSTING MACHINE')
    data_modeler.GradientBoostingMachine_Modeler(df, split_method, scaler, pcaer, components)
    return


""" RUN CODE FROM HERE"""


# Pre-Modeling Functions
# matches = data_loading()
# df = pd.read_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FE.csv", low_memory=False)
# df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
# print(df.head(5))
def clean_null_values(df):
    # 1. drop tournament, country, location -> I have tourney_id for it
    df.drop(columns=['tournament', 'country', 'location'], inplace=True)
    # 2. drop score, A1 - A5, B1 - B5, Asets, Bsets, minutes -> this is information obtained after the match
    df.drop(columns=['score', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'Asets', 'Bsets', 'minutes'],
            inplace=True)
    # 3. drop name because I have the ID's
    df.drop(columns=['A_name', 'B_name'], inplace=True)
    # 4. I don't have seeds and entries for all players, so I consider dropping these columns.
    df.drop(columns=['A_seed', 'B_seed', 'A_entry', 'B_entry'], inplace=True)
    # 5. I don't care about the origin of the players
    df.drop(columns=['A_ioc', 'B_ioc'], inplace=True)
    # 6. drop betting odds LB, SJ
    df.drop(columns=['A_LB', 'B_LB', 'A_SJ', 'B_SJ'], inplace=True)
    # 7. I have created columns for surface, so I don't want the extra columns for every surface & court
    df.drop(columns=['A_wins_Hard_Outdoor', 'A_losses_Hard_Outdoor', 'A_matches_Hard_Outdoor', 'A_finals_Hard_Outdoor',
                     'A_titles_Hard_Outdoor', 'B_wins_Hard_Outdoor', 'B_losses_Hard_Outdoor', 'B_matches_Hard_Outdoor',
                     'B_finals_Hard_Outdoor', 'B_titles_Hard_Outdoor', 'A_wins_Hard_Indoor', 'A_losses_Hard_Indoor',
                     'A_matches_Hard_Indoor', 'A_finals_Hard_Indoor', 'A_titles_Hard_Indoor', 'B_wins_Hard_Indoor',
                     'B_losses_Hard_Indoor', 'B_matches_Hard_Indoor', 'B_finals_Hard_Indoor', 'B_titles_Hard_Indoor',
                     'A_wins_Grass_Outdoor', 'A_losses_Grass_Outdoor', 'A_matches_Grass_Outdoor',
                     'A_finals_Grass_Outdoor',
                     'A_titles_Grass_Outdoor', 'B_wins_Grass_Outdoor', 'B_losses_Grass_Outdoor',
                     'B_matches_Grass_Outdoor',
                     'B_finals_Grass_Outdoor', 'B_titles_Grass_Outdoor', 'A_wins_Clay_Outdoor', 'A_losses_Clay_Outdoor',
                     'A_matches_Clay_Outdoor', 'A_finals_Clay_Outdoor', 'A_titles_Clay_Outdoor', 'B_wins_Clay_Outdoor',
                     'B_losses_Clay_Outdoor', 'B_matches_Clay_Outdoor', 'B_finals_Clay_Outdoor',
                     'B_titles_Clay_Outdoor',
                     'A_wins_Clay_Indoor', 'A_losses_Clay_Indoor', 'A_matches_Clay_Indoor', 'A_finals_Clay_Indoor',
                     'A_titles_Clay_Indoor', 'B_wins_Clay_Indoor', 'B_losses_Clay_Indoor', 'B_matches_Clay_Indoor',
                     'B_finals_Clay_Indoor', 'B_titles_Clay_Indoor'], inplace=True)
    return df


# df = clean_null_values(df)
# print(df.head(5))
# print(df['A_surf_Per'].value_counts())
# print(df['A_surf_Per'].isnull().any())
""" feature engineering below"""
#
# matches = data_engineering.betting_features(df)
# start_time = datetime.datetime.now()
# end_time = datetime.datetime.now()
# elapsed_time = end_time - start_time
# print('Execution time:', str(elapsed_time))
# matches.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FE.csv")

# matches = get_final_dataset(matches)
# matches = eda_analysis(matches)
# matches = encode_features(matches)
# matches1, matches2 = create_datasets(matches)

# matches1 = correlation_with_target(matches1, '1')
# matches2 = correlation_with_target(matches2, '2')
# matches1 = correlation(matches1, '1')
# matches2 = correlation(matches2, '2')

"""
# Baseline Models
print('\n🏁 🏁 🏁 BASELINE MODEL')

matches_baseline = matches[['Rank_Points_Difference', 'Label']]     # add 'year' if you want to use method = 1

# DEFINE VARIABLES TO CALL MODELS
SPLIT_METHOD = "2"
SCALER = True
PCA = False
COMPONENTS = 5
INTERCEPT = False   # Set the intercept value - bias term - to 0 -> False. Else -> True
INTERCEPT_SCALING = 1

print('\nVARIABLES ON SET\nSPLIT_METHOD:                          ' + str(SPLIT_METHOD)
      + '\nSCALER:                                ' + str(SCALER)
      + '\nPCA:                                   ' + str(PCA)
      + '\nCOMPONENTS (PCA=True):                 ' + str(COMPONENTS)
      + '\nINTERCEPT:                             ' + str(INTERCEPT)
      + '\nINTERCEPT_SCALING (INTERCEPT=True):    ' + str(INTERCEPT_SCALING))

Logistic_Regression(matches_baseline, SPLIT_METHOD, SCALER, PCA, COMPONENTS, INTERCEPT, INTERCEPT_SCALING)

#Decision_Tree(matches1, SPLIT_METHOD, SCALER, PCA, COMPONENTS)

#Support_Vector_Machine(matches1, SPLIT_METHOD, SCALER, PCA, COMPONENTS)
#ADA_Boost(matches1, SPLIT_METHOD, SCALER, PCA, COMPONENTS)
#Gradient_Boost_Machine(matches1, SPLIT_METHOD, SCALER, PCA, COMPONENTS)


print('\n🏁 🏁 🏁 EXPERIMENTS WITH DIFFERENT MODELS')

matches_exp_RF = matches[['Rank_Points_Difference', 'Rank_Difference', 'money_prize', #'Rank_Difference_Log', 'Rank_Points_Difference_Log',
                          'Height_Difference', 'Age_Difference', #'Ace_Difference', 'Df_Difference', 'Svpt_Difference',
                          #'2ndWon_Difference', 'SvGms_Difference', '2ndIn_Difference', 'Wins_Career_Difference',
                          #'Wins_LastSemester_Difference', 'Matches_LastSemester_Difference',
                          #'Wins_LastTwoWeeks_Difference',
                          #'Losses_LastTwoWeeks_Difference',
                          #'Matches_LastTwoWeeks_Difference', 'Winning_Streak_Difference', 'Lossing_Streak_Difference',
                          'Inactivity_Difference',
                          #'Proba_Elo',
                          'HeadToHead_Difference', 'Losses_Tournament_Difference',
                          'Losses_Surface_Difference', 'SurfaceAdv', 'Label']]  # add 'year' if you want to use method = 1

# DEFINE VARIABLES TO CALL MODELS
SPLIT_METHOD = "2"
SCALER = False
PCA = False
COMPONENTS = 5
INTERCEPT = True  # Set the intercept value - bias term - to 0 -> False. Else -> True
INTERCEPT_SCALING = 1

print('\nVARIABLES ON SET\nSPLIT_METHOD:                          ' + str(SPLIT_METHOD)
      + '\nSCALER:                                ' + str(SCALER)
      + '\nPCA:                                   ' + str(PCA)
      + '\nCOMPONENTS (PCA=True):                 ' + str(COMPONENTS)
      + '\nINTERCEPT:                             ' + str(INTERCEPT)
      + '\nINTERCEPT_SCALING (INTERCEPT=True):    ' + str(INTERCEPT_SCALING))

Random_Forest(matches_exp_RF, SPLIT_METHOD, SCALER, PCA, COMPONENTS)
"""


# 1. Data Loading ----> OK
def data_loading():
    print("🏁 🏁 🏁 DATA LOADING")
    isFile = os.path.isfile("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/raw_dataset.csv")

    # if the file exists, just load the .csv to a dataframe
    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/raw_dataset.csv",
                         low_memory=False)
        df.drop(columns='Unnamed: 0', inplace=True)

    # if the file does not exist, run the appropriate functions
    else:
        start_time = datetime.datetime.now()
        # atp files
        atp_files = glob.glob(
            "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/ATP/atp_matches_" + "????.csv")
        atp_loader = data_loader.get_data_from_file(atp_files)
        # bet files
        bet_files = glob.glob("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/ATP/????.csv")
        bet_loader = data_loader.get_data_from_file(bet_files)
        # clean datasets, so as to merge them
        atp_cleaned = data_loader.get_cleaned_data(atp_loader, 'atp')
        bet_cleaned = data_loader.get_cleaned_data(bet_loader, 'bet')
        # merge datasets
        df = data_loader.merger_data(atp_cleaned, bet_cleaned)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/raw_dataset.csv")
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print('***COMPLETED***')
        print('Execution time:', str(elapsed_time))
    return df


# 2. Null Values Handling ---> OK
def null_handling(df):
    print("🏁 🏁 🏁 NULL VALUES HANDLING")
    start_time = datetime.datetime.now()
    df = data_null_handing.drop_unnecessary_info(df)
    df = data_null_handing.fill_null_values(df)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print('***COMPLETED***')
    print('Execution time:', str(elapsed_time))
    return df


# 3. Feature Engineering
def feature_engineering(df):
    print("\n🏁 🏁 🏁 FEATURE ENGINEERING")
    path = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/FeatEng_Final.csv"
    isFile = os.path.isfile(path=path)
    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(path, low_memory=False)
    else:
        df = data_engineering.run_feat_eng(df)
    return df


# 4. Complete Dataset
def get_final_dataset(df):
    print("\n🏁 🏁 🏁 FINAL COMPLETED DATASET")
    path = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Completed.csv"
    isFile = os.path.isfile(path=path)

    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(path, low_memory=False)
    else:
        df = data_processor.get_final_dataset(df)

    return df


# 5. Differences
def get_differences(df):
    print("\n🏁 🏁 🏁 DIFFERENCES")
    path = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/CommonOpponents.csv"
    isFile = os.path.isfile(path=path)
    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(path, low_memory=False)
    else:
        df = data_engineering.run_differences(df)
    return df


# 6. Encoding
def get_encoding(df):
    print("\n🏁 🏁 🏁 ENCODING")
    path = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Encoded.csv"
    isFile = os.path.isfile(path=path)
    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(path, low_memory=False)
    else:
        df.drop(columns=['match_index', 'Unnamed: 0', 'Unnamed: 0.1', 'tournament', 'tourney_date',
                         'country', 'surface', 'court',
                         'A_name', 'B_name', 'A_ioc', 'B_ioc', 'A_ace', 'B_ace', 'A_df', 'B_df', 'A_svpt', 'B_svpt',
                         'A_1stIn', 'B_1stIn', 'A_1stWon', 'B_1stWon', 'A_2ndWon', 'B_2ndWon', 'A_SvGms', 'B_SvGms',
                         'A_bpSaved', 'B_bpSaved', 'A_bpFaced', 'B_bpFaced', 'A_PS', 'B_PS', 'A_Max', 'B_Max',
                         'A_Avg', 'B_Avg', 'A_2ndIn', 'B_2ndIn', 'A_bpWon', 'B_bpWon', 'A_bpConv', 'B_bpConv',
                         'A_1stSvrptWon', 'B_1stSvrptWon', 'A_2ndSvrptWon', 'B_2ndSvrptWon',
                         'A_1stServeWon', 'B_1stServeWon', 'A_2ndServeWon', 'B_2ndServeWon',
                         'A_1stServe', 'B_1stServe', 'A_bpSavedratio', 'B_bpSavedratio'], inplace=True)

        cat_list_enc = ['series', 'round', 'location', 'surface_court', 'preferred_hand', 'A_hand', 'B_hand']

        encoder = OrdinalEncoder()
        df[cat_list_enc] = df[cat_list_enc].astype(str)
        encoder.fit(df[cat_list_enc])
        df[cat_list_enc] = encoder.transform(df[cat_list_enc])

        df.fillna(0, inplace=True)
        df.replace(np.inf, 0, inplace=True)
        df.replace(-np.inf, 0, inplace=True)
        df.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Encoded.csv")
    return df

# 7. Get Datasets
def get_datasets(df):
    Dataset_No1 = df[['A_id', 'B_id', 'tourney_id', 'A_wins_tour', 'B_wins_tour', 'A_losses_tour',
                      'B_losses_tour', 'A_matches_tour', 'B_matches_tour', 'A_finals_tour', 'B_finals_tour',
                      'A_titles_tour', 'B_titles_tour', 'A_tour_percentage', 'B_tour_percentage',
                      'surface_court', 'A_matches_per_surface', 'B_matches_per_surface', 'A_wins_per_surface',
                      'B_wins_per_surface', 'A_losses_per_surface', 'B_losses_per_surface', 'A_finals_per_surface',
                      'B_finals_per_surface', 'A_titles_per_surface', 'B_titles_per_surface', 'A_surface_percentage',
                      'B_surface_percentage', 'draw_size', 'series', 'money_prize', 'tourney_date', 'year', 'month',
                      'day', 'match_num', 'best_of', 'round', 'A_round_wins', 'B_round_wins', 'A_round_losses',
                      'B_round_losses', 'A_round_matches', 'B_round_matches', 'A_round_percentage',
                      'B_round_percentage',
                      'A_hand', 'B_hand', 'preferred_hand', 'A_ace', 'B_ace', 'A_df', 'B_df', 'A_svpt', 'B_svpt',
                      'A_1stIn', 'A_1stWon', 'A_2ndWon', 'A_SvGms', 'B_SvGms', 'A_bpSaved', 'B_bpSaved', 'A_bpFaced',
                      'B_bpFaced', 'A_AceVsDf_percentage', 'B_AceVsDf_percentage', 'A_2ndIn', 'B_2ndIn',
                      'A_1stServeReturnPointsWon', 'B_1stServeReturnPointsWon', 'A_2ndServeReturnPointsWon',
                      'B_2ndServeReturnPointsWon', 'A_2ndWon_2ndIn_percentage', 'B_2ndWon_2ndIn_percentage',
                      'A_1stWon_1stIn_percentage', 'B_1stWon_1stIn_percentage', 'A_1stIn_1stServe_percentage',
                      'B_1stIn_1stServe_percentage', 'A_bpSaved_percentage', 'B_bpSaved_percentage',
                      'A_1stServe_percentage', 'B_1stServe_percentage', 'A_1stSPWon_percentage',
                      'B_1stSPWon_percentage',
                      'A_2ndSPWon_percentage', 'B_2ndSPWon_percentage', 'A_1stSRPWon', 'B_1stSRPWon', 'A_2ndSRPWon',
                      'B_2ndSRPWon', 'A_1stSRPWon_percentage', 'B_1stSRPWon_percentage', 'A_2ndSRPWon_percentage',
                      'B_2ndSRPWon_percentage', 'A_bpWon_percentage', 'B_bpWon_percentage', 'A_bpWon', 'B_bpWon',
                      'A_bpConv_percentage', 'B_bpConv_percentage', 'match_quality', 'A_rank', 'B_rank',
                      'A_rank_points',
                      'B_rank_points', 'A_rank_log', 'B_rank_log', 'A_rank_points_log', 'B_rank_points_log',
                      'A_elo_rating', 'B_elo_rating', 'A_B365', 'B_B365', 'A_PS', 'B_PS', 'A_Max', 'B_Max', 'A_Avg',
                      'B_Avg', 'A_spread', 'B_spread', 'A_wins_career', 'B_wins_career', 'A_losses_career',
                      'B_losses_career', 'A_matches_career', 'B_matches_career', 'A_finals_career', 'B_finals_career',
                      'A_titles_career', 'B_titles_career', 'A_wins_year', 'B_wins_year', 'A_losses_year',
                      'B_losses_year', 'A_matches_year', 'B_matches_year', 'A_finals_year', 'B_finals_year',
                      'A_titles_year', 'B_titles_year', 'A_past_games_percentage',
                      'B_past_games_percentage', 'A_wins_semester', 'B_wins_semester',
                      'A_losses_semester', 'B_losses_semester', 'A_matches_semester', 'B_matches_semester',
                      'A_momentum', 'B_momentum', 'A_wins_recent', 'B_wins_recent', 'A_losses_recent',
                      'B_losses_recent',
                      'A_matches_recent', 'B_matches_recent', 'A_winning_streak', 'B_winning_streak',
                      'A_lossing_streak', 'B_lossing_streak', 'A_inactivity', 'B_inactivity',
                      'headtohead', 'A_over_B', 'B_over_A', 'A_oppon_percentage', 'B_oppon_percentage', 'Label']]

    Dataset_No2 = df[['A_id', 'B_id', 'tourney_id', 'wins_tour', 'losses_tour', 'matches_tour', 'finals_tour',
                      'titles_tour', 'tour_percentage', 'surface_court', 'matches_per_surface', 'wins_per_surface',
                      'losses_per_surface', 'finals_per_surface', 'titles_per_surface',
                      'surface_advantage', 'surface_percentage', 'draw_size', 'series', 'money_prize', 'tourney_date',
                      'year', 'month', 'day', 'match_num', 'best_of', 'round', 'round_wins', 'round_losses',
                      'round_matches', 'round_percentage', 'preferred_hand', 'ace', 'df', 'svpt', '1stIn', '1stWon',
                      '2ndWon', 'SvGms', 'bpSaved', 'bpFaced', '2ndIn', '1stServeReturnPointsWon',
                      '2ndServeReturnPointsWon', '1stSRPWon', '2ndSRPWon', 'bpWon', 'aceVsDf_percentage',
                      '2ndWon_2ndIn_percentage', '1stWon_1stIn_percentage', '1stIn_1stServe_percentage',
                      'bpSaved_percentage', '1stServe_percentage', '1stSPWon_percentage',
                      '2ndSPWon_percentage', '1stSRPWon_percentage',
                      '2ndSRPWon_percentage', 'bpWon_percentage', 'bpConv_percentage', 'match_quality', 'rank',
                      'rank_log', 'rank_points_log', 'spread', 'B365', 'PS', 'Max', 'Avg',
                      'wins_career', 'losses_career', 'matches_career', 'finals_career', 'titles_career', 'wins_year',
                      'losses_year', 'matches_year', 'finals_year', 'titles_year',
                      'past_games_percentage', 'wins_semester', 'losses_semester', 'matches_semester', 'momentum',
                      'wins_recent', 'losses_recent', 'matches_recent', 'winning_streak', 'lossing_streak',
                      'inactivity', 'oppon_percentage', 'Label']]

    Dataset_No3 = df[['A_id', 'B_id', 'tourney_id', 'wins_tour_opp', 'losses_tour_opp', 'matches_tour_opp',
                      'finals_tour_opp', 'titles_tour_opp', 'tour_percentage', 'surface_court',
                      'matches_per_surface_opp', 'wins_per_surface_opp', 'losses_per_surface_opp', 'finals_per_surface_opp',
                      'titles_per_surface_opp', 'surface_advantage', 'surface_percentage',
                      'draw_size', 'series', 'money_prize', 'tourney_date', 'year', 'month', 'day', 'match_num',
                      'best_of', 'round', 'round_wins_opp', 'round_losses_opp', 'round_matches_opp', 'round_percentage',
                      'preferred_hand', 'ace_opp', 'df_opp', 'svpt_opp', '1stIn_opp', '1stWon_opp', '2ndWon_opp', 'SvGms_opp',
                      'bpSaved_opp', 'bpFaced_opp', '2ndIn_opp',
                      '1stServeReturnPointsWon_opp', '2ndServeReturnPointsWon_opp', '1stSRPWon_opp', '2ndSRPWon_opp',
                      'bpWon_opp', 'aceVsDf_percentage', '2ndWon_2ndIn_percentage', '1stWon_1stIn_percentage',
                      '1stIn_1stServe_percentage', 'bpSaved_percentage',
                      '1stServe_percentage', '1stSPWon_percentage', '2ndSPWon_percentage', '1stSRPWon_percentage',
                      '2ndSRPWon_percentage', 'bpWon_percentage', 'bpConv_percentage', 'match_quality', 'rank',
                      'rank_log',  'rank_points_log', 'spread', 'B365', 'PS', 'Max', 'Avg',
                      'wins_career_opp', 'losses_career_opp', 'matches_career_opp', 'finals_career_opp',
                      'titles_career_opp',  'wins_year_opp', 'losses_year_opp',
                      'matches_year_opp', 'finals_year_opp', 'titles_year_opp', 'past_games_percentage',
                      'wins_semester_opp', 'losses_semester_opp', 'matches_semester_opp',
                      'momentum', 'wins_recent_opp', 'losses_recent_opp', 'matches_recent_opp', 'winning_streak_opp',
                      'lossing_streak_opp', 'inactivity_opp', 'oppon_percentage', 'Label']]

    return Dataset_No1, Dataset_No2, Dataset_No3

def run_main():
    """
    1. Dataset Loading from files
    2. Drop unnecessary columns from the loaded dataset
    3. Feature Engineering
    """
    # 1. Loading : Execution time: 0:00:08
    df = data_loading()
    # 2. Drop unnecessary columns
    df = null_handling(df)
    # 3. Feature Engineering
    df.sort_values(['tourney_date', 'tourney_id', 'match_num'], ascending=True, inplace=True)
    df.index.name = 'match_index'
    df.reset_index(level=0, inplace=True)
    df = feature_engineering(df)
    # 4. Get Final Complete Dataset
    df = get_final_dataset(df)
    # 5. Get Differences
    df = get_differences(df)
    # 6. Get Encoded Values
    df = get_encoding(df)
    # 7. Split Datasets
    #df1, df2, df3 = get_datasets(df)
    #print('Shape of DF1: ', df1.shape)
    #print('Shape of DF2: ', df2.shape)
    #print('Shape of DF3: ', df3.shape)
    # 8. Modeling
    #''' df: dataset to use , year: year for split, test_size - random_state: for sklearn.train_test_split,
    #    split_method: {1,2}, scaler: {True, False}, pcaer: {True, False}, components for pca, name for file saving'''
    #data_modeler.LogisticRegression_Modeler(data=df1, model=LogisticRegression(), year=2019, test_size=0.3, random_state=0,
                                            #split_method=2, scaler=True, pcaer=True, name='[df1][testsize03][sc][pca160]',
                                            #n_components=160)


    return df

matches = run_main()
