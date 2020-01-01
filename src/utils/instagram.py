from configparser import ConfigParser
from InstagramAPI import InstagramAPI
import pandas as pd


class Instagram(object):

    def __init__(self, username, password):

        self.api = InstagramAPI(username=username, password=password)
        self.api.login()

        assert self.api.isLoggedIn, 'not logged in'

    def is_logged_in(self):
        return self.api.isLoggedIn

    def get_latest_followers(self):
        self.followers = self.api.getTotalSelfFollowers()

    def get_followers_df(self):
        self.get_latest_followers()
        return pd.DataFrame(self.followers)
