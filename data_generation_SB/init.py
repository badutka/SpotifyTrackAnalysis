import time
from io import BytesIO

import requests
import spotipy
import spotipy.util as util
import sys
import webbrowser
import converter
import os
from json.decoder import JSONDecodeError
import spotipy.oauth2
import data
import urllib.request
from PIL import Image
# import matplotlib.pyplot as plt
from os import walk
import csv


class Spotify:

    def __init__(self, user, id, secret):

        try:
            self.token = util.prompt_for_user_token(user,
                                                    scope='playlist-modify-private playlist-modify user-read-playback-state user-read-currently-playing, user-modify-playback-state app-remote-control streaming',
                                                    client_id=id,
                                                    client_secret=secret, redirect_uri='http://54.229.55.83/')

        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{user}")
            self.token = util.prompt_for_user_token(user,
                                                    scope='playlist-modify-private playlist-modify user-read-playback-state user-read-currently-playing, user-modify-playback-state app-remote-control streaming',
                                                    client_id=id,
                                                    client_secret=secret, redirect_uri='http://54.229.55.83/')

        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        # self.sp_client = spotipy.client.Spotify(token)
        # self.sp_obj = spotipy.oauth2.SpotifyClientCredentials(client_id=id, client_secret=secret)

    def download(self):
        pass

    def play(self, artist, num):
        results = self.sp.search(q='artist:' + artist, type='artist')
        for k, v in results.items():
            for w, x in v.items():
                if type(x) == list:
                    artist = x[0]
                    # for i in range(len(x)):
                    #    print(x[i])

        lz_uri = 'spotify:artist:' + artist['id']
        results = self.sp.artist_top_tracks(lz_uri)
        best_tracks = []
        d = {}
        for track in results['tracks'][:10]:
            '''print(
                'track    : ' + track['name'])
            print(
                'audio    : ' + track['preview_url'])
            print(
                'cover art: ' + track['album']['images'][0]['url'])'''

            best_tracks.append(track)

        # track = self.sp.track(best_tracks[num])
        print("Atrist: " + artist['name'])
        print("Track: " + best_tracks[num]['name'])

        print("Length: " + converter.miliseconds_to_minutes(best_tracks[num]['duration_ms']))

        print(best_tracks[num]['preview_url'])

        # for i in self.sp.user_playlists('kamilj185')['items']:
        # print(i)

        webbrowser.open(best_tracks[num]['preview_url'])

    def get_playlist(self, user):
        playlists = []
        # print(type(self.sp.current_user_playlists()))

        if self.sp.me()['display_name'] == user:
            for i in self.sp.current_user_playlists()['items']:
                playlists.append(i)
        else:
            for i in self.sp.user_playlists(user)['items']:
                playlists.append(i)

        return playlists

    def get_playlist_id(self, playlist):
        return playlist['uri']

    def get_playlists_metadata(self, playlists):
        for i in range(len(playlists)):
            print(str(i) + ' - ' + playlists[i]['name'] + ' tracks: ' + str(playlists[i]['tracks']['total']))

        playlist = input("Select playlist")
        if playlist == '':
            playlist_data = {'name': '', 'type': '', 'track_number': '', 'id': ''}
            return playlist_data
        else:
            playlist_data = {
                'name': playlists[int(playlist)]['name'],
                'type': 'playlist',
                'track_number': str(playlists[int(playlist)]['tracks']['total']),
                'id': playlists[int(playlist)]['uri']
            }

            # playlist_id = self.get_playlist_id(playlists[int(playlist)])

            return playlist_data

    def get_tracks_from_playlist(self, playlist):

        tracks = self.sp.user_playlist_tracks(playlist['owner']['display_name'], playlist_id=playlist['uri'])
        track_list = []
        for i in tracks['items']:
            track_list.append(i)

        return track_list

    def get_tracks_metadata(self, tracks):
        d = {}
        id = 0

        for i in tracks:
            d[id] = {}

            for k, v in i['track'].items():
                if k == 'artists':
                    d[id]['artists'] = []
                    for j in v:
                        for w, x in j.items():
                            if w == "name":
                                d[id]['artists'].append(x)
                if k == 'name':
                    d[id]['name'] = v

            id += 1

        for k, v in d.items():
            print("Artists: ", end="")
            for i in v['artists']:
                print(i, end=' ')

            print(' ')
            print('Title: ' + v['name'])
            print(' ')

    def devices(self):

        # print(self.token)
        '''r = requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Accept": "application/json",
                                                                                  "Content-Type": "application/json",
                                                                                  "Authorization": "Bearer " + self.token})'''
        # devices = r.json()
        devices = self.sp.devices()
        print(devices)
        for i in devices['devices']:

            for k, v in i.items():
                print(k, v)

            print(' ')

        return devices['devices']

        # mp3file = urllib2.urlopen("https://p.scdn.co/mp3-preview/7998fb593b8ca2792422111117247a1230e980a6?cid=e49509108d364d2fa32a92000160d7e8")
        # with open('./test.mp3', 'wb') as output:
        # output.write(mp3file.read())
        # webbrowser.open('https://p.scdn.co/mp3-preview/7998fb593b8ca2792422111117247a1230e980a6?cid=e49509108d364d2fa32a92000160d7e8')
        # results1 = spotify.user_playlist_tracks("Paszan666", "Skillet", limit=100, offset=0)

    def get_device_id(self, device):
        return device['id']

    def get_device_metadata(self):
        for i in range(len(self.sp.devices()['devices'])):
            print(str(i) + '- ' + self.sp.devices()['devices'][i]['name'] + ' type: ' + self.sp.devices()['devices'][i]['type'])

        device = input("Select device")
        if device == '':
            d = {'name': '', 'type': '', 'id': ''}
            return d
        else:
            d = {
                "name": self.sp.devices()['devices'][int(device)]['name'],
                "type": self.sp.devices()['devices'][int(device)]['type'],
                "id": self.sp.devices()['devices'][int(device)]['id']
            }

            return d

    def play_from_device(self, device, medium, option):
        '''r = requests.get("https://api.spotify.com/v1/me/player/play",
                         params={'q': device, 'type': 'device_id'},
                         data = {'context_uri': playlist},
                         headers={"Accept": "application/json",
                                "Content-Type": "application/json",
                                "Authorization": "Bearer " + self.token})'''

        # print('Play ' + device['id'] + ' ' +  medium['id'])
        if option == 0:
            self.sp.start_playback(device['id'])
            return 0

        if medium['type'] == 'playlist':
            self.sp.start_playback(device['id'], context_uri=medium['id'])

        if medium['type'] == 'top_tracks':
            self.sp.start_playback(device['id'], uris=medium['id'])

    def get_artist_top_tracks(self, name):
        results = self.sp.search(q='artist:' + name, type='artist')
        for k, v in results.items():
            for i in range(len(v['items'])):
                print(str(i) + '- ' + v['items'][i]['name'], end=' ||')
                # print(v['items'][i]['images'][0]['url'])
                if len(v['items'][i]['images']) > 0:
                    print("Picture URL: ", end=' ')
                    print(v['items'][i]['images'][0]['url'])
                    # response = requests.get(v['items'][i]['images'][0]['url'])
                    # img = Image.open(BytesIO(response.content))
                    # Image.open(urllib.request.urlopen(v['items'][i]['images'][0]['url']))
                    # print(v['items'][i])
                print(' ')

        a = input("Select Artist")
        if a == '':
            top_tracks = {'name': '', 'type': '', 'track_number': '', 'id': ''}
            return top_tracks
        else:
            artist = v['items'][int(a)]

            top_tracks = self.sp.artist_top_tracks(artist['uri'])
            top_tracks_list = []
            for i in top_tracks['tracks']:
                top_tracks_list.append(i['uri'])

            d = {
                'name': artist['name'],
                'type': 'top_tracks',
                'track_number': len(top_tracks_list),
                'id': top_tracks_list
            }

            return d

    def play_next(self, device):
        self.sp.next_track(device['id'])

    def play_previous(self, device):
        self.sp.previous_track(device['id'])

    def stop_from_device(self, device):
        self.sp.pause_playback(device['id'])

    '''def change_volume(self, device, volume):
        self.sp.volume(volume, device['id'])'''

    def get_track_info(self, tracks):
        # print(self.sp.tracks(tracks))

        for i in self.sp.tracks(tracks)['tracks']:
            print(i)

    def current_playback(self):
        if self.sp.current_playback() == None:
            print("None")
            return None
        data = self.sp.current_playback()
        # for k,v in data['item'].items():
        #    print(k, v)
        print("Device: " + data['device']['name'])
        print("Artists: ", end=' ')
        for i in data['item']['artists']:
            print(i['name'], end=' ')
        print(' ')
        print("Track: " + data['item']['name'])
        return self.sp.current_playback()


