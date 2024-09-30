# data_processing.py

import pandas as pd

def clean_player_data(df):
    """
    Cleans and formats player data.

    Parameters:
    df (DataFrame): The raw player data.

    Returns:
    DataFrame: The cleaned player data.
    """
    # Convert 'height' to numeric (meters)
    df['height'] = pd.to_numeric(
        df['height'].str.rstrip('m').str.replace(',', '.'),
        errors='coerce'
    )

    # Convert 'marketValue' to numeric (Euros)
    df['marketValue'] = pd.to_numeric(
        df['marketValue']
        .str.lstrip('€')
        .str.replace('k', 'e3')
        .str.replace('m', 'e6')
        .str.replace('.', ''),
        errors='coerce'
    )

    # Convert 'age' to numeric
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    return df

def aggregate_all_data(df_list):
    """
    Aggregates a list of DataFrames into one DataFrame.

    Parameters:
    df_list (list): A list of DataFrames.

    Returns:
    DataFrame: The aggregated DataFrame.
    """
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()
