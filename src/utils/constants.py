MIDDELKLAS_YT_ID = 'BzGOPUwr4-Q'
KOPSTAMP_YT_ID = 's4LEe7K96-U'

SUPPORTED_RAW_LOG_PLATFORMS = ['SPOTIFY',
                               'INSTAGRAM',
                               'FACEBBOOK',
                               'YOUTUBE']

SUPPORTED_RAW_LOG_MESSAGES = ['FOLLOWER_COUNT',
                              'FOLLOWERS_LEFT',
                              'FOLLOWERS_JOINED',
                              'PLAYS_RAAK_N_BIETJIE_FUCKED',
                              'PLAYS_MY_DOLLA_NEE',
                              'PLAYS_SEEMAN',
                              'PLAYS_KOPSTAMP',
                              'PLAYS_MIDDELKLAS_MIDDELMAN',
                              'PLAYS_SKIET_REENBOE_OP_FASCISME']
YOUTUBE_MESSAGES = []
for vid in ['KOPSTAMP', 'MIDDELKLAS_MIDDELMAN']:
    for stat in ['VIEWCOUNT', 'LIKECOUNT', 'DISLIKECOUNT', 'FAVORITECOUNT', 'COMMENTCOUNT']:
        YOUTUBE_MESSAGES.append(stat+'_'+vid)

SUPPORTED_RAW_LOG_MESSAGES = SUPPORTED_RAW_LOG_MESSAGES + YOUTUBE_MESSAGES