def switch(spotify):
    exitFlag = 0

    device = {'name': '', 'type': '', 'id': ''}
    medium = {'name': '', 'type': '', 'track_number': '', 'id': ''}
    # play = "No"
    while exitFlag == 0:
        time.sleep(0.5)
        print("1 - Get User Playlists")
        print("2 - Get Artist Top Tracks")
        print("3 - Get Device")
        print("4 - Play")
        print("5 - Next Track")
        print("6 - Previous Track")
        print("7 - Stop")
        print("8 - Current Playback")
        print("0000 - Get Track Info")
        print("0 - Exit")
        print(' ')
        print("Device: " + device['name'] + ' ' + device['type'])
        print("Medium: " + medium['name'] + ' ' + medium['type'])
        # print("Play " + play)
        print(' ')
        c = input("Select Option ")
        try:
            c = int(c)
        except:
            print("Wrong Option")

        if c == 1:
            u = input("Type Username ")
            if u == '':
                pass
            else:
                playlists = spotify.get_playlist(u)
                medium = spotify.get_playlists_metadata(playlists)
            print(' ')
        if c == 2:
            a = input("Type Artist ")
            medium = spotify.get_artist_top_tracks(a)
            print(' ')

        if c == 3:
            device = spotify.get_device_metadata()
            print(' ')

        if c == 4:
            if device['id'] == '':
                print("No device")
            else:
                if medium['name'] == '':
                    spotify.play_from_device(device, medium, 0)
                else:
                    print("0 - Start")
                    print('1 - Start medium (' + medium['name'] + ' ' + medium['type'] + ')')

                    p = input("Select play type")
                    spotify.play_from_device(device, medium, int(p))
                    play = "Yes"

        if c == 5:
            '''if play == "No":
                print("Turn device On")
            else:'''
            spotify.play_next(device)
            print(' ')

        if c == 6:
            '''if play == "No":
                print("Turn device On")
            else:'''
            spotify.play_previous(device)
            print(' ')
        if c == 7:
            spotify.stop_from_device(device)
            play = "No"
            print(' ')

        if c == 8:
            spotify.current_playback()
        if c == 0000:
            spotify.get_track_info(medium['id'])
        if c == 0:
            exitFlag = 1

        print('========================================')


