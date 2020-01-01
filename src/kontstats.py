from utils.instagram import Instragram
from utils.sheets import GoogleSheet
from configparser import ConfigParser


def main():

    config = ConfigParser()
    config.read('../config.ini')

    insta_user = config['INSTAGRAM']['KONT_USERNAME']
    insta_pass = config['INSTAGRAM']['KONT_PASSWORD']

    InstaClient = Instragram(insta_user, insta_pass)
    GoogleClient = GoogleSheet()

    insta_num_followers = InstaClient.get_num_followers()

    GoogleClient.add_row([insta_num_followers])


if __name__ == '__main__':
    main()
