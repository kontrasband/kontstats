import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
import plotly.express as px
from utils.bot import Bot
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


body = dbc.Container([
    dbc.Row([dbc.Button('Refresh', color="danger", id='btnRefresh')]),
    dcc.Loading([dbc.Row(dbc.Col([dcc.Graph(id='graphSpotify')], width=12)),
                 dbc.Row(dbc.Col([dcc.Graph(id='graphYoutube')], width=12))
                 ])
])
app.layout = body


@app.callback([Output('graphSpotify', 'figure'),
               Output('graphYoutube', 'figure')],
              [Input('btnRefresh', 'n_clicks')])
def refreshGraph(n_clicks):
    if n_clicks is not None:
        bot = Bot(*bot_deats)
        df = bot.GSpread.get_raw_logs_as_df()
        df.DATETIME = df.DATETIME.astype('datetime64[ns]')
        spot_df = df[df.PLATFORM == 'SPOTIFY']
        yt_df = df[df.PLATFORM == 'YOUTUBE']

        spot_fig = px.scatter(spot_df,
                              x='DATETIME',
                              y='VALUE',
                              color='SONG',
                              title='Spotify song streams',
                              template='plotly_dark').update_traces(mode='lines+markers')

        yt_stat = 'LIKECOUNT'
        yt_fig = px.scatter(yt_df[yt_df.MESSAGE == yt_stat],
                            x='DATETIME',
                            y='VALUE',
                            color='SONG',
                            title=f'Youtube {yt_stat}',
                            template='plotly_dark').update_traces(mode='lines+markers')

    return (spot_fig, yt_fig)


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
