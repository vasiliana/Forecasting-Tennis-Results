import pandas as pd

def create_label(df):
    df['Label'] = 1
    return df

def get_final_dataset(df):
    # Create Label
    df = create_label(df)

    # Cut the dataset in two parts in a random way
    half_df1 = df.sample(frac=0.5)
    half_df2 = df.drop(half_df1.index)

    half_df2.rename(columns={'A_id': 'B_id', 'B_id': 'A_id', 'A_name': 'B_name', 'B_name': 'A_name',
                             'A_rank': 'B_rank', 'B_rank': 'A_rank', 'A_ht': 'B_ht', 'B_ht': 'A_ht',
                             'A_ioc': 'B_ioc', 'B_ioc': 'A_ioc', 'A_age': 'B_age', 'B_age': 'A_age',
                             'A_hand': 'B_hand', 'B_hand': 'A_hand',

                             'A_ace': 'B_ace', 'B_ace': 'A_ace',
                             'A_df': 'B_df', 'B_df': 'A_df',
                             'A_svpt': 'B_svpt', 'B_svpt': 'A_svpt',
                             'A_1stIn': 'B_1stIn', 'B_1stIn': 'A_1stIn',
                             'A_1stWon': 'B_1stWon', 'B_1stWon': 'A_1stWon',
                             'A_2ndWon': 'B_2ndWon', 'B_2ndWon': 'A_2ndWon',
                             'A_SvGms': 'B_SvGms', 'B_SvGms': 'A_SvGms',
                             'A_bpSaved': 'B_bpSaved', 'B_bpSaved': 'A_bpSaved',
                             'A_bpFaced': 'B_bpFaced', 'B_bpFaced': 'A_bpFaced',

                             'A_rank_points': 'B_rank_points', 'B_rank_points': 'A_rank_points',
                             'A_B365': 'B_B365', 'B_B365': 'A_B365', 'A_PS': 'B_PS', 'B_PS': 'A_PS',
                             'A_Max': 'B_Max', 'B_Max': 'A_Max', 'A_Avg': 'B_Avg', 'B_Avg': 'A_Avg',

                             'A_rank_log': 'B_rank_log', 'B_rank_log': 'A_rank_log',
                             'A_rank_points_log': 'B_rank_points_log', 'B_rank_points_log': 'A_rank_points_log',
                             'A_spread': 'B_spread', 'B_spread': 'A_spread',
                             'A_wins_career': 'B_wins_career', 'B_wins_career': 'A_wins_career',
                             'A_losses_career': 'B_losses_career', 'B_losses_career': 'A_losses_career',
                             'A_matches_career': 'B_matches_career', 'B_matches_career': 'A_matches_career',
                             'A_titles_career': 'B_titles_career', 'B_titles_career': 'A_titles_career',
                             'A_wins_year': 'B_wins_year', 'B_wins_year': 'A_wins_year',
                             'A_losses_year': 'B_losses_year', 'B_losses_year': 'A_losses_year',
                             'A_matches_year': 'B_matches_year', 'B_matches_year': 'A_matches_year',
                             'A_titles_year': 'B_titles_year', 'B_titles_year': 'A_titles_year',
                             'A_matches_year_per': 'B_matches_year_per', 'B_matches_year_per': 'A_matches_year_per',
                             'A_wins_semester': 'B_wins_semester', 'B_wins_semester': 'A_wins_semester',
                             'A_losses_semester': 'B_losses_semester', 'B_losses_semester': 'A_losses_semester',
                             'A_matches_semester': 'B_matches_semester', 'B_matches_semester': 'A_matches_semester',
                             'A_titles_semester': 'B_titles_semester', 'B_titles_semester': 'A_titles_semester',
                             'A_wins_recent': 'B_wins_recent', 'B_wins_recent': 'A_wins_recent',
                             'A_losses_recent': 'B_losses_recent', 'B_losses_recent': 'A_losses_recent',
                             'A_matches_recent': 'B_matches_recent', 'B_matches_recent': 'A_matches_recent',
                             'A_titles_recent': 'B_titles_recent', 'B_titles_recent': 'A_titles_recent',
                             'A_matches_per_surface': 'B_matches_per_surface', 'B_matches_per_surface': 'A_matches_per_surface',
                             'A_wins_per_surface': 'B_wins_per_surface', 'B_wins_per_surface': 'A_wins_per_surface',
                             'A_losses_per_surface': 'B_losses_per_surface', 'B_losses_per_surface': 'A_losses_per_surface',
                             'A_titles_per_surface': 'B_titles_per_surface', 'B_titles_per_surface': 'A_titles_per_surface',
                             'A_surface_per': 'B_surface_per', 'B_surface_per': 'A_surface_per',
                             'A_wins_tour': 'B_wins_tour', 'B_wins_tour': 'A_wins_tour',
                             'A_losses_tour': 'B_losses_tour', 'B_losses_tour': 'A_losses_tour',
                             'A_matches_tour': 'B_matches_tour', 'B_matches_tour': 'A_matches_tour',
                             'A_titles_tour': 'B_titles_tour', 'B_titles_tour': 'A_titles_tour',
                             'A_tour_per': 'B_tour_per', 'B_tour_per': 'A_tour_per',
                             'A_round_wins': 'B_round_wins', 'B_round_wins': 'A_round_wins',
                             'A_round_losses': 'B_round_losses', 'B_round_losses': 'A_round_losses',
                             'A_round_matches': 'B_round_matches', 'B_round_matches': 'A_round_matches',
                             'A_round_per': 'B_round_per', 'B_round_per': 'A_round_per',
                             'A_elo_rating': 'B_elo_rating', 'B_elo_rating': 'A_elo_rating',
                             'A_ratio_ace/df_year': 'B_ratio_ace/df_year', 'B_ratio_ace/df_year': 'A_ratio_ace/df_year',
                             'A_2ndIn': 'B_2ndIn', 'B_2ndIn': 'A_2ndIn',
                             'A_bpWon': 'B_bpWon', 'B_bpWon': 'A_bpWon',
                             'A_bpConv': 'B_bpConv', 'B_bpConv': 'A_bpConv',
                             'A_1stSvrptWon': 'B_1stSvrptWon', 'B_1stSvrptWon': 'A_1stSvrptWon',
                             'A_2ndSvrptWon': 'B_2ndSvrptWon', 'B_2ndSvrptWon': 'A_2ndSvrptWon',
                             'A_1stServeWon': 'B_1stServeWon',  'B_1stServeWon': 'A_1stServeWon',
                             'A_2ndServeWon': 'B_2ndServeWon', 'B_2ndServeWon': 'A_2ndServeWon',
                             'A_1stServe': 'B_1stServe', 'B_1stServe': 'A_1stServe',
                             'A_bpSavedratio': 'B_bpSavedratio', 'B_bpSavedratio': 'A_bpSavedratio',

                             'A_ace_career': 'B_ace_career', 'B_ace_career': 'A_ace_career',
                             'A_df_career': 'B_df_career', 'B_df_career': 'A_df_career',
                             'A_svpt_career': 'B_svpt_career', 'B_svpt_career': 'A_svpt_career',
                             'A_1stIn_career': 'B_1stIn_career', 'B_1stIn_career': 'A_1stIn_career',
                             'A_1stWon_career': 'B_1stWon_career', 'B_1stWon_career': 'A_1stWon_career',
                             'A_2ndWon_career': 'B_2ndWon_career', 'B_2ndWon_career': 'A_2ndWon_career',
                             'A_SvGms_career': 'B_SvGms_career', 'B_SvGms_career': 'A_SvGms_career',
                             'A_bpSaved_career': 'B_bpSaved_career', 'B_bpSaved_career': 'A_bpSaved_career',
                             'A_bpFaced_career': 'B_bpFaced_career', 'B_bpFaced_career': 'A_bpFaced_career',
                             'A_2ndIn_career': 'B_2ndIn_career', 'B_2ndIn_career': 'A_2ndIn_career',
                             'A_1stSvrptWon_career': 'B_1stSvrptWon_career', 'B_1stSvrptWon_career': 'A_1stSvrptWon_career',
                             'A_2ndSvrptWon_career': 'B_2ndSvrptWon_career', 'B_2ndSvrptWon_career': 'A_2ndSvrptWon_career',
                             'A_1stServeWon_career': 'B_1stServeWon_career', 'B_1stServeWon_career': 'A_1stServeWon_career',
                             'A_2ndServeWon_career': 'B_2ndServeWon_career', 'B_2ndServeWon_career': 'A_2ndServeWon_career',
                             'A_1stServe_career': 'B_1stServe_career', 'B_1stServe_career': 'A_1stServe_career',
                             'A_bpSavedratio_career': 'B_bpSavedratio_career', 'B_bpSavedratio_career': 'A_bpSavedratio_career',
                             'A_bpWon_career': 'B_bpWon_career', 'B_bpWon_career': 'A_bpWon_career',
                             'A_bpConv_career': 'B_bpConv_career', 'B_bpConv_career': 'A_bpConv_career',

                             'A_ace_year': 'B_ace_year', 'B_ace_year': 'A_ace_year',
                             'A_df_year': 'B_df_year', 'B_df_year': 'A_df_year',
                             'A_svpt_year': 'B_svpt_year', 'B_svpt_year': 'A_svpt_year',
                             'A_1stIn_year': 'B_1stIn_year', 'B_1stIn_year': 'A_1stIn_year',
                             'A_1stWon_year': 'B_1stWon_year', 'B_1stWon_year': 'A_1stWon_year',
                             'A_2ndWon_year': 'B_2ndWon_year', 'B_2ndWon_year': 'A_2ndWon_year',
                             'A_SvGms_year': 'B_SvGms_year', 'B_SvGms_year': 'A_SvGms_year',
                             'A_bpSaved_year': 'B_bpSaved_year', 'B_bpSaved_year': 'A_bpSaved_year',
                             'A_bpFaced_year': 'B_bpFaced_year', 'B_bpFaced_year': 'A_bpFaced_year',
                             'A_2ndIn_year': 'B_2ndIn_year', 'B_2ndIn_year': 'A_2ndIn_year',
                             'A_1stSvrptWon_year': 'B_1stSvrptWon_year', 'B_1stSvrptWon_year': 'A_1stSvrptWon_year',
                             'A_2ndSvrptWon_year': 'B_2ndSvrptWon_year', 'B_2ndSvrptWon_year': 'A_2ndSvrptWon_year',
                             'A_1stServeWon_year': 'B_1stServeWon_year', 'B_1stServeWon_year': 'A_1stServeWon_year',
                             'A_2ndServeWon_year': 'B_2ndServeWon_year', 'B_2ndServeWon_year': 'A_2ndServeWon_year',
                             'A_1stServe_year': 'B_1stServe_year', 'B_1stServe_year': 'A_1stServe_year',
                             'A_bpSavedratio_year': 'B_bpSavedratio_year', 'B_bpSavedratio_year': 'A_bpSavedratio_year',
                             'A_bpWon_year': 'B_bpWon_year', 'B_bpWon_year': 'A_bpWon_year',
                             'A_bpConv_year': 'B_bpConv_year', 'B_bpConv_year': 'A_bpConv_year',
                             'A_over_B': 'B_over_A', 'B_over_A': 'A_over_B',
                             'A_Win_oppon': 'B_Win_oppon', 'B_Win_oppon': 'A_Win_oppon',
                             'A_momentum': 'B_momentum', 'B_momentum': 'A_momentum',
                             'A_wstreak': 'B_wstreak', 'B_wstreak': 'A_wstreak',
                             'A_lstreak': 'B_lstreak', 'B_lstreak': 'A_lstreak',
                             'A_days_inactive': 'B_days_inactive', 'B_days_inactive': 'A_days_inactive'},
                    inplace=True)
    half_df2['Label'] = 0
    half_df1.sort_values(['match_index'], inplace=True)
    half_df1.to_csv('/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/New/half1.csv')
    half_df2.sort_values(['match_index'], inplace=True)
    half_df2.to_csv('/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/New/half2.csv')

    concat_dataset = pd.concat([half_df1, half_df2])
    concat_dataset.sort_values(['match_index'], inplace=True)
    concat_dataset.to_csv("/Users/vasilianaroidouli/Desktop/Forecasting_Tennis_Results/Output/Feature_Engineering/New/Completed.csv")
    return concat_dataset