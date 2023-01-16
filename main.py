import datetime
import glob
import os
import warnings
import numpy as np

import pandas as pd
from sklearn import set_config
from sklearn.preprocessing import OrdinalEncoder

import data_loader
import data_null_handing
import data_engineering
import data_processor

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
        atp_files = glob.glob("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Dataset/ATP/atp_matches_" + "????.csv")
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


# 3. Feature Engineering ---> OK
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


# 4. Complete Dataset ---> OK
def get_final_dataset(df):
    """
    get balanced dataset with same number of target values {0,1}
    """
    print("\n🏁 🏁 🏁 FINAL COMPLETED DATASET")
    path = "/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/Completed.csv"
    isFile = os.path.isfile(path=path)

    if isFile:
        print('***COMPLETED***')
        df = pd.read_csv(path, low_memory=False)
    else:
        df = data_processor.get_final_dataset(df)

    return df


# 5. Differences ---> OK
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


# 6. Encoding  ---> OK
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


def run_main():
    """
    1. Dataset Loading from files
    2. Drop unnecessary columns from the loaded dataset
    3. Feature Engineering
    4. Get Balanced Dataset
    5. Feature Engineering for Differences and Common Opponent Features
    6. Encode Categorical Features
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
    return df

matches = run_main()
