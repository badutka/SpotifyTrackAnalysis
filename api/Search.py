import spotipy
import string


def search(sp: spotipy.client.Spotify) -> None:
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])


def search2(sp: spotipy.client.Spotify) -> None:
    playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def search3(sp: spotipy.client.Spotify) -> None:
    pass

def get_playlist_tracks(username,playlist_id, sp):
    print("hello")
    results = sp.user_playlist_tracks(username)
    # tracks = results['items']
    # while results['next']:
    #     results = sp.next(results)
    #     tracks.extend(results['items'])
    # return tracks
