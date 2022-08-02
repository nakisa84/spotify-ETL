
from sympy import limit


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


