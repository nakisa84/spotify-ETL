import csv
from config.playlist import spotify_playlists
from tools.spotify_helper import SpotipyHelper
from config.playlist import spotify_playlists
from tools.s3_helper import s3


spotify_object = SpotipyHelper()
s3_ = s3()

def get_track_info(spotipy_object,uris):
    tracks = {}
    playlist_tracks = spotipy_object.playlist_tracks(playlist_id=uris)

    counter = 0
    for song in playlist_tracks['items']:
        if song['track']:
            if song['track']['album'] and song['track']['album']['name']:
                counter +=1
                tracks[f'track-{counter}']               = {}
                tracks[f'track-{counter}']['name']       = song['track']['name']
                tracks[f'track-{counter}']['uri']        = song['track']['artists'][0]['uri']
                tracks[f'track-{counter}']['artist']     = song['track']['artists'][0]['name']
                tracks[f'track-{counter}']['album_name'] = song['track']['album']['name']
                tracks[f'track-{counter}']['album_uri']  = song['track']['album']['uri']
    return tracks


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
        tracks_info = get_track_info(spotify_object.client,spotify_playlists()[playlist])
        for track in tracks_info:
            key = tracks_info[track]['album_name']+"-"+tracks_info[track]['artist']
            print(key)
            if key not in albums_obtained:
                albums_obtained.append(key)
                album_data = spotify_object.client.album(tracks_info[track]['album_uri'])
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
        tracks_info = get_track_info(spotify_object.client,spotify_playlists()[playlist])
        for track in tracks_info:
            key = tracks_info[track]['album_name']+"-"+tracks_info[track]['artist']
            print(key)
            if key not in albums_obtained:
                albums_obtained.append(key)
                album_data = spotify_object.client.album(tracks_info[track]['album_uri'])
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
    
    s3_.save_data_s3(playlist,bucket)




def save_rec_tracks_data(playlist,aws = False,bucket = None):
    rec_track_full = spotify_object.create_rec_playlist()
    trach_counter = 0
    rec_dic = {
            'Track Number':[],
            'Track':[],
            'Artist':[],
            'URI':[]
            }
 
    if aws:
        path = '/tmp/'  
    else:
        path = 'data/'       
    with open(f"{path}{playlist}.csv",'w') as file:
        header = list(rec_dic.keys())
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        for track in rec_track_full:
            trach_counter += 1
            writer.writerow({
                            'Track Number': trach_counter,
                            'Track' : track[0],
                            'Artist': track[1],
                            'URI': track[2]
                            })
    if aws == True:
        s3_.save_data_s3(playlist,bucket) 


def save_tracks_data(tracks,playlist,aws = False,bucket = None):
        trach_counter = 0
        rec_dic = {
                'Track Number':[],
                'Track':[],
                'Artist':[],
                'URI':[]
                }
    
        if aws:
            path = '/tmp/'  
        else:
            path = 'data/'       
        with open(f"{path}{playlist}.csv",'w') as file:
            header = list(rec_dic.keys())
            writer = csv.DictWriter(file,fieldnames=header)
            writer.writeheader()
            for track in tracks:
                trach_counter += 1
                writer.writerow({
                                'Track Number': trach_counter,
                                'Track' : track.name,
                                'Artist': track.artist,
                                'URI': track.uri
                                })
        if aws == True:
            s3_.save_data_s3(playlist,bucket)     

                       




  
    
                             
