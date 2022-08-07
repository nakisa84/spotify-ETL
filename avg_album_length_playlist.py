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
s3_clients = s3_resource.meta.client
# bucket = helper.create_bucket('naki-',s3_clients)

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



def gather_data(playlist):

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

    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/{playlist}.csv'
    s3_resource.Object('spotify-analysis-data-nakisa', filename).upload_file(f'/tmp/{playlist}.csv')
    

def read_data(key,filename,bucket):
    s3_clients.download_file(Bucket=bucket, Key=f'{key}/{filename}', 
                            Filename="data/downloaded_from_s3.csv")

   
    


