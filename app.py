from utils.playlist_utils import gather_data
from tools.s3_helper import s3
from tools.spotify_helper import SpotipyHelper




if __name__ == '__main__' : 
    spotipy_ = SpotipyHelper()
    s3_ = s3()
    bucket_name = 'spotify-analysis-etl-august'
    if not s3_.is_bucket_exists(bucket_name):
        s3_.create_bucket(bucket_name=bucket_name)
    else:
        print(f"{bucket_name}-already exists.")


    # PLAYLIST1 = 'rap_caviar'
    # PLAYLIST2 = 'relax_and_chill'
    # PLAYLIST3 = 'best_of_2000_pop'
    # PLAYLIST4 = 'iranian_rap'
    # playlists =  [PLAYLIST1,PLAYLIST2,PLAYLIST3,PLAYLIST4]
    # for item in playlists:
    #     gather_data(item,bucket_name)


    spotipy_.create_recommended_playlist()

