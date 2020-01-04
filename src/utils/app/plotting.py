import plotly.express as px


def plot_spotify_plays_per_song(spotify_df):
    fig = px.scatter(spotify_df,
                     x='DATETIME',
                     y='VALUE',
                     color='SONG',
                     title='Spotify song streams',
                     template='plotly_dark').update_traces(mode='lines+markers')

    return fig


def plot_youtube_3d(youtube_df):
    fig = px.scatter_3d(youtube_df.sort_values(by='DATETIME'),
                        x='DATETIME',
                        y='MESSAGE',
                        z='VALUE',
                        color='SONG',
                        log_z=True,
                        title=f'Youtube Stats',
                        template='plotly_dark')  # .update_traces(mode='lines+markers')

    return fig


def plot_instagram_followers(instagram_df):
    fig = px.scatter(instagram_df[instagram_df.MESSAGE == 'FOLLOWER_COUNT'],
                     x='DATETIME',
                     y='VALUE',
                     color_discrete_sequence=['#f3a55c'],
                     title='Instagram Followers',
                     template='plotly_dark').update_traces(mode='lines+markers')

    return fig


def plot_total_play_per_song(df):
    plays_per_day_df = df[df.PLATFORM.isin(['YOUTUBE', 'SPOTIFY']) &
                          (df.SONG != '') &
                          (df.MESSAGE.isin(['PLAYS', 'VIEWCOUNT']))].\
        drop('DATETIME', axis=1).drop_duplicates()

    plays_per_day_df.VALUE = plays_per_day_df.VALUE.astype(float)
    plays_per_day_df = plays_per_day_df.\
        groupby(['SONG', 'PLATFORM', 'DATETIME_D']).\
        max().reset_index().\
        groupby(['DATETIME_D', 'SONG']).\
        sum().reset_index()

    fig = px.scatter(plays_per_day_df,
                     x='DATETIME_D',
                     y='VALUE',
                     color='SONG',
                     title='Total Streams per song',
                     template='plotly_dark').update_traces(mode='lines+markers')
    return fig
