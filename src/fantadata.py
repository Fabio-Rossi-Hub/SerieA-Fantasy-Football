import pandas as pd
import costants as const
import fanta_utils as futils
class Fantadata:
    def __init__(self, seasons: list, championship: str):
        self.seasons = seasons
        self.championship = championship 
    
    @staticmethod
    def clean_player_data(raw_df:pd.DataFrame, origin:str, championship: str)->pd.DataFrame:
        """
            Basic cleaning of player data based on its origin(fbref/fanta).

            Args:
                raw_df (pd.DataFrame): Raw data to be cleaned.
                origin (str): Origin/source of the data.

            Returns:
                pd.DataFrame: Cleaned data.
        """
        if 'fbrek' in origin:
            raw_df = futils.rename_fbref_columns(raw_df)
        clean_df = raw_df[const.col_selection[origin]]    
        clean_df = clean_df.astype(const.col_type[origin])
        clean_df = clean_df.rename(columns=const.col_rename[origin])

        return clean_df if 'fanta' in origin else clean_df[['Comp']== championship]     

    def add_player_stats_fbref(self):
        """
            Get player statistics from FBref.

            Args:
                seasons (list): List of seasons to fetch data for.
                gk (bool, optional): True if goalkeepers' stats are to be fetched. False for outfield players. Defaults to False.

            Returns:
                pd.DataFrame: Player statistics.
        """
        gk_stats = pl_stats =  None
        for year in self.seasons:
            gk_url = 'https://fbref.com/en/comps/Big5/'+year+'/keepers/players/'+year+'-Big-5-European-Leagues-Stats'
            pl_url = 'https://fbref.com/en/comps/Big5/'+year+'/stats/players/'+year+'-Big-5-European-Leagues-Stats'
            
            gk_partial_df = pd.read_html(gk_url)[0]
            gk_partial_df['Season'] = year
            gk_stats = gk_stats.append(gk_partial_df, ignore_index=True) if gk_stats else gk_partial_df

            pl_partial_df = pd.read_html(pl_url)[0]
            pl_partial_df['Season'] = year
            pl_stats = pl_stats.append(pl_partial_df, ignore_index=True) if pl_stats else pl_partial_df
        
        self.fbref_df = {'pl': self.clean_player_data(pl_stats, 'fbref_player', self.championship),
                    'gk': self.clean_player_data(pl_stats, 'fbref_gk', self.championship)}
        
        return "fbred data downloaded"

    def add_player_fanta_score(self):
        """
            Get player Fantacalcio scores.

            Args:
                seasons (list): List of seasons to fetch scores for.

            Returns:
                pd.DataFrame: Player Fantacalcio scores.
        """
        df_scores = None
        for year in self.seasons:
            path = 'Data/Player Scores/Statistiche_Fantacalcio_Stagione_'+year[:4]+'_'+year[:-2]+'.xlsx'
            partial_df = pd.read_excel(path,skiprows=1, header=0)[0]
            partial_df['season'] = year
            df_scores = df_scores.append(partial_df, ignore_index=True) if df_scores else partial_df
        
        self.fanta_scores_df = self.clean_player_data(df_scores, 'fanta_scores', self.championship)

        return 'Fanta Scores Processed'
    
    def get_fbref_stats(self)-> pd.DataFrame:
        return self.fbref_df
    
    def get_fanta_scores(self)-> pd.DataFrame:
        return self.fanta_scores_df



