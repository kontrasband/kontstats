import pandas as pd


def clean_data(df):
    """
    Function that cleans the data from the sheet to a clean format
    """
    df.DATETIME = pd.to_datetime(df.DATETIME, format='%d/%m/%Y %H:%M:%S')
    # Add day for aggregations
    df['DATETIME_D'] = df.DATETIME.dt.round('D')

    return df


def get_daily_plays_per_platform(df):
    daily_plays = df[df.PLATFORM.isin(['SPOTIFY', 'YOUTUBE', 'APPLE'])]
    daily_plays.MESSAGE = daily_plays.MESSAGE.apply(
        lambda x: 'PLAYS' if x == 'VIEWCOUNT' else x)
    daily_plays = daily_plays[daily_plays.MESSAGE == 'PLAYS']
    daily_plays = daily_plays.groupby(['DATETIME_D', 'PLATFORM', 'SONG']).max().VALUE.\
        reset_index().drop_duplicates()
    daily_plays.VALUE = daily_plays.VALUE.astype(int)
    daily_plays = daily_plays.groupby(
        ['DATETIME_D', 'PLATFORM']).sum().VALUE.reset_index()
    return daily_plays


def get_daily_plays(df):
    daily_plays = get_daily_plays_per_platform(df)
    return daily_plays.groupby('DATETIME_D').sum().VALUE.reset_index()
