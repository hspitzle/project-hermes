from gmusicapi import Webclient
from Library import *

import Settings
import soundcloud

import sys
import getpass

import pickle
import json


class User:
    def __init__(self, hermes, username):
        self.username = username
        self.enc_key = "private_key"

        self.playlists = []
        self.library = Library(self)

        self.load()

        for filer in os.listdir(Settings.pathman["user"]): #>? move to library?
            if filer.startswith("playlist_"):
                #print "Adding playlist " , file
                playlist = Playlist(filer, self)
                self.playlists.append(playlist)


    def add_account(self, j_item):
        src_type = j_item["type"]
        username = j_item["user"]
        password = j_item["pass"]

        src = Source(self.library, "@NA")
        if src_type is SourceType.GOOGLE:
            src = GoogleMusic(self.library, username, password)
        elif src_type is SourceType.SOUNDCLOUD:
            return #>*
            extras = j_item["extras"]
            client_id = extras["client_id"]
            secret_id = extras["secret_id"]
            print "sc client", client_id
            print "sc secret", secret_id
            src = Soundcloud(self.library, username, password, client_id, secret_id)
        elif src is SourceType.SPOTIFY:
            src = Spotify(self.library, username, password)
        else:
            raise ValueError("Unrecognized src_type value")

        self.library.add_source(src)

    def load(self):
        # f = open('user.tmp', 'r')
        # username = f.readline()[:-1]
        # self.G_username = f.readline().rstrip('\n')
        # self.G_password = f.readline().rstrip('\n')
        # self.S_username = f.readline().rstrip('\n')
        # self.S_password = f.readline().rstrip('\n')
        # self.SOUNDCLOUD_CLIENT_ID = f.readline().rstrip('\n')
        # self.SOUNDCLOUD_CLIENT_SECRET_ID = f.readline().rstrip('\n')
        # f.close()

        j_account_list = self.load_credentials()
        for acct in j_account_list:
            self.add_account(acct)

    def load_credentials(self):
        print "Loading credentials..."
        filer = open(Settings.pathman["profile"], 'r')
        try:
            enc_cred = pickle.load(filer)
        except EOFError:
            return []
        filer.close()

        j = json.loads(Settings.decode(self.enc_key, enc_cred))
        print j

        return j

    def add_credentials(self, j_item):
        j = self.load_credentials()
        src_type = j_item["type"]
        print "adding source type:", src_type

        for item in j:
            if item["type"] is src_type:
                print "credentials already stored"
                return

        j.append(j_item)

        filer = open(Settings.pathman["profile"], 'w')
        enc_cred = Settings.encode(self.enc_key, json.dumps(j))
        pickle.dump(enc_cred, filer)
        filer.close()

    def library_get(self, distinct, get_others, where_like, ordered_return, USI, single=False, db='tracks'):
        return self.library.get(distinct, get_others, where_like, ordered_return, USI, single, db)

    def sync(self):
        self.library.sync()

    def sync_stream(self):
        self.library.sync_stream()

    def get_stream_URL(self, location, song_id):
        return self.library.get_stream_URL(location, song_id)

    def create_playlist(self, playlist_name):
        title = 'playlist_' + playlist_name
        playlist = Playlist(title, self)
        self.playlists.append(playlist)

    def get_watched(self):
        return self.library.get_watched()

    def add_watched(self, directory):
        return self.library.add_watched(directory)

    def remove_watched(self, directory):
        self.library.remove_watched(directory)

    def quit(self):
        self.library.close()
        # if self.player.Queue != 'stream':
        #     self.player.Queue.save()
