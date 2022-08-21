class Track:
    def __init__(self,name,artist,id,uri = None):
        self.name = name
        self.artist = artist
        self.id = id
        self.uri = uri
    def create_spotify_uri(self):
        return  f"spotify:track:{self.id}"


    def __str__(self):
        return f"{self.name} by {self.artist}"  