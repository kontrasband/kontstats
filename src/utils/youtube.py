from requests import get
from json import loads
import pandas as pd
from .constants import MIDDELKLAS_YT_ID, KOPSTAMP_YT_ID


class Youtube(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stats(self):
        """
        Method that gets all the stats for our youtube videos
        """

        videos = {'KOPSTAMP': KOPSTAMP_YT_ID,
                  'MIDDELKLAS_MIDDELMAN': MIDDELKLAS_YT_ID}

        df = pd.DataFrame()
        for name, video_id in videos.items():
            resp = get(
                f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={self.api_key}')

            video_df = pd.DataFrame(loads(resp.text)['items'][0]['statistics'],
                                    index=[1])
            video_df['name'] = name
            df = pd.concat([df, video_df])

        return df
