import csv
from urllib import response
import boto3
from datetime import datetime
from io import StringIO

from config.playlist import spotify_playlists
from tools.playlists import get_track_info
from tools.helpers import Helper,SpotipyHelper
from  config.playlist import spotify_playlists
import pandas as pd


helper = Helper()
spotipy_object = helper.authorize_and_create_client()
s3_resource = helper.create_aws_resource()
s3_client = s3_resource.meta.client
#bucket_name,bucket_response = helper.create_bucket('naki-agust-',s3_client,bucket_name=)

def create_recommended_playlist():
    spotify_helper = SpotipyHelper()
    helper = Helper()
    spotify_client = helper.authorize_and_create_client()


    tracks = spotify_helper.track_to_viz(spotify_client)
    recommended_tracks = spotify_helper.recommended_tracks(spotify_client,tracks)
    recommended_track_names = spotify_helper.recommended_tracks_name(recommended_tracks)

    playlist = spotify_helper.create_playlist(spotify_client)
    recommended_uris = spotify_helper.get_tracks_uris(spotify_client,recommended_track_names)
    response = spotify_helper.populate_tracks_in_playlist(spotify_client,playlist['id'],recommended_uris)



def gather_data_local(playlist):

    final_data_dictionary = {
        'Year':[],
        'Album Length(ms)':[],
        'Album Name':[],
        'Artist':[],
        'Songs Number':[]
    }
    with open(f'data/{playlist}_album.csv','w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        albums_obtained = []
        tracks_info = get_track_info(spotipy_object,spotify_playlists()[playlist])
        for track in tracks_info:
            key = tracks_info[track]['album_name']+"-"+tracks_info[track]['artist']
            print(key)
            if key not in albums_obtained:
                albums_obtained.append(key)
                album_data = spotipy_object.album(tracks_info[track]['album_uri'])
                album_length_ms = 0
                counter = 0
                for song in album_data['tracks']['items']:
                    counter += 1
                    album_length_ms = song['duration_ms'] + album_length_ms
                writer.writerow({'Year': album_data['release_date'][:4],
                                        'Album Length(ms)': album_length_ms,
                                        'Album Name': album_data['name'],
                                        'Artist': album_data['artists'][0]['name'],
                                        'Songs Number': counter})
                final_data_dictionary['Year'].append(album_data['release_date'][:4])
                final_data_dictionary['Album Length(ms)'].append(album_length_ms)
                final_data_dictionary['Album Name'].append(album_data['name'])
                final_data_dictionary['Artist'].append(album_data['artists'][0]['name']) 
                final_data_dictionary['Songs Number'].append(counter)

    return final_data_dictionary

def gather_data(playlist,bucket):

    final_data_dictionary = {
        'Year':[],
        'Album Length(ms)':[],
        'Album Name':[],
        'Artist':[],
        'Songs Number':[]
    }
    with open(f'/tmp/{playlist}.csv','w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        albums_obtained = []
        tracks_info = get_track_info(spotipy_object,spotify_playlists()[playlist])
        for track in tracks_info:
            key = tracks_info[track]['album_name']+"-"+tracks_info[track]['artist']
            print(key)
            if key not in albums_obtained:
                albums_obtained.append(key)
                album_data = spotipy_object.album(tracks_info[track]['album_uri'])
                album_length_ms = 0
                counter = 0
                for song in album_data['tracks']['items']:
                    counter += 1
                    album_length_ms = song['duration_ms'] + album_length_ms
                writer.writerow({'Year': album_data['release_date'][:4],
                                        'Album Length(ms)': album_length_ms,
                                        'Album Name': album_data['name'],
                                        'Artist': album_data['artists'][0]['name'],
                                        'Songs Number': counter})
                final_data_dictionary['Year'].append(album_data['release_date'][:4])
                final_data_dictionary['Album Length(ms)'].append(album_length_ms)
                final_data_dictionary['Album Name'].append(album_data['name'])
                final_data_dictionary['Artist'].append(album_data['artists'][0]['name']) 
                final_data_dictionary['Songs Number'].append(counter)                        
    
    save_data(playlist,bucket)
  
    
def save_data(playlist,bucket):
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/{playlist}.csv'
    s3_client.upload_file(Filename = f'/tmp/{playlist}.csv',
                           Bucket = bucket,
                           Key = filename)

def read_data(bucket,key,filename):
    keys = key.split('/')
    s3_client.download_file(Bucket = bucket,
                             Key = f'{key}/{filename}', 
                             Filename = f"data/{keys[0]}_{keys[1]}_{keys[2]}_{filename}")

def delete_buckets():
    response = s3_client.list_buckets()
    print("Listing Amazon S3 Buckets:")
    for bucket in response['Buckets']:
        print(f"-- {bucket['Name']}")

    for item in response['Buckets']:
        answer = input('\ndelete? ')
        if answer.lower() == 'y':
            bucket = s3_resource.Bucket(item['Name'])
            bucket.objects.all().delete()
            s3_client.delete_bucket(Bucket=item['Name'])
            print(f"Amazon S3 {item['Name']} has been deleted")                              

#gather_data('best_of_2000_pop')
#read_data('naki-agust-9652c097-a290-4dd8-9100-01ece4e8e4c3''2022/8/15','best_of_2000_pop.csv',)
    
# s3 = boto3.resource('s3')
# bucket_list = [bucket.name for bucket in s3.buckets.all()]
# print(len(bucket_list))
# print(bucket_list)
# bucket_name,bucket_response = helper.create_bucket('Agust-',s3_client,bucket_name='spotify-analytics-2')  
# bucket_name,bucket_response = helper.create_bucket('Agust-',s3_client,bucket_name='spotify-analytics')  
# gather_data('best_of_2000_pop',bucket_name)
delete_buckets()
