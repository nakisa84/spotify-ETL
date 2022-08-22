import os

AUTH_URL = 'https://accounts.spotify.com/api/token'
SCOPE = 'playlist-modify-public user-read-recently-played'
USERNAME = os.getenv('SPOTIFY_USER_NAME')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPTOFY_CLIENT_SECRET')
REDIRECT_URL = 'http://localhost:9000'
BUCKET_GENRA = 'spotify-genre-data'
BUCKET_COUNTRY = 'spotify-genre-data-by-country'
BUCKET_FULL_FEATURES_GENRA = 'spotify-full-features-genre'
BUCKET_FULL_FEATURES_COUNTRY = 'spotify-full-features-country'
