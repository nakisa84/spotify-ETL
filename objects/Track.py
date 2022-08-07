class Track:
    def __init__(self,track_name,artist_name,track_id):
        self.name = track_name
        self.artist_name = artist_name
        self.track_id = track_id
    def create_spotify_uri(self):
        return  f"spotify:track:{self.id}"


    def __str__(self):
        return f"{self.name} by {self.artist}"  