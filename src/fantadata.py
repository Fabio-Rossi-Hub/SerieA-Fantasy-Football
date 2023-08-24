import pandas as pd
import costants as const

def clean_player_data(raw_df:object, origin:str):
        clean_df = raw_df[const.col_selection[origin]]    
        clean_df = clean_df.astype(const.col_type[origin])
        clean_df = clean_df.rename(columns=const.col_rename[origin])
        return clean_df     

def get_player_stats_fbref(seasons:list, gk:bool=False):
    stats_type = 'keepers' if gk else 'stats'
    df_stats = None
    for year in seasons:
        url = 'https://fbref.com/en/comps/Big5/'+year+'/'+stats_type+'/players/'+year+'-Big-5-European-Leagues-Stats'

        partial_df = pd.read_html(url)[0]
        partial_df['Season'] = year
        df_stats = df_stats.append(partial_df, ignore_index=True) if df_stats else partial_df

    # creating a data with the same headers but without multi indexing
    df_stats.columns = [' '.join(col).strip() for col in df_stats.columns]

    df_stats = df_stats.reset_index(drop=True)

    # creating a list with new names
    new_columns = []
    for col in df_stats.columns:
        if 'level_0' in col:
            new_col = col.split()[-1]  # takes the last name
        else:
            new_col = col
        new_columns.append(new_col)

    # rename columns
    df_stats.columns = new_columns

    return df_stats

def get_player_fanta_score(seasons:list):
    df_scores = None
    for year in seasons:
        path = 'Data/Player Scores/Statistiche_Fantacalcio_Stagione_'+year[:4]+'_'+year[:-2]+'.xlsx'
        partial_df = pd.read_excel(path,skiprows=1, header=0)[0]
        partial_df['season'] = year
        df_scores = df_scores.append(partial_df, ignore_index=True) if df_scores else partial_df
    
    return df_scores




