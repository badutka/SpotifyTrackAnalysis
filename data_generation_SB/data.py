import converter

d = {}


def get_artist(spotify, name, music_type):
    results = spotify.sp.search(q='artist:' + name, type='artist')
    # print(results)
    artists = []
    for k, v in results['artists'].items():
        # print(k, v)
        if k == 'items':
            for i in v:
                # if music_type in i['genres']:
                # print(i['name'])
                artists.append(i['uri'])
                # print(i['uri'])

    for i in artists:
        get_albums(spotify, i, music_type)


def get_albums(spotify, uri, music_type):
    results = spotify.sp.artist_albums(uri, limit=50)
    albums = {}
    for i in results['items']:
        if any(x not in i['name'] for x in ['(']) and i['name'] not in d.keys():
            albums[i['name']] = i['uri']

        # print(i['name'], i['uri'])
        # albums.append(i['uri'])
        # print(i['uri'])
    # print(uri)
    # print(albums)
    for k, v in albums.items():
        get_tracks(spotify, v, music_type)
        break


def get_tracks(spotify, uri, music_type):
    # print(uri)
    results = spotify.sp.album_tracks(uri)
    # print(results)
    '''for i in results['items']:
        print(i['name'], i['uri'])'''
    # breakpoint()

    for i in results['items']:
        # print(i['name'])
        track = spotify.sp.track(i['uri'])
        # print(spotify.sp.audio_analysis(i['uri']))
        '''for k,v in spotify.sp.audio_analysis(i['uri']).items():
            print(k, v)'''

        '''for k,v in spotify.sp.audio_features(i['uri'])[0].items():
            print(k, v)
        break'''
        d[track['uri']] = []
        for k, v in track.items():
            # print(k, v)
            # d[v['uri']] = ''
            # print(k, v)
            '''if k=='name':
                d[track['uri']].append(v)'''
            if k == 'duration_ms':
                time = converter.miliseconds_to_seconds(v)
                d[track['uri']].append(music_type)
                if time < 750:
                    d[track['uri']].append(time)

            if k == 'popularity':
                if v > 30:
                    d[track['uri']].append(v)
                # print(v)

        for k, v in spotify.sp.audio_features(i['uri'])[0].items():
            if k == 'danceability':
                d[track['uri']].append(v)

            if k == 'energy':
                d[track['uri']].append(v)

            if k == 'loudness':
                d[track['uri']].append(v)

            if k == 'speechiness':
                d[track['uri']].append(v)

            if k == 'acousticness':
                d[track['uri']].append(v)

            if k == 'instrumentalness':
                d[track['uri']].append(v)

            if k == 'liveness':
                d[track['uri']].append(v)

            if k == 'valence':
                d[track['uri']].append(v)

            if k == 'tempo':
                d[track['uri']].append(v)
