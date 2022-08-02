import csv
import spotipy
import boto3
from datetime import datetime

from config.playlist import spotify_playlists
from tools.playlists import get_track_info
from tools.helpers import Helper
from  config.playlist import spotify_playlists


helper = Helper()
spotipy_object = helper.authorize_and_create_client()


def gather_data_local(playlist):

    final_data_dictionary = {
        'Year':[],
        'Album Length(ms)':[],
        'Album Name':[],
        'Artist':[],
        'Songs Number':[]
    }
    with open(f'data/{playlist}_album.csv','w') as file:
        heather = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file,fieldnames=heather)
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




PLAYLIST1 = 'rap_caviar'
PLAYLIST2 = 'relax_and_chill'
PLAYLIST3 = 'best_of_2000_pop'
PLAYLIST4 = 'iranian_rap'
playlists =  [PLAYLIST1,PLAYLIST2,PLAYLIST3,PLAYLIST4]

for item in playlists:
    gather_data_local(item)