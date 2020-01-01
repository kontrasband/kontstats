from utils.bot import Bot
from configparser import ConfigParser
from utils.argparser import KontArgumentParser
from pathlib import Path

import imageio
imageio.plugins.ffmpeg.download()


def main():

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

    # Create Client
    Client = Bot(insta_u, insta_p, google_key_file)

    # Instagram Tasks
    Client.update_insta_follower_count()
    Client.update_insta_followers_info()


if __name__ == '__main__':
    main()
