import pandas as pd
import costants as const
import fanta_utils as futils
import os

class Fantadata:
    def __init__(self, seasons: list, championship: str):
        self.seasons = seasons
        self.championship = championship
        self.fanta_prices = self.fanta_scores_df  = self.fbref_df_gk = self.fbref_df_pl = None

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
            raw_df['Age'] = raw_df['Age'].apply(lambda x: x[:2] if isinstance(x, str) and len(x) > 2 else x)

        clean_df = raw_df[const.col_selection[origin]] 
        clean_df = clean_df.fillna(0)
        clean_df = clean_df.astype(const.col_type[origin])
        clean_df = clean_df.rename(columns=const.col_rename[origin])

        if origin in ['fbref_player', 'fbref_gk']:
            clean_df = clean_df.loc[clean_df['Comp'] == championship]
        return clean_df

    def add_player_stats_fbref(self, pos='fbref_player'):
        """
            Get player statistics from FBref.

        """
        
        stats =  []
        # Iterate over seasons to fetch data for each season's html page
        for year in self.seasons:
            #Goal keeper stats are different from other players and are stored in a different table
            
            url = 'https://fbref.com/en/comps/Big5/'+year+'/'+const.fbref_url_dict[pos]+'/players/'+year+'-Big-5-European-Leagues-Stats'
            
            season_df = pd.read_html(url)[0]
            season_df[('','Season')] = year
            stats.append(season_df)
            print('Season '+year+' added')
        
        stats = pd.concat(stats, ignore_index=True)    
        clean_df = self.clean_player_data(stats, pos, self.championship)
        
        if pos == 'fbref_player':
            self.fbref_df_pl = clean_df
        
        if pos == 'fbref_gk':
            self.fbref_df_gk = clean_df
        
        print("Fbred data downloaded for {pos}".format())

    def add_player_fanta_score(self):
        """
            Get player Fantacalcio scores.
        """
        df_scores = []
        # Iterate over seasons to fetch data for each season's excel workbook 
        for year in self.seasons:
            path = 'Data/Player Scores/Statistiche_Fantacalcio_Stagione_'+year[:4]+'_'+year[-2:]+'.xlsx'
            season_df = pd.read_excel(path,skiprows=1, header=0, sheet_name='Tutti')
            #Store season in a column
            season_df['Season'] = year
            df_scores.append(season_df)
            
            print('Season '+year+' added')
        df_scores = pd.concat(df_scores, ignore_index=True)
        self.fanta_scores_df = self.clean_player_data(df_scores, 'fanta_scores', self.championship).reset_index()

        print('Fanta Scores Added')

    def add_fanta_prices(self):
        df_prices = []
        dir = 'Data/Creator Strategies 2023-2024'
        file_list = os.listdir(dir)
        for file in file_list:
            creator_df = pd.read_excel(os.path.join(dir,file), sheet_name=None)
            # Concatenate all DataFrames in the list into a single DataFrame
            combined_creator_df = pd.concat([df for df in creator_df.values()], ignore_index=True)
            df_prices.append(combined_creator_df)
        df_prices = pd.concat(df_prices, ignore_index=True)
        df_prices = df_prices[['Team','Nome','Budget','PMAL']] 
        
        df_prices[['Budget','PMAL']] = combined_creator_df[['Budget','PMAL']].applymap(lambda x: float(x.strip('%'))/100 if isinstance(x, str) else x)
        self.fanta_prices = df_prices.groupby(['Team','Nome'], as_index=False).mean().rename(columns=const.prices_cols_rename)  
        


    def save_dfs_to_parquet(self, path:str, dfs:list[str]):
        '''Saves all dfs to parquet file'''
        if 'fanta' in dfs:
            self.fanta_scores_df.to_parquet(path+'fanta_scores.parquet', index=False)
        elif 'fbref_pl' in dfs:
            self.fbref_df_pl.to_parquet(path + 'fbref_stats_pl.parquet', index=False)
        elif 'fbref_gk' in dfs:
            self.fbref_df_gk.to_parquet(path + 'fbref_stats_gk.parquet', index=False)
        if 'prices' in dfs:
            self.fanta_prices.to_parquet(path+'fanta_prices.parquet', index=False)
    
    def add_new_seasons(self, path:str, seasons:list[str]):
        old_df = pd.read_parquet(path)
        old_df.reset_index(drop=True, inplace=True)
        new_df = None
        
        for year in set(seasons)  - set(self.seasons):
            if 'fanta' in path:
                url = 'Data/Player Scores/Statistiche_Fantacalcio_Stagione_'+year[:4]+'_'+year[-2:]+'.xlsx'
                season_df = pd.read_excel(path,skiprows=1, header=0, sheet_name='Tutti', engine='openpyxl')
                season_df['Season'] = year

            elif 'fbref_stats_pl' in path:
                url = 'https://fbref.com/en/comps/Big5/'+year+'/stats/players/'+year+'-Big-5-European-Leagues-Stats'
                season_df = pd.read_html(url)[0]
                season_df[('','Season')] = year
            
            
            #If first season then season df becomes df_scores, otherwise we append
            new_df = season_df if new_df is None else pd.concat([new_df, season_df], ignore_index=True)
            print('Season '+year+' added')

            if 'fanta' in path:
                clean_df = self.clean_player_data(new_df, 'fanta_scores', self.championship)
                old_df.reset_index(drop=True, inplace=True)
                clean_df.reset_index(drop=True, inplace=True)
                self.fanta_scores_df =  pd.concat([old_df, clean_df], axis=1) 
                
            elif 'fbref_stats_pl' in path:
                clean_df = self.clean_player_data(new_df, 'fbref_player', self.championship)
                old_df.reset_index(drop=True, inplace=True)
                clean_df.reset_index(drop=True, inplace=True)
                self.fbref_df_pl = pd.concat([old_df, clean_df], axis=0)

        self.seasons = list(set(self.seasons).union(set(seasons)))
        
        print('Data Added')



if __name__ == '__main__':

    seasons = ['2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023', '2023-2024' ]

    fdata = Fantadata(seasons, 'it Serie A')
    
    fdata.add_fanta_prices()
    fdata.fanta_prices.head()
    new_seasons = ['2023-2024']
    fdata.add_player_fanta_score()
    #fdata.add_new_seasons('Notebook/fbref_stats_pl.parquet', new_seasons)
    #fdata.add_new_seasons('Notebook/fanta_scores.parquet', new_seasons)


    fdata.save_dfs_to_parquet('Notebook/', ['fanta', 'prices'])
