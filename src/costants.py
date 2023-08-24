player_cols = ['Season','Player', 'Pos', 'Squad', 'Comp', 'Age',
        'Playing Time MP', 'Playing Time Starts', 'Playing Time Min',
        'Playing Time 90s', 'Performance Gls', 'Performance Ast', 'Performance PK',
        'Performance PKatt', 'Performance CrdY', 'Performance CrdR',
        'Expected xG', 'Expected npxG', 'Expected xAG',
        'Progression PrgC', 'Progression PrgP', 'Progression PrgR']

player_cols_type = {
        'Season':str, 'Player': str, 'Pos': str, 'Squad': str, 'Comp': str, 'Age':'int8',
        'Playing Time MP': 'int8', 'Playing Time Starts':'int8', 'Playing Time Min':'int16',
        'Playing Time 90s':'float32', 'Performance Gls':'int8', 'Performance Ast':'int8', 'Performance PK':'int8',
        'Performance PKatt':'int8', 'Performance CrdY':'int8', 'Performance CrdR':'int8',
        'Expected xG':'float32', 'Expected npxG':'float32', 'Expected xAG':'float32',
        'Progression PrgC':'int16', 'Progression PrgP':'int16', 'Progression PrgR':'int16'
}

player_cols_rename = {
        'Playing Time MP': 'Match_Played', 'Playing Time Starts':'Match_Started', 'Playing Time Min':'Min_Played',
        'Playing Time 90s': 'Avg_Min_Played', 'Performance Gls': 'Goal', 'Performance Ast': 'Assist', 'Performance PK': 'Penalties_Scored',
        'Performance PKatt': 'Penalties_Attempted', 'Performance CrdY':'YCards', 'Performance CrdR':'RCards',
        'Expected xG': 'xG', 'Expected npxG': 'npxG', 'Expected xAG':'xAG',
        'Progression PrgC': 'PrgC', 'Progression PrgP': 'PrgP', 'Progression PrgR': 'PrgR'
}



gk_cols = ['Season','Player','Pos', 'Squad', 'Comp', 'Age',
        'Playing Time MP', 'Playing Time Starts', 'Playing Time Min', '90s',
        'Performance GA', 'Performance SoTA',
        'Performance Saves', 'Performance Save%', 'Performance CS', 'Performance CS%',
        'Penalty Kicks PKatt', 'Penalty Kicks PKA', 'Penalty Kicks PKsv',
        'Penalty Kicks PKm', 'Penalty Kicks Save%']

gk_cols_type = {
        'Season': str,'Player': str, 'Pos': str, 'Squad': str, 'Comp': str, 'Age':'int8',
        'Playing Time MP': 'int8', 'Playing Time Starts': 'int8', 'Playing Time Min': 'int16', '90s': 'float32',
        'Performance GA': 'int16', 'Performance SoTA': 'int16',
        'Performance Saves': 'int16', 'Performance Save%': float, 'Performance CS': 'int8', 'Performance CS%': float,
        'Penalty Kicks PKatt': 'int16', 'Penalty Kicks PKA': 'int16', 'Penalty Kicks PKsv': 'int16',
        'Penalty Kicks PKm': 'int16', 'Penalty Kicks Save%': float}

gk_cols_rename = {
        'Playing Time MP': 'Match_Played', 'Playing Time Starts':'Match_Started', 'Playing Time Min':'Min_Played',
        '90s': 'Avg_Min_Played', 'Performance GA': 'Goal_Allowed', 'Performance SoTA': 'Shots_Target',
        'Performance Saves': 'Saves', 'Performance Save%': 'Save%', 'Performance CS': 'Clean_Sheets', 'Performance CS%': 'Clean_Sheets%',
        'Penalty Kicks PKatt': 'Penalties_Faced', 'Penalty Kicks PKA': 'Penalties_Allowed', 'Penalty Kicks PKsv': 'Penalties_Saves',
        'Penalty Kicks PKm': 'Penalties_Miss', 'Penalty Kicks Save%': 'Penalties_Save%'}

fanta_cols = ['Nome','Mv','Au']
fanta_cols_type = {'Nome':str,'Mv':'float32','Au': 'int8'}
fanta_cols_rename = {'Nome':'Player','Mv':'Avg_Fanta_Score','Au': 'Autogoal'}

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