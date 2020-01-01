from utils.bot import Bot
from configparser import ConfigParser
from utils.argparser import KontArgumentParser
from pathlib import Path

import imageio
imageio.plugins.ffmpeg.download()


def main():
    """
    Run python konstats.py -h for help
    """

    # Parse Arguments
    parser = KontArgumentParser()
    args = parser.get_args()

    # Read config
    config_file = Path(args.config)
    assert config_file.exists(), f'{config_file} doesn\'t exist.'
    config = ConfigParser()
    config.read(config_file)

    insta_u, insta_p = config['INSTAGRAM']['KONT_USERNAME'], config['INSTAGRAM']['KONT_PASSWORD']
    google_key_file = config['GOOGLE']['KEY_FILE']
    google_api_key = config['GOOGLE']['API_KEY']
    spotify_client_id = config['SPOTIFY']['CLIENT_ID']
    spotify_client_secret = config['SPOTIFY']['CLIENT_SECRET']

    # Create Client
    Client = Bot(insta_u, insta_p,
                 google_key_file,
                 spotify_client_id,
                 spotify_client_secret,
                 google_api_key)

    # Instagram Tasks
    Client.update_insta_follower_count()
    Client.update_insta_followers_info()

    # Spotify Tasks
    Client.update_spotify_track_plays()

    # Youtube Tasks
    Client.update_youtube_stats()


if __name__ == '__main__':
    main()
