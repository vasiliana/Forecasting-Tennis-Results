import pandas as pd

def check_null_values(df):
    null = (df.isnull().sum() / len(df)) * 100
    null = null.drop(null[null == 0].index).sort_values(ascending=False)
    missing_data = pd.DataFrame({'Percentage of Missing Values': null})
    return missing_data

def drop_unnecessary_info(df):
    """ score, A1 - A5, B1 - B5, minutes, Asets, Bsets
        indicate the result of the game and will add bias
        to the model, as it is information that is
        obtained when the match is completed.

        also, I don't want seed and entries """

    # uncomment to check for null_values
    #missing_data = check_null_values(df)
    #print(missing_data)

    df.drop(columns=['score', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5',
                     'Asets', 'Bsets', 'minutes'], inplace=True)
    df.drop(columns=['A_seed', 'B_seed', 'A_entry', 'B_entry'], inplace=True)
    df.drop(columns=['A_SJ', 'B_SJ', 'A_LB', 'B_LB', 'A_EX', 'B_EX'], inplace=True)

    # uncomment to check for null_values
    #missing_data = check_null_values(df)
    #print(missing_data)
    return df

def fill_null_values(df):
    df['A_Max'].fillna(df['A_Max'].mean(), inplace=True)
    df['B_Max'].fillna(df['B_Max'].mean(), inplace=True)
    df['A_Avg'].fillna(df['A_Avg'].mean(), inplace=True)
    df['B_Avg'].fillna(df['B_Avg'].mean(), inplace=True)
    df['A_ht'].fillna(df['A_ht'].mean(), inplace=True)
    df['B_ht'].fillna(df['B_ht'].mean(), inplace=True)
    df['A_PS'].fillna(df['A_PS'].mean(), inplace=True)
    df['B_PS'].fillna(df['B_PS'].mean(), inplace=True)
    df['A_B365'].fillna(df['A_B365'].mean(), inplace=True)
    df['B_B365'].fillna(df['B_B365'].mean(), inplace=True)
    df['A_rank_points'].fillna(df['A_rank_points'].mean(), inplace=True)
    df['B_rank_points'].fillna(df['B_rank_points'].mean(), inplace=True)
    df['A_rank'].fillna(df['A_rank'].mean(), inplace=True)
    df['B_rank'].fillna(df['B_rank'].mean(), inplace=True)
    df['A_SvGms'].fillna(df['A_SvGms'].mean(), inplace=True)
    df['B_SvGms'].fillna(df['B_SvGms'].mean(), inplace=True)
    df['A_bpFaced'].fillna(df['A_bpFaced'].mean(), inplace=True)
    df['B_bpFaced'].fillna(df['B_bpFaced'].mean(), inplace=True)
    df['A_bpSaved'].fillna(df['A_bpSaved'].mean(), inplace=True)
    df['B_bpSaved'].fillna(df['B_bpSaved'].mean(), inplace=True)
    df['A_2ndWon'].fillna(df['A_2ndWon'].mean(), inplace=True)
    df['B_2ndWon'].fillna(df['B_2ndWon'].mean(), inplace=True)
    df['A_1stIn'].fillna(df['A_1stIn'].mean(), inplace=True)
    df['B_1stIn'].fillna(df['B_1stIn'].mean(), inplace=True)
    df['A_svpt'].fillna(df['A_svpt'].mean(), inplace=True)
    df['B_svpt'].fillna(df['B_svpt'].mean(), inplace=True)
    df['A_df'].fillna(df['A_df'].mean(), inplace=True)
    df['B_df'].fillna(df['B_df'].mean(), inplace=True)
    df['A_ace'].fillna(df['A_ace'].mean(), inplace=True)
    df['B_ace'].fillna(df['B_ace'].mean(), inplace=True)
    df['A_1stWon'].fillna(df['A_1stWon'].mean(), inplace=True)
    df['B_1stWon'].fillna(df['B_1stWon'].mean(), inplace=True)

    # uncomment to check for null_values
    #missing_data = check_null_values(df)
    #print(missing_data)
    return df



