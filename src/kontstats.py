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
    logging.warning('Start')

    logging.debug('Parsing Arguments')
    parser = KontArgumentParser()
    args = parser.get_args()

    youtube = args.youtube
    spotify = args.spotify
    instagram = args.instagram

    logging.debug('Reading Config')
    config_file = Path(args.config)
    assert config_file.exists(), f'{config_file} doesn\'t exist.'
    config = ConfigParser()
    config.read(config_file)

    insta_u, insta_p = config['INSTAGRAM']['USERNAME'], config['INSTAGRAM']['PASSWORD']
    google_key_file = config['GOOGLE']['KEY_FILE']
    google_api_key = config['GOOGLE']['API_KEY']
    spotify_client_id = config['SPOTIFY']['CLIENT_ID']
    spotify_client_secret = config['SPOTIFY']['CLIENT_SECRET']

    print('Initialising Bot')
    logging.debug('Creating Bot client')
    bot = Bot(insta_u, insta_p,
              google_key_file,
              spotify_client_id,
              spotify_client_secret,
              google_api_key)

    if instagram:
        print('Performing Instagram Tasks')
        logging.info('Initialising Instagram')
        bot.init_instagram()

        logging.info('Performing Instagram tasks')
        bot.update_insta_follower_count()
        bot.update_insta_followers_info()

    if spotify:
        print('Performing Spotify Tasks')
        logging.info('Initialising Spotify')
        bot.init_spotify()

        logging.info('Performing Spotify tasks')
        bot.update_spotify_track_plays()

    if youtube:
        print('Performing Youtube Tasks')
        logging.info('Initialising Youtube')
        bot.init_youtube()
        logging.info('Performing Youtube tasks')
        bot.update_youtube_stats()

    logging.warning('End')


if __name__ == '__main__':
    main()
