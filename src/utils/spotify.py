import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials as SCC
from requests import get
from json import loads


def get_albums_count(album_ids):
    """
    Function that uses a server hosted on https://t4ils.dev:4433/api/beta/albumPlayCount 
    for https://github.com/evilarceus/Spotify-PlayCount that returns the playcount of an album

    Parameters
    album_ids(list): list of album ids, ['5NJafKlvdUSssGlVG3nGuo', '2w1W2OrF3PW4eAuqdN0nVk']
    """
    df = pd.DataFrame()
    for album_id in album_ids:
        resp = get(
            f'https://t4ils.dev:4433/api/beta/albumPlayCount?albumid={album_id}')
        data = loads(resp.text)['data']
        df = pd.concat([df, pd.DataFrame(data)])
    return df


class SpotifyArtist(object):
    def __init__(self, client_id, client_secret, artist_uri='spotify:artist:13mo5g6PR09u3Rq8bEstY2'):

        creds = SCC(client_id, client_secret)
        self.client = spotipy.Spotify(client_credentials_manager=creds)
        self.artist_uri = artist_uri
        self.artist = self.client.artist(self.artist_uri)
        self.albums = self.client.artist_albums(self.artist_uri)

    def get_track_counts(self):
        albums = self.albums
        albums_ids = [album['id'] for album in albums['items']]
        df = get_albums_count(albums_ids)
        return df
