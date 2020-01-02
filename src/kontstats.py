import imageio
import logging

from utils.bot import Bot
from configparser import ConfigParser
from utils.argparser import KontArgumentParser
from pathlib import Path

from utils.constants import LOGGING_FORMAT

logging.basicConfig(filename='konstats.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT)

imageio.plugins.ffmpeg.download()


def main():
    """
    Run python konstats.py -h for help
    """
    logging.info('Start')

    # Parse Arguments
    logging.debug('Parsing Arguments')
    parser = KontArgumentParser()
    args = parser.get_args()

    # Read config
    logging.debug('Reading Config')
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
    logging.debug('Creating Bot client')
    client = Bot(insta_u, insta_p,
                 google_key_file,
                 spotify_client_id,
                 spotify_client_secret,
                 google_api_key)

    # Instagram Tasks
    logging.info('Instagram tasks')
    # client.challenge_instagram_auth()
    # client.update_insta_follower_count()
    # client.update_insta_followers_info()

    # Spotify Tasks
    logging.info('Spotify tasks')
    client.update_spotify_track_plays()

    # Youtube Tasks
    logging.info('Youtube tasks')
    client.update_youtube_stats()

    logging.info('Done')


if __name__ == '__main__':
    main()
