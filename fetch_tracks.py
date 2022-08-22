
from config.playlist import spotify_playlists
from utils.data_utils import gather_data,save_tracks_data
from tools.s3_helper import s3
from tools.spotify_helper import SpotipyHelper
from objects.Artist import Artist
from objects.Track import Track
from countryinfo import CountryInfo
import pycountry
import pandas as pd
import boto3
import sys
from config import variables
from tools.s3_helper import s3
from tools.spotify_helper import SpotipyHelper




spotipy_ = SpotipyHelper()
s3_ = s3()
#bucket_name = 'spotify-analysis-etl-august'
# s3_.create_bucket(bucket_name=bucket_name)
uri = 'spotify:track:1EzrEOXmMH3G43AXT1y7pA'
spotipy_.get_audio_features(uri)



# playlist = 'reco-playlist'
# save_rec_data(playlist,False,bucket_name)
# key = '2022/8/20'
# s3_.read_data(bucket_name,key,playlist)
# cat = spotipy_.get_categories()
# cat_id = cat['categories']['items'][0]['id']
# playlist = spotipy_.get_category_playlists(cat_id)
# print(playlist)
# bucket_name = 'spotify-genre-data-by-country'
# s3_.create_bucket(bucket_name=bucket_name)

# genra = spotipy_.get_rec_genre()
# genre = input('\nWhat genra:')
# while genre != 'done':
#       atrists_track = spotipy_.get_tracks_by_genre(genre) 
#       save_tracks_data(atrists_track,genre,aws = True,bucket = bucket_name)
#       genre = input('\nWhat genra:')
# curent_genre = list(set(s3_.read_bucket_files(bucket_name)))
# curent_genre = [genre.split('.')[0] for genre in curent_genre]
# print(curent_genre)

# s3_.delete_buckets_s3()

# s3_.create_bucket(bucket_name=bucket_name)
# genra = ['arabic','english','armenia','polish','turkish','persian','japanese','chinese','italian','spanish']
# for genre in genra:
#     print(genre)
#     if genre not in curent_genre:
#         print(f'#######################-{genre}-###############')
#         atrists_track = spotipy_.get_tracks_by_genre(genre) 
#         save_tracks_data(atrists_track,genre,aws = True,bucket = bucket_name)
# con_info = CountryInfo().all()
# print('nak')

def fetch_track_by_country():
    bucket_name = 'spotify-genre-data-by-country'
    s3_.create_bucket(bucket_name=bucket_name)

    countries = list(pycountry.countries)
    countries = [country.name for country in countries]

    curent_genre = list(set(s3_.read_bucket_file_names(bucket_name)))
    curent_genre = [genre.split('.')[0] for genre in curent_genre]

    for country in countries:
        if country not in curent_genre:
            print(f'#######################-{country}-###############')
            artists_tracks = spotipy_.get_tracks_by_keyword(country) 
            save_tracks_data(artists_tracks,country,aws = True,bucket = bucket_name)


def fetch_track_by_spotify_genra():
    bucket_name = 'spotify-genre-data'
    s3_.create_bucket(bucket_name=bucket_name)

    genra = spotipy_.get_rec_genre()
    genre = input('\nWhat genra:')
    # while genre != 'done':
    #       atrists_track = spotipy_.get_tracks_by_genre(genre) 
    #       save_tracks_data(atrists_track,genre,aws = True,bucket = bucket_name)
    #       genre = input('\nWhat genra:')
    curent_genre = list(set(s3_.read_bucket_file_names(bucket_name)))
    curent_genre = [genre.split('.')[0] for genre in curent_genre]
    print(curent_genre)
    for genre in genra:
        print(genre)
        if genre not in curent_genre:
            print(f'#######################-{genre}-###############')
            atrists_track = spotipy_.get_tracks_by_genre(genre) 
            save_tracks_data(atrists_track,genre,aws = True,bucket = bucket_name)

def add_features_to_track(bucket,bucket_features):
    curent_files = list(set(s3_.read_bucket_file_names(bucket_features)))
    curent_files = [genre.split('-')[0] for genre in curent_files]        
   

    file_names = s3_.read_bucket_file_names(bucket)
    for file_name in file_names:
        obj = s3_.client.get_object(Bucket= bucket, Key= f'{file_name}.csv') 
        df = pd.read_csv(obj['Body']) 
        df.columns = [c.lower() for c in df.columns]
        df.drop_duplicates(subset=['uri'],inplace=True)
        uris = list(df.uri.values)
        if len(uris) > 0:
            features = []
            for i in range(0,len(uris),50):
                sebset = uris[i:i+50]
                features.append(spotipy_.get_audio_features(sebset))
            features_df = pd.DataFrame()
            for i in range(0,len(features)):
                temp = pd.DataFrame(features[i])
                features_df = features_df.append(temp,ignore_index=True)

            full_df = df.merge(features_df, how='left',on='uri')


            with open(f'/tmp/temp.csv','w') as file:
                full_df.to_csv(file)
            s3_.save_data_s3('temp',bucket_features,f'{file_name}-features.csv')
            print(f'\n{file_name} has been saved!' )



# s3_.delete_buckets_s3()
bucket = variables.BUCKET_GENRA
bucket_features = variables.BUCKET_FULL_FEATURES_GENRA
s3_.create_bucket(bucket_name=bucket_features) 
add_features_to_track(bucket,bucket_features)
 







                           










   


    

