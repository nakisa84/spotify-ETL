import spotipy
from spotipy.oauth2 import SpotifyOAuth
from objects.Track import Track
from config import variables





class SpotipyHelper():

    def __init__(self):
        self.client = self.authorize_and_create_client()

    def authorize_and_create_client(self):
        token = SpotifyOAuth(scope=variables.SCOPE,username=variables.USERNAME,client_id=variables.CLIENT_ID,client_secret=variables.CLIENT_SECRET,redirect_uri=variables.REDIRECT_URL)
        spotify_client = spotipy.Spotify(auth_manager=token)
        return spotify_client 



    def track_to_viz(self):
        num_tracks_to_visualise = int(input("How many tracks would you like to visualise? "))
        last_played_tracks = self.client.current_user_recently_played(num_tracks_to_visualise)

        tracks = [Track(track["track"]["name"],track["track"]["artists"][0]["name"],track["track"]["id"]) for
            track in last_played_tracks["items"]]

        print(f"\nHere are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
        for index, track in enumerate(tracks):
            print(f"{index+1}- {track.name}")
        return tracks


    def recommended_tracks(self,tracks):
        indexes = input("\nEnter a list of up to 5 tracks you'd like to use as seeds. Use indexes separated by a space: ")
        indexes = indexes.split()
        seed_tracks = [tracks[int(index)-1].track_id for index in indexes]  
        #track_features = spotify_client.audio_features(seed_tracks)
        recommended_tracks = self.client.recommendations(seed_tracks=seed_tracks)
        return recommended_tracks  


    def recommended_tracks_name(self,recommended_tracks):
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        recommended_track_names = []
        for index, track in enumerate(recommended_tracks['tracks']):
            recommended_track_names.append(track['name'])
            print(f"{index+1}- {track['name']}")
        return    recommended_track_names  

    def get_tracks_uris(self,recommended_track_names):
        recommended_uris = []
        for track in recommended_track_names:
            query = track
            uri = self.client.search(limit=1,q=query)['tracks']['items'][0]['id']
            recommended_uris.append(uri)
        return recommended_uris


    def create_playlist(self):
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = self.client.user_playlist_create(variables.USERNAME,playlist_name)
        print(f"\nPlaylist '{playlist['name']}' was created successfully.") 
        return playlist



    def populate_tracks_in_playlist(self,playlistid,recommended_uris):
        response = self.client.user_playlist_add_tracks(variables.USERNAME,playlist_id=playlistid,tracks=recommended_uris)
        if response['snapshot_id']:
            print(f"\nTracks populated successfully.") 
        return response

    def create_recommended_playlist(self):
        
        tracks = self.track_to_viz()
        recommended_tracks = self.recommended_tracks(tracks)
        recommended_track_names = self.recommended_tracks_name(recommended_tracks)

        playlist = self.create_playlist()
        recommended_uris = self.get_tracks_uris(recommended_track_names)
        response = self.populate_tracks_in_playlist(playlist['id'],recommended_uris)
        return response

          

    