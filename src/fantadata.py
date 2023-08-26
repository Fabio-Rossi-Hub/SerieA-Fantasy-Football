import pandas as pd
import costants as const
import fanta_utils as futils
class Fantadata:
    def __init__(self, seasons: list, championship: str):
        self.seasons = seasons
        self.championship = championship
        self.fanta_scores_df  = self.fbref_df = None

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
        if origin in  ['fbref_player', 'fbref_gk']:
            raw_df = futils.rename_fbref_columns(raw_df)

        clean_df = raw_df[const.col_selection[origin]] 
        clean_df = clean_df.fillna(0)
        clean_df = clean_df.astype(const.col_type[origin])
        clean_df = clean_df.rename(columns=const.col_rename[origin])

        if origin in ['fbref_player', 'fbref_gk']:
            clean_df = clean_df.loc[clean_df['Comp'] == championship]
        return clean_df

    def add_player_stats_fbref(self):
        """
            Get player statistics from FBref.
            Returns:
                pd.DataFrame: Player statistics.
        """
        gk_stats = pl_stats =  None
        # Iterate over seasons to fetch data for each season's html page
        for year in self.seasons:
            #Goal keeper stats are different from other players and are stored in a different table
            gk_url = 'https://fbref.com/en/comps/Big5/'+year+'/keepers/players/'+year+'-Big-5-European-Leagues-Stats'
            pl_url = 'https://fbref.com/en/comps/Big5/'+year+'/stats/players/'+year+'-Big-5-European-Leagues-Stats'
            
            gk_partial_df = pd.read_html(gk_url)[0]
            gk_partial_df[('','Season')] = year
            gk_stats = gk_partial_df if gk_stats is None else pd.concat([gk_stats, gk_partial_df], ignore_index=True) 

            pl_partial_df = pd.read_html(pl_url)[0]
            pl_partial_df[('','Season')] = year
            pl_stats = pl_partial_df if pl_stats is None else pd.concat([pl_stats, pl_partial_df], ignore_index=True)
            print('Season '+year+' added')

        self.fbref_df = {'pl': self.clean_player_data(pl_stats, 'fbref_player', self.championship),
                    'gk': self.clean_player_data(gk_stats, 'fbref_gk', self.championship)}
        
        print("Fbred data downloaded")

    def add_player_fanta_score(self):
        """
            Get player Fantacalcio scores.

            Args:
                seasons (list): List of seasons to fetch scores for.

            Returns:
                pd.DataFrame: Player Fantacalcio scores.
        """
        df_scores = None
        # Iterate over seasons to fetch data for each season's excel workbook 
        for year in self.seasons:
            path = 'Data/Player Scores/Statistiche_Fantacalcio_Stagione_'+year[:4]+'_'+year[-2:]+'.xlsx'
            partial_df = pd.read_excel(path,skiprows=1, header=0, sheet_name='Tutti')
            #Store season in a column
            partial_df['Season'] = year

            #If first season then partial df becomes df_scores, otherwise we append
            df_scores = partial_df if df_scores is None else pd.concat([df_scores, partial_df], ignore_index=True)
            
            print('Season '+year+' added')
        
        self.fanta_scores_df = self.clean_player_data(df_scores, 'fanta_scores', self.championship)

        print('Fanta Scores Added')
   
    def get_fbref_stats(self)-> pd.DataFrame:
        '''Returns fbref df stats'''
        return self.fbref_df
   
    def get_fanta_scores(self)-> pd.DataFrame:
        '''Returns fanta df scores'''
        return self.fanta_scores_df
    def save_fanta_scores(self, path: str):
        '''Saves fanta score df to parquet file'''
        self.fanta_scores_df.to_parquet(path+'fanta_scores.parquet', index=False)
    def save_dfs_to_parquet(self, path:str):
        '''Saves all dfs to parquet file'''
        self.fanta_scores_df.to_parquet(path+'fanta_scores.parquet', index=False)
        self.fbref_df['pl'].to_parquet(path + 'fbref_stats_pl.parquet', index=False)
        self.fbref_df['gk'].to_parquet(path + 'fbref_stats_gk.parquet', index=False)


if __name__ == '__main__':

    seasons = ['2015-2016', '2016-2017', '2017-2018', '2018-2019',
            '2019-2020', '2020-2021', '2021-2022','2022-2023']

    df = Fantadata(seasons, 'it Serie A')
    df.add_player_fanta_score()
    #df.add_player_stats_fbref()
    df.save_fanta_scores('Notebook/')
