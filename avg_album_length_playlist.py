import csv
import boto3
from datetime import datetime

from config.playlist import spotify_playlists
from tools.playlists import get_track_info
from tools.helpers import Helper
from  config.playlist import spotify_playlists


helper = Helper()
spotipy_object = helper.authorize_and_create_client()
s3 = helper.create_aws_boto3_client()



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
    with open('/tmp/rapcaviar_album.csv','w') as file:
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

        
        s3 = boto3.resource('s3')
        date = datetime.now()
        filename = f'{date.year}/{date.month}/{date.day}/rapcaviar_albums.csv'
        object = s3.Object('spotify-analysis-data-nakisa', filename)
        object.put(Body=file)


# def test():
#     some_binary_data = b'Here we have some data'
#     more_binary_data = b'Here we have some more data'

#     # Method 1: Object.put()
#     s3 = boto3.resource('s3')
#     object = s3.Object('spotify-analysis-data-nakisa', 'my/key/including/filename.txt')
#     object.put(Body=some_binary_data)

#     # # Method 2: Client.put_object()
#     # client = boto3.client('s3')
#     # client.put_object(Body=more_binary_data, Bucket='spotify-analysis-data-nakisa', Key='my/key/including/anotherfilename.txt')



def lambda_handler(event, context):
    gather_data()


