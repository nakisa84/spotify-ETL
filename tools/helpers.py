import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import boto3
import uuid

class Track:
    def __init__(self,track_name,artist_name,track_id):
        self.name = track_name
        self.artist_name = artist_name
        self.track_id = track_id

        

AUTH_URL = 'https://accounts.spotify.com/api/token'
SCOPE = 'playlist-modify-public user-read-recently-played'
USERNAME = os.getenv('SPOTIFY_USER_NAME')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPTOFY_CLIENT_SECRET')
REDIRECT_URL = 'http://localhost:9000'



class Helper:
    def authorize_and_create_client(self):
        token = SpotifyOAuth(scope=SCOPE,username=USERNAME,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URL)
        spotify_client = spotipy.Spotify(auth_manager=token)
        return spotify_client 

   
    def create_bucket_name(self,bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
        return ''.join([bucket_prefix, str(uuid.uuid4())]) 


    def create_aws_resource(self):
        s3_resource = boto3.resource('s3')
        return s3_resource      

    def create_bucket(self,bucket_prefix, s3_connection):
        session = boto3.session.Session()
        current_region = session.region_name
        bucket_name = self.create_bucket_name(bucket_prefix)
        bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name)
        print(bucket_name, current_region)
        return bucket_name, bucket_response    

class SpotipyHelper:
    def track_to_viz(self,spotify_client):
        num_tracks_to_visualise = int(input("How many tracks would you like to visualise? "))
        last_played_tracks = spotify_client.current_user_recently_played(num_tracks_to_visualise)

        tracks = [Track(track["track"]["name"],track["track"]["artists"][0]["name"],track["track"]["id"]) for
            track in last_played_tracks["items"]]

        print(f"\nHere are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
        for index, track in enumerate(tracks):
            print(f"{index+1}- {track}")
        return tracks


    def recommended_tracks(self,spotify_client,tracks):
        indexes = input("\nEnter a list of up to 5 tracks you'd like to use as seeds. Use indexes separated by a space: ")
        indexes = indexes.split()
        seed_tracks = [tracks[int(index)-1].id for index in indexes]  
        #track_features = spotify_client.audio_features(seed_tracks)
        recommended_tracks = spotify_client.recommendations(seed_tracks=seed_tracks)
        return recommended_tracks  


    def recommended_tracks_name(self,recommended_tracks):
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        recommended_track_names = []
        for index, track in enumerate(recommended_tracks['tracks']):
            recommended_track_names.append(track['name'])
            print(f"{index+1}- {track['name']}")
        return    recommended_track_names  

    def get_tracks_uris(self,spotify_client,recommended_track_names):
        recommended_uris = []
        for track in recommended_track_names:
            query = track
            uri = spotify_client.search(limit=1,q=query)['tracks']['items'][0]['id']
            recommended_uris.append(uri)
        return recommended_uris


    def create_playlist(self,spotify_client):
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = spotify_client.user_playlist_create(USERNAME,playlist_name)
        print(f"\nPlaylist '{playlist['name']}' was created successfully.") 
        return playlist



    def populate_tracks_in_playlist(self,spotify_client,playlistid,recommended_uris):
        response = spotify_client.user_playlist_add_tracks(USERNAME,playlist_id=playlistid,tracks=recommended_uris)
        return response