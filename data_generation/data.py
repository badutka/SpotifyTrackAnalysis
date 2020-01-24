import src.data_generation.converter as converter

d = {}


def get_artist(spotify, name, music_type):
    results = spotify.sp.search(q='artist:' + name, type='artist')
    artists = []

    for k, v in results['artists'].items():
        if k == 'items':
            for i in v:
                if music_type in i['genres']:
                    artists.append(i['uri'])

    for i in artists:
        get_albums(spotify, i)


def get_albums(spotify, uri):
    results = spotify.sp.artist_albums(uri, limit=50)
    albums = {}

    for i in results['items']:
        if any(x not in i['name'] for x in ['(']) and i['name'] not in d.keys():
            albums[i['name']] = i['uri']

    for k, v in albums.items():
        get_tracks(spotify, v)
        break


def get_tracks(spotify, uri):
    results = spotify.sp.album_tracks(uri)

    for i in results['items']:
        track = spotify.sp.track(i['uri'])
        d[track['uri']] = []
        for k, v in track.items():
            if k == 'duration_ms':
                time = converter.miliseconds_to_seconds(v)
                d[track['uri']].append(time)
            if k == 'popularity':
                d[track['uri']].append(v)
