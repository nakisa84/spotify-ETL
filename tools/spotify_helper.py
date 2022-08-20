
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from objects.Track import Track
from config import variables


class Helper():
    def __init__(self):
        self.token = SpotifyOAuth(scope=variables.SCOPE,username=variables.USERNAME,client_id=variables.CLIENT_ID,client_secret=variables.CLIENT_SECRET,redirect_uri=variables.REDIRECT_URL)
        self.client = spotipy.Spotify(auth_manager=self.token)


class SpotipyHelper(Helper):
    def __init__(self):
        super().__init__()
   
    def track_to_viz(self):
        num_tracks_to_visualise = int(input("How many tracks would you like to visualise? "))
        last_played_tracks = self.client.current_user_recently_played(num_tracks_to_visualise)

        tracks = [Track(track["track"]["name"],track["track"]["artists"][0]["name"],track["track"]["id"]) for
            track in last_played_tracks["items"]]

        print(f"\nHere are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
        for index, track in enumerate(tracks):
            print(f"{index+1}- {track.name}")
        return tracks


    def rec_tracks(self,tracks):
        indexes = input("\nEnter a list of up to 5 tracks you'd like to use as seeds. Use indexes separated by a space: ")
        indexes = indexes.split()
        seed_tracks = [tracks[int(index)-1].track_id for index in indexes]  
        #track_features = spotify_client.audio_features(seed_tracks)
        rec_tracks = self.client.recommendations(seed_tracks=seed_tracks)
        return rec_tracks  


    def rec_tracks_name(self,rec_tracks):
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        rec_track_names = []

        for index, track in enumerate(rec_tracks['tracks']):
            rec_track_names.append(track['name'])
            print(f"{index+1}- {track['name']}")

        return  rec_track_names

    def recommended_tracks_info(self,rec_tracks):
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        rec_tracks_info= []

        for index, track in enumerate(rec_tracks['tracks']):
            rec_tracks_info.append((track['name'],track['artists'][0]['name']))
            print(f"{index+1}- {(track['name'],track['artists'][0]['name'])}")

        return  rec_tracks_info        

    def get_tracks_uris(self,recommended_track_names):
        rec_uris = []
        for track in recommended_track_names:
            query = track
            uri = self.client.search(limit=1,q=query)['tracks']['items'][0]['id']
            rec_uris.append(uri)
        return rec_uris


    def create_playlist(self):
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = self.client.user_playlist_create(variables.USERNAME,playlist_name)
        print(f"\nPlaylist '{playlist['name']}' was created successfully.") 
        return playlist



    def populate_tracks_in_playlist(self,playlistid,rec_uris):
        response = self.client.user_playlist_add_tracks(variables.USERNAME,playlist_id=playlistid,tracks=rec_uris)
        if response['snapshot_id']:
            print(f"\nTracks populated successfully.") 
        return response

    def create_rec_playlist_spo(self):
        
        tracks = self.track_to_viz()
        rec_tracks = self.recommended_tracks(tracks)
        rec_track_names = self.recommended_tracks_name(rec_tracks)

        playlist = self.create_playlist()
        rec_uris = self.get_tracks_uris(rec_track_names)
        try:
            response = self.populate_tracks_in_playlist(playlist['id'],rec_uris)
            if response['snapshot_id']:
                print("Tracks have been populated successfully!")
        except: 
                print("There was an error!")
        return response

    def get_tracks_uris_full(self,rec_tracks_info):
        rec_uris = []
        for track in rec_tracks_info:
            query = track[0]
            uri = self.client.search(limit=1,q=query)['tracks']['items'][0]['id']
            rec_uris.append((track[0],track[1],uri))
        return rec_uris

    def create_rec_playlist(self,numbers = 10):
        if not numbers:
             numbers = int(input("How many tracks would you like to visualise? "))

        last_played_tracks = self.client.current_user_recently_played(numbers)
        tracks = [Track(track["track"]["name"],track["track"]["artists"][0]["name"],track["track"]["id"]) for
            track in last_played_tracks["items"]]

        print(f"\nHere are the last {numbers} tracks you listened to on Spotify:")
        for index, track in enumerate(tracks):
            print(f"{index+1}- {track.name}")

        seed_tracks = [tracks[i].track_id for i in range(3)]  
        #track_features = spotify_client.audio_features(seed_tracks)
        rec_track = self.client.recommendations(seed_tracks=seed_tracks)
        rec_tracks_info = self.recommended_tracks_info(rec_track)
        rec_track_full = self.get_tracks_uris_full(rec_tracks_info)
        return rec_track_full
        
          
        
             
       


    

          

    