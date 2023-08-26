import pandas as pd
def rename_fbref_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Extract the second part of the tuple for each column
    if ('Penalty Kicks', 'Save%') in df.columns.to_list():
        

        df.columns = df.columns.to_series().replace(('Penalty Kicks', 'Save%'), ('Penalty Kicks', 'PSave%'))

    print(df)
    new_columns = [col[1] if '90' not in col[0] else col[0] for col in df.columns]

    # Rename the columns with the new names
    df.columns = new_columns

    mask = df.apply(lambda row: 'Player' in row.values, axis=1)
    df = df[~mask]

    df = df.reset_index(drop=True)

    return df
