import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
import plotly.express as px
from utils.bot import Bot
from utils.app.wrangling import clean_data, get_daily_plays_per_platform, get_daily_plays
from utils.app.plotting import plot_spotify_plays_per_song, plot_youtube_3d, plot_instagram_followers, fig_to_card
from utils.app.plotting import plot_total_play_per_song, plot_daily_plays_per_platform, plot_daily_plays
from argparse import ArgumentParser, RawTextHelpFormatter
from dash.dependencies import Input, Output
from dash import Dash
from pathlib import Path
from configparser import ConfigParser

config_file = Path('../src/config.ini')
assert config_file.exists(), f'{config_file} doesn\'t exist.'
config = ConfigParser()
config.read(config_file)

insta_u, insta_p = config['INSTAGRAM']['KONT_USERNAME'], config['INSTAGRAM']['KONT_PASSWORD']
google_key_file = config['GOOGLE']['KEY_FILE']
google_api_key = config['GOOGLE']['API_KEY']
spotify_client_id = config['SPOTIFY']['CLIENT_ID']
spotify_client_secret = config['SPOTIFY']['CLIENT_SECRET']

bot_deats = [insta_u, insta_p,
             google_key_file,
             spotify_client_id,
             spotify_client_secret,
             google_api_key]


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.config.suppress_callback_exceptions = True

summary_card = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='graphTotalPlays')
    ]))

youtube_card = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='graphYoutube')
    ]))

spotify_card = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='graphSpotify')
    ]))

instagram_card = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='graphInstagram')
    ]))

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="/home")),
        dbc.NavItem(dbc.NavLink("Songs", href="/songs"))],
    fluid=True,
    brand="Kont Stats",
    brand_href="/",
    color="dark"
)


# body = dbc.Container([
#     dbc.Row([dbc.Button('Refresh', color="danger", id='btnRefresh')]),
#     dcc.Loading([dbc.Row([dbc.Col([summary_card], width=6),
#                           dbc.Col([instagram_card], width=6)]),
#                  dbc.Row([dbc.Col([spotify_card], width=6),
#                           dbc.Col([youtube_card], width=6)])
#                  ])
# ], fluid=True)


app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    dcc.Loading(html.Div(id='pageContent'))
])


def song_page():
    return html.H1('Song Page')


def home_page():
    # get data
    bot = Bot(*bot_deats)
    df = bot.GSpread.get_raw_logs_as_df()

    # wrangle
    df = clean_data(df)
    daily_plays_per_platform_df = get_daily_plays_per_platform(df)
    daily_plays_df = get_daily_plays(df)

    # plot
    daily_plays_per_platform_fig = plot_daily_plays_per_platform(
        daily_plays_per_platform_df)
    daily_plays_fig = plot_daily_plays(daily_plays_df)
    instagram_followers_fig = plot_instagram_followers(df)

    l = [dbc.Row([dbc.Col([fig_to_card(id='daily_plays_per_platform_fig', fig=daily_plays_per_platform_fig)], width=6),
                  dbc.Col([fig_to_card(id='daily_plays_fig', fig=daily_plays_fig)], width=6)]),
         dbc.Row([dbc.Col([fig_to_card(id='instagram_followers_fig', fig=instagram_followers_fig)], width=6),
                  dbc.Col([], width=6)])
         ]

    return [html.H1('Home Page')]+l


@app.callback(
    Output('pageContent', 'children'),
    [Input('url', 'pathname')]


)
def display_page(pathname):
    if pathname == '/songs':
        return song_page()
    elif pathname in ['/home', '/', None]:
        return home_page()
    else:
        return home_page()


@app.callback([Output('graphSpotify', 'figure'),
               Output('graphYoutube', 'figure'),
               Output('graphInstagram', 'figure'),
               Output('graphTotalPlays', 'figure')],
              [Input('btnRefresh', 'n_clicks')])
def refreshGraph(n_clicks):
    # if n_clicks is not None:
    bot = Bot(*bot_deats)
    df = bot.GSpread.get_raw_logs_as_df()

    df, spotify_df, youtube_df, instagram_df = clean_data(df)

    spotify_plays_per_song_fig = plot_spotify_plays_per_song(spotify_df)
    youtube_3d_fig = plot_youtube_3d(youtube_df)
    instagram_followers_fig = plot_instagram_followers(instagram_df)
    total_play_fig = plot_total_play_per_song(df)

    return (spotify_plays_per_song_fig,
            youtube_3d_fig,
            instagram_followers_fig,
            total_play_fig)


if __name__ == '__main__':
    description = """
    Konstats App
    """

    parser = ArgumentParser(
        prog='Konstats', description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--ip',
                        type=str,
                        help='Which IP to start server on.',
                        default='127.0.0.1')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='which port to start on. If nothing is specified then defaults to 8050',
                        default=8050)
    parser.add_argument(
        '-d', '--debug', action='store_true', help='Debug app')
    args = parser.parse_args()
    host = args.ip
    port = args.port
    debug = args.debug

    app.run_server(debug=debug, port=port, host=host)