def main(arg):
    spotify = Spotify('Paszan666', 'e49509108d364d2fa32a92000160d7e8', 'fbe5330b72fb44048ae44ca735f021e4')
    # switch(spotify)

    f = []
    for (dirpath, dirnames, filenames) in walk("types"):
        f.extend(filenames)
        break

    with open('data/dataset.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(
            ['Genre', 'Length', 'Popularity', 'Danceabilty', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 'Instrumentalness',
             'Liveness', 'Valence', 'Tempo'])
    csv_file.close()

    for i in f:
        with open("types/" + i, 'r') as file:
            type = i.split('.')[0]
            '''for j in range(7):
                data.get_artist(spotify, file.readline(), type)'''
            for j in file:
                data.get_artist(spotify, file.readline(), type)

        with open('data/dataset.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # csv_writer.writerow(['Genre', 'Length', 'Popularity'])
            for k, v in data.d.items():
                csv_writer.writerow([v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11]])
        data.d = {}
    # print(data.d)
    # playlists = spotify.get_playlist("kamilj185")

    # tracks = spotify.get_tracks_from_playlist(playlists[0])
    # spotify.get_tracks_metadata(tracks)
    # devices = spotify.devices()
    # spotify.play_from_device(devices[0])

    '''playlists = spotify.get_playlist("Paszan666")
    print(playlists)
    p_id = spotify.get_playlist_id(playlists[0])
    d_id = spotify.get_device_id(spotify.devices()[0])
    #print(spotify.devices())
    spotify.play_from_device(d_id, p_id)'''


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main(1)
    else:
        main(int(sys.argv[1]) - 1)
