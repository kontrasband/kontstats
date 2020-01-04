import pandas as pd


def clean_data(df):
    """
    Function that cleans the data from the sheet to a clean format
    """
    df.DATETIME = pd.to_datetime(df.DATETIME, format='%d/%m/%Y %H:%M:%S')
    # Add day for aggregations
    df['DATETIME_D'] = df.DATETIME.dt.round('D')

    spotify_df = df[(df.PLATFORM == 'SPOTIFY') & (df.SONG != '')]
    youtube_df = df[(df.PLATFORM == 'YOUTUBE') & (df.SONG != '')]
    instagram_df = df[df.PLATFORM == 'INSTAGRAM']

    return df, spotify_df, youtube_df, instagram_df
