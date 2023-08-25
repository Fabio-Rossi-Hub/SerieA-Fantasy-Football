import pandas as pd
def rename_fbref_columns(df: pd.DataFrame) -> pd.DataFrame:
    # creating a data with the same headers but without multi indexing
    df.columns = [' '.join(col).strip() for col in df.columns]

    df = df.reset_index(drop=True)

    # creating a list with new names
    new_columns = []
    for col in df.columns:
        if 'level_0' in col:
            new_col = col.split()[-1]  # takes the last name
        else:
            new_col = col
        new_columns.append(new_col)

    # rename columns
    df.columns = new_columns
    return df