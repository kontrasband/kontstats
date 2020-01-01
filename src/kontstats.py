from utils.instagram import Instragram
from utils.sheets import GoogleSheet
from configparser import ConfigParser
from utils.argparser import KontArgumentParser
from pathlib import Path


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

    # Create Clients
    InstaClient = Instragram(insta_u, insta_p)
    GoogleClient = GoogleSheet(google_key_file)

    insta_num_followers = InstaClient.get_num_followers()

    GoogleClient.add_row([insta_num_followers])


if __name__ == '__main__':
    main()
