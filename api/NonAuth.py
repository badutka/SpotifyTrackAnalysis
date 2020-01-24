import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.api.Credentials import Credentials


class NonAuth(object):
    def __init__(self):
        pass

    @staticmethod
    def connect(creds: Credentials) -> spotipy.client.Spotify:
        client_credentials_manager = SpotifyClientCredentials(client_id=creds.SPOTIPY_CLIENT_ID,
                                                              client_secret=creds.SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
