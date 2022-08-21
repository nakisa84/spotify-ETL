class Artist:
    def __init__(self,id,genres,uri,name,popularity) -> None:
        self.genres = genres
        self.id = id
        self.uri = uri
        self.name = name
        self.popularity = popularity

    def __str__(self):
        return f"{self.name}" 

          
