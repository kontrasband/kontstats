from .instagram import Instagram
from .sheets import GoogleSheet
from .spotify import SpotifyArtist
from .youtube import Youtube
from .auth.insta_auth import LoginChallenge


class Bot(object):
    def __init__(self, insta_u, insta_p, google_key_file, spotify_client_id, spotify_client_secret, google_api_key):
        self.Insta = Instagram(insta_u, insta_p)
        self.InstaLC = LoginChallenge(insta_u, insta_p)
        self.Google = GoogleSheet(google_key_file)
        self.SpotifyArtist = SpotifyArtist(spotify_client_id,
                                           spotify_client_secret)
        self.Youtube = Youtube(google_api_key)

    def challenge_instagram_auth(self):
        self.InstaLC.init_challenge()

    def update_youtube_stats(self):
        df = self.Youtube.get_stats()
        stats = [c for c in df.columns if c != 'name']
        for row in df.iterrows():
            name = row[1]['name']
            for stat in stats:
                metric = str(row[1][stat])
                stat = stat.upper()
                self.Google.write_raw_log('YOUTUBE', name, stat, metric)

    def update_spotify_track_plays(self):
        """
        """
        df = self.SpotifyArtist.get_track_counts()
        for row in df.iterrows():
            name = row[1]['name'].upper().replace(
                ' ', '_').replace('Ë', 'E').replace("'", '')
            playcount = str(row[1]['playcount'])
            message = 'PLAYS'
            self.Google.write_raw_log('SPOTIFY', name, message, playcount)

    def update_insta_follower_count(self):
        """
        Method that writes a count of the current instagram followers into RAW_LOGS 

        Log that gets written:
        |31/12/2019 15:36:59 | FOLLOWER_COUNT | 655
        """

        df = self.Insta.get_followers_df()
        n_followers = df.shape[0]
        self.Google.write_raw_log('INSTAGRAM',
                                  '',
                                  'FOLLOWER_COUNT',
                                  n_followers)

    def update_insta_followers_info(self):
        """
        Method that writes the public available data of followers to Google Sheets

        Log that gets written:
        |31/12/2019 15:36:59 | FOLLOWERS_LEFT | lwdf, asdfa, asdfas
        |31/12/2019 15:36:59 | FOLLOWERS_JOINED | asdf, ad, ad


        Sheet that gets updated: INSTA_FOLLOWERS

        """

        cur_following = self.Google.sheet_to_df('kontstats',
                                                'INSTA_FOLLOWERS')
        new_following = self.Insta.get_followers_df()

        cur_followers = set(cur_following.username.values)
        new_followers = set(new_following.username.values)

        who_left = list(cur_followers.difference(new_followers))
        who_joined = list(new_followers.difference(cur_followers))

        if len(who_left) > 0:
            self.Google.write_raw_log('INSTAGRAM',
                                      '',
                                      'FOLLOWERS_LEFT',
                                      ', '.join(who_left))

        if len(who_joined) > 0:
            self.Google.write_raw_log('INSTAGRAM',
                                      '',
                                      'FOLLOWERS_JOINED',
                                      ', '.join(who_joined))

        if (len(who_left) > 0) or (len(who_joined) > 0):
            self.Google.df_to_sheet('kontstats',
                                    'INSTA_FOLLOWERS',
                                    new_following)
