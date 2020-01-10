import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def fig_to_card(id, fig):

    return dbc.Card(
        dbc.CardBody([
            dcc.Graph(id=id, figure=fig)
        ]))


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


def plot_instagram_followers(df):
    instagram_df = df[(df.PLATFORM == 'INSTAGRAM') &
                      (df.MESSAGE == 'FOLLOWER_COUNT')]

    fig = px.scatter(instagram_df,
                     x='DATETIME',
                     y='VALUE',
                     color_discrete_sequence=['#be499d'],
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


def plot_daily_plays_per_platform(df):
    fig = px.scatter(df,
                     x='DATETIME_D',
                     y='VALUE',
                     color_discrete_map={'SPOTIFY': '#66d36d',
                                         'YOUTUBE': '#eb3323',
                                         'APPLE': '#dddddd'},
                     color='PLATFORM',
                     title='Total Streams per Platform',
                     template='plotly_dark').update_traces(mode='lines+markers')
    return fig


def plot_daily_plays(df):
    fig = px.scatter(df,
                     x='DATETIME_D',
                     y='VALUE',
                     title='Total Streams',
                     template='plotly_dark').update_traces(mode='lines+markers')
    return fig
