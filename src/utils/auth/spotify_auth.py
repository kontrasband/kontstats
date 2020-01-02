import sys
import os
import spotipy
import spotipy.util as util
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

scopes = ['ugc-image-upload',
          'user-read-playback-state',
          'user-modify-playback-state',
          'user-read-currently-playing',
          'streaming',
          'app-remote-control',
          'user-read-email',
          'user-read-private',
          'playlist-read-collaborative',
          'playlist-modify-public',
          'playlist-read-private',
          'playlist-modify-private',
          'user-library-modify',
          'user-library-read',
          'user-top-read',
          'user-read-recently-played',
          'user-follow-read',
          'user-follow-modify']

scope = 'playlist-modify-private'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    default_username = input('No username specified, use default? [Y/n]: ')

    if default_username.lower() == 'y':
        username = 'm7klrf290iwgyn4tm0qxlzfn0'
    else:
        sys.exit()

token = util.prompt_for_user_token(
    username,
    scope,
    client_id=config['SPOTIFY']['CLIENT_ID'],
    client_secret=config['SPOTIFY']['CLIENT_SECRET'],
    redirect_uri='http://127.0.0.1')

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)
