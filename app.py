import imp
from operator import imod
from urllib import response
from config.playlist import spotify_playlists
from utils.playlist_utils import gather_data,save_tracks_data
from tools.s3_helper import s3
from tools.spotify_helper import SpotipyHelper
from objects.Artist import Artist
from objects.Track import Track


if __name__ == '__main__' : 
    spotipy_ = SpotipyHelper()
    s3_ = s3()
    # bucket_name = 'spotify-analysis-etl-august'
    # s3_.create_bucket(bucket_name=bucket_name)


    # bucket_name = 'spotify-recom'
    # s3_.create_bucket(bucket_name=bucket_name)
    # playlist = 'reco-playlist'
    # save_rec_data(playlist,False,bucket_name)
    # key = '2022/8/20'
    # s3_.read_data(bucket_name,key,playlist)
    # cat = spotipy_.get_categories()
    # cat_id = cat['categories']['items'][0]['id']
    # playlist = spotipy_.get_category_playlists(cat_id)
    # print(playlist)
    bucket_name = 'spotify-genre-data'
    s3_.create_bucket(bucket_name=bucket_name)
    
    geras = spotipy_.get_rec_genre()
    genre = ''
    while genre != 'done':
          genre = input('What genra:')
          atrists_track = spotipy_.get_tracks_by_genre(genre)
          
          playlist = f'{genre}-genre'
          save_tracks_data(atrists_track,playlist,aws = True,bucket = bucket_name)

                           










   


    

