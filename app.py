from urllib import response
from utils.playlist_utils import gather_data,rec_data
from tools.s3_helper import s3
from tools.spotify_helper import SpotipyHelper


if __name__ == '__main__' : 
    spotipy_ = SpotipyHelper()
    s3_ = s3()
    # bucket_name = 'spotify-analysis-etl-august'
    # s3_.create_bucket(bucket_name=bucket_name)


    bucket_name = 'spotify-recom'
    s3_.create_bucket(bucket_name=bucket_name)
    playlist = 'reco-playlist'
    rec_data(playlist,False,bucket_name)
    # key = '2022/8/20'
    # s3_.read_data(bucket_name,key,playlist)
      
    

