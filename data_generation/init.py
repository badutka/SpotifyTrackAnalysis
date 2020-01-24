import spotipy
import spotipy.util as util
import sys
import os
from json.decoder import JSONDecodeError
import spotipy.oauth2
import src.data_generation.data as data
from os import walk
import csv


class Spotify:

    def __init__(self, user, id, secret):

        try:
            self.token = util.prompt_for_user_token(user,
                                                    scope='playlist-modify-private playlist-modify user-read-playback-state user-read-currently-playing, user-modify-playback-state app-remote-control streaming',
                                                    client_id=id,
                                                    client_secret=secret,
                                                    redirect_uri='http://localhost:8888/callback/')
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{user}")
            self.token = util.prompt_for_user_token(user,
                                                    scope='playlist-modify-private playlist-modify user-read-playback-state user-read-currently-playing, user-modify-playback-state app-remote-control streaming',
                                                    client_id=id,
                                                    client_secret=secret,
                                                    redirect_uri='http://localhost:8888/callback/')
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)

    def download(self):
        pass


def main(arg):
    spotify = Spotify('td3q7kjc03ctqgipbkb72zn62',
                      '54fdfa2962664b91872c52a157a994d5',
                      'af2147fd29824614ae63375940ab5653')

    f = []
    for (dirpath, dirnames, filenames) in walk("../../data/artists"):
        f.extend(filenames)
        break

    for i in f:
        with open("../../data/artists/" + i, 'r') as file:
            type = i.split('.')[0]
            '''for j in range(7):
                data.get_artist(spotify, file.readline(), type)'''
            for j in file:
                data.get_artist(spotify, file.readline(), type)

        with open('data/' + type + '.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Length', 'Popularity'])
            for k, v in data.d.items():
                csv_writer.writerow([v[0], v[1]])
        data.d = {}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main(1)
    else:
        main(int(sys.argv[1]) - 1)
