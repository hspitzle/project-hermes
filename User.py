from gmusicapi import Webclient
from Library import *
from ClientHandler import *

import Settings
import soundcloud

# import eyed3

import sys
# import os
# from os import path
import getpass

import pickle
import json


class User:
    def __init__(self, hermes, username):
        self.username = username
        self.G_username = ""
        self.G_password = ""
        self.S_username = ""
        self.S_password = ""
        self.GOOGLE_DEVICE_ID = ""
        self.SOUNDCLOUD_CLIENT_ID = ""
        self.SOUNDCLOUD_CLIENT_SECRET_ID = ""
        self.enc_key = "private_key"

        self.playlists = []

        # if len(sys.argv) >= 2:
        #     try:
        #         File = open(self.get_filename(str(sys.argv[1])))
        #     except IOError:
        #         print 'Cannot find user: ' + str(sys.argv[1])
        #         print 'Creating new user...'
        #         self.authenticate(self.get_filename())
        #     else:
        #         self.login(self.get_filename(str(sys.argv[1])))
        # else:
        #     self.authenticate(self.get_filename())

        self.userdata_path = Settings.pathman["user"]
        print "User data path:", Settings.pathman["user"]

        self.library = Library(self)

        self.load() #TODO: replace with load profile call, init all authenticated services



        # >*
        # self.watched_file = path.join(self.userdata_path, self.profile_name + "_watched")
        #
        # if not path.exists(self.watched_file):
        #     open(self.watched_file, 'w').close()
        #
        # if os.stat(self.watched_file).st_size > 0:
        #     filer = open(self.watched_file, 'r')
        #     self.watched = pickle.load(filer)
        #     filer.close()

        for filer in os.listdir(Settings.pathman["user"]): #> move to library
            if filer.startswith("playlist_"):
                #print "Adding playlist " , file
                playlist = Playlist(filer, self)
                self.playlists.append(playlist)

        self.client = ClientHandler(self) #>*


    def add_account(self, src_type, username, password, extras = None):
        src = Source(self.library, "@NA")
        if src_type is SourceType.LOCAL:
            src = LocalMusic(self.library)
        elif src_type is SourceType.GOOGLE:
            src = GoogleMusic(self.library, username, password)
        elif src_type is SourceType.SOUNDCLOUD:
            client_id = extras["client_id"]
            client_secret = extras["client_secret"]
            src = Soundcloud(self.library, username, password, client_id, client_secret)
        elif src is SourceType.SPOTIFY:
            src = Spotify(self.library, username, password)
        else:
            raise ValueError("Unrecognized src_type value")

        self.library.add_source(src)

    # def authenticate(self, USER_DATA_FILENAME):
    #     self.G_username = raw_input("Google Play Account Email: ")
    #     self.G_password = getpass.getpass("Google Play Account Pass: ")
    #
    #     Deviceclient = Webclient()
    #     Deviceclient.login(self.G_username, self.G_password)
    #
    #     DList = Deviceclient.get_registered_devices()
    #
    #     for device in DList:
    #         if device['type'] == "PHONE":
    #             self.GOOGLE_DEVICE_ID = device["id"]
    #             if self.GOOGLE_DEVICE_ID[:2] == '0x':
    #                 self.GOOGLE_DEVICE_ID = self.GOOGLE_DEVICE_ID[2:]
    #             break
    #
    #     self.S_username = raw_input("Soundcloud Account Username: ")
    #     self.S_password = getpass.getpass("Soundcloud Account Password: ")
    #     self.SOUNDCLOUD_CLIENT_ID = raw_input("Soundcloud Client ID: ")
    #     self.SOUNDCLOUD_CLIENT_SECRET_ID = raw_input("Soundcloud Secret Client ID: ")
    #
    #     File = open(USER_DATA_FILENAME, 'w+')
    #     File.write(self.encode(self.enc_key, self.G_username) + '\n')
    #     File.write(self.encode(self.enc_key, self.G_password) + '\n')
    #     File.write(self.encode(self.enc_key, self.S_username) + '\n')
    #     File.write(self.encode(self.enc_key, self.S_password) + '\n')
    #     File.write(self.GOOGLE_DEVICE_ID + '\n')
    #     File.write(self.SOUNDCLOUD_CLIENT_ID + '\n')
    #     File.write(self.SOUNDCLOUD_CLIENT_SECRET_ID + '\n')
    #     File.close()

    def load(self):
        USER_DATA_FILENAME = Settings.pathman["profile"]
        # File = open(USER_DATA_FILENAME, 'r')
        # self.G_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
        # self.G_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
        # self.S_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
        # self.S_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
        # self.GOOGLE_DEVICE_ID = File.readline().rstrip('\n')
        # self.SOUNDCLOUD_CLIENT_ID = File.readline().rstrip('\n')
        # self.SOUNDCLOUD_CLIENT_SECRET_ID = File.readline().rstrip('\n')
        # File.close()
        f = open('user.tmp', 'r')
        username = f.readline()[:-1]
        self.G_username = f.readline().rstrip('\n')
        self.G_password = f.readline().rstrip('\n')
        self.S_username = f.readline().rstrip('\n')
        self.S_password = f.readline().rstrip('\n')
        self.SOUNDCLOUD_CLIENT_ID = f.readline().rstrip('\n')
        self.SOUNDCLOUD_CLIENT_SECRET_ID = f.readline().rstrip('\n')
        f.close()

        cred = []

        account = {}
        account["type"] = SourceType.GOOGLE
        account["user"] = self.G_username
        account["pass"] = self.G_password

        cred.append(account)

        account = {}
        account["type"] = SourceType.SOUNDCLOUD
        account["user"] = self.S_username
        account["pass"] = self.S_password
        account["extras"] = {}
        account["extras"]["sc_client_id"] = self.SOUNDCLOUD_CLIENT_ID
        account["extras"]["sc_secret_id"] = self.SOUNDCLOUD_CLIENT_SECRET_ID

        cred.append(account)

        cred = str(cred).replace("'", "\"")
        enc_cred = Settings.encode(self.enc_key, cred)
        print cred
        print enc_cred
        print Settings.decode(self.enc_key, enc_cred)
        print Settings.pathman["profile"]

        j = json.loads(Settings.decode(self.enc_key, enc_cred))
        print j
        for item in j:
            print item
        # print j["g_user"]
        # print j["g_pass"]


        filer = open(Settings.pathman["profile"], 'w')
        pickle.dump(enc_cred, filer)
        filer.close()

        self.add_account(SourceType.GOOGLE, self.G_username, self.G_password)

        self.load_credentials()
        self.add_credentials(account)

        self.load_credentials()

    def load_credentials(self):
        print "Loading credentials..."
        filer = open(Settings.pathman["profile"], 'r')
        enc_cred = pickle.load(filer)
        filer.close()

        j = json.loads(Settings.decode(self.enc_key, enc_cred))
        print j
        for item in j:
            print item

        print json.dumps(j)

        return j

    def add_credentials(self, jitem):
        j = self.load_credentials()
        src_type = jitem["type"]
        print src_type

        for item in j:
            if item["type"] is src_type:
                print "credentials already stored"
                return

        j.append(jitem)

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
