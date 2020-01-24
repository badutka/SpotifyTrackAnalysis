import sys
import spotipy
import spotipy.util as util
from src.api.Credentials import Credentials


class Auth(object):
    def __init__(self):
        self.username = "td3q7kjc03ctqgipbkb72zn62"
        self.scope = "user-library-read"

    def authorize(self, creds: Credentials) -> str:
        token = util.prompt_for_user_token(username=self.username,
                                           scope=self.scope,
                                           client_id=creds.SPOTIPY_CLIENT_ID,
                                           client_secret=creds.SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=creds.SPOTIPY_REDIRECT_URI)
        return token

    def connect(self, token: str) -> spotipy.client.Spotify:
        if token:
            sp = spotipy.Spotify(auth=token)
            return sp
        else:
            print("Can't get token for", self.username)
            Exception("Make sure credentials are passed correctly to \"authorize\" method")
