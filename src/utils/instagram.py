from configparser import ConfigParser
from InstagramAPI import InstagramAPI
import pandas as pd


class Instragram(object):

    def __init__(self, username, password):

        self.api = InstagramAPI(username=username, password=password)
        self.api.login()

        assert self.api.isLoggedIn, 'not logged in'

    def is_logged_in(self):
        return self.api.isLoggedIn

    def update_followers(self):
        self.followers = self.api.getTotalSelfFollowers()

    def get_num_followers(self):
        self.update_followers()
        self.nr_followers = len(self.followers)
        return self.nr_followers

    def get_followers_ids(self):
        self.update_followers()
        followers_df = pd.DataFrame(self.followers)
        return list(followers_df.username.values)
