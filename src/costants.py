player_cols = ['Season','Player', 'Pos', 'Squad', 'Comp', 'Age',
        'MP', 'Starts', 'Min', '90s', 'Gls', 'Ast', 'PK',
        'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG',
        'PrgC', 'PrgP', 'PrgR']

player_cols_type = {
        'Season':str, 'Player': str, 'Pos': str, 'Squad': str, 'Comp': str, 'Age':'int8',
        'MP': 'int8', 'Starts':'int8', 'Min':'int16',
        '90s':'float32', 'Gls':'int8', 'Ast':'int8', 'PK':'int8',
        'PKatt':'int8', 'CrdY':'int8', 'CrdR':'int8',
        'xG':'float32', 'npxG':'float32', 'xAG':'float32',
        'PrgC':'int16', 'PrgP':'int16', 'PrgR':'int16'
}

player_cols_rename = {
        'MP': 'Match_Played', 'Starts':'Match_Started', 'Min':'Min_Played',
        '90s': 'Avg_Min_Played', 'Gls': 'Goal', 'Ast': 'Assist', 'PK': 'Pen_Scored',
        'PKatt': 'Pen_Attempted', 'CrdY':'YCards', 'CrdR':'RCards',
        'xG': 'xG', 'npxG': 'npxG', 'xAG':'xAG',
        'PrgC': 'PrgC', 'PrgP': 'PrgP', 'PrgR': 'PrgR'
}



gk_cols = ['Season','Player','Pos', 'Squad', 'Comp', 'Age',
        'MP', 'Starts', 'Min', '90s', 'GA', 'SoTA',
        'Saves', 'Save%', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv',
        'PKm', 'PSave%']

gk_cols_type = {
        'Season': str,'Player': str, 'Pos': str, 'Squad': str, 'Comp': str, 'Age':'int8',
        'MP': 'int8', 'Starts': 'int8', 'Min': 'int16', '90s': 'float32',
        'GA': 'int16', 'SoTA': 'int16',
        'Saves': 'int16', 'Save%': float, 'CS': 'int8', 'CS%': float,
        'PKatt': 'int16', 'PKA': 'int16', 'PKsv': 'int16',
        'PKm': 'int16', 'PSave%': float}

gk_cols_rename = {
        'MP': 'Match_Played', 'Starts':'Match_Started', 'Min':'Min_Played',
        '90s': 'Avg_Min_Played', 'GA': 'Goal_Allowed', 'SoTA': 'Shots_Target',
        'Saves': 'Saves', 'Save%': 'Save%', 'CS': 'Clean_Sheets', 'CS%': 'Clean_Sheets%',
        'PKatt': 'Pen_Faced', 'PKA': 'Pen_Allowed', 'PKsv': 'Pen_Saves',
        'PKm': 'Pen_Miss', 'PSave%': 'Pen_Save%'}

fanta_cols = ['Season','Nome','Squadra','R','Pv', 'Mv', 'Gf', 'R-', 'Ass', 'Amm', 'Esp', 'Au']
fanta_cols_type = {'Season':str,'Nome':str,'R':str,'Mv':'float32','Au': 'int8'}
fanta_cols_rename = {'Nome':'Player','Squadra':'Squad','R': 'F_Pos','Mv':'Avg_Fanta_Score',
                'Pv':'Match_Played','Gf':'Goal', 'R-':'Pen_Missed', 'Ass':'Assist', 'Amm':'YCards', 'Esp':'RCards','Au': 'Autogoal'}

prices_cols_rename = {'Nome':'Player','Team':'Squad_b'}
col_selection = {'fbref_gk':gk_cols,
                'fbref_player':player_cols,
                'fanta_scores': fanta_cols
                }

col_rename= {'fbref_gk':gk_cols_rename,
                'fbref_player':player_cols_rename,
                'fanta_scores': fanta_cols_rename
                }

col_type= {'fbref_gk':gk_cols_type,
                'fbref_player':player_cols_type,
                'fanta_scores': fanta_cols_type
                }

fbref_url_dict = {'fbref_gk':'keepers',
                'fbref_player':'stats'}