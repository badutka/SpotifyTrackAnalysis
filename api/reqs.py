import src.api.Credentials as crd
# import Credentials as crd  # still works, just highlights as "No module named..." ?
import src.api.Auth as Auth
import src.api.Search as Search
import src.api.NonAuth as NonAuth


def non_authorized():
    # Spotify App Credentials
    creds = crd.Credentials()

    # client object
    client = NonAuth.NonAuth()

    # spotipy connection object
    sp = client.connect(creds)

    # Search through tracks, playlists, etc.
    # Search.search3(sp)
    Search.get_playlist_tracks("td3q7kjc03ctqgipbkb72zn62", "6SF4Ni8e9Lv4TyxbZEGOgc", sp)


def authorized():
    # Spotify App Credentials
    creds = crd.Credentials()

    # client object
    client = Auth.Auth()

    # User authorization (token)
    token = client.authorize(creds)

    # spotipy connection object
    sp = client.connect(token)

    # Search through tracks, playlists, etc.
    Search.search3(sp)
