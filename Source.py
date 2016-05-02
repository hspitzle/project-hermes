from Library import *
import Settings

import pickle
import os
from os import path
import eyed3
from enum import Enum

from gmusicapi import Mobileclient
import soundcloud
import urllib3.contrib.pyopenssl
import requests

requests.packages.urllib3.disable_warnings()
urllib3.contrib.pyopenssl.inject_into_urllib3()


class SourceType(Enum):
    LOCAL = 0
    GOOGLE = 1
    SOUNDCLOUD = 2
    SPOTIFY = 3

class Source(object):
    def __init__(self, library, s_type):
        self.library = library
        self._source = s_type

    def get_source(self):
        return self._source

    def get_stream_URL(self, song_id):
        pass

    def sync(self):
        pass

class GoogleMusic(Source):
    def __init__(self, library, username, password):
        Source.__init__(self, library, SourceType.GOOGLE)
        self.GOOGLE_DEVICE_ID = None

        print username
        print password

        self.client = Mobileclient()
        logged_in = self.client.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
        print "Google logged in:", logged_in

        DList = self.client.get_registered_devices()
        self.GOOGLE_DEVICE_ID = DList[0]["id"]
        if self.GOOGLE_DEVICE_ID[:2] == '0x':
            self.GOOGLE_DEVICE_ID = self.GOOGLE_DEVICE_ID[2:]

        print self.GOOGLE_DEVICE_ID

        #>testing
        # self.get_stream_URL("47b9d52c-9d66-3ff2-94d4-3ae55c0d2acc")

    def get_stream_URL(self, song_id):
        return self.client.get_stream_url(song_id, self.GOOGLE_DEVICE_ID)

    def sync(self):
        gmusic_tracks = self.client.get_all_songs()
        for track in gmusic_tracks:
            art = ''
            try:
                art = track['albumArtRef'][0]['url']
            except KeyError:
                art = ''
            self.library.insert_track(track['title'], track['album'], track['artist'], self._source, str(track['id']), track['trackNumber'], art)

class Soundcloud(Source):
    def __init__(self, library, username, password, client_id, client_secret):
        Source.__init__(self, library, SourceType.SOUNDCLOUD)

        #TODO: set up sc client and authenticate
        # self.client = soundcloud.Client(client_id=user.SOUNDCLOUD_CLIENT_ID, client_secret=user.SOUNDCLOUD_CLIENT_SECRET_ID, username=user.S_username, password=user.S_password)

        self.SOUNDCLOUD_CLIENT_ID = "" #>& init
        self.client = None #>& init

    def get_stream_URL(self, song_id):
        if self.client is None:
            return
        return self.client.get('/tracks/' + str(song_id)).stream_url + "?client_id=" + self.SOUNDCLOUD_CLIENT_ID

    def sync(self):
        Fav_Size = 0
        S_list = self.client.get('/me/favorites', limit=300)
        while Fav_Size != len(S_list):
            Fav_Size = len(S_list)
            S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

        for track in S_list:
            self.library.insert_track(track.title, "Unknown Album", track.user['username'], self._source, str(track.id), 0, track.artwork_url)

class Spotify(Source):
    def __init__(self, library, username, password):
        Source.__inti__(self, library, SourceType.SPOTIFY)

        #TODO: set up google client and authenticate

    def sync(self):
        pass #> implement

class LocalMusic(Source):
    def __init__(self, library):
        Source.__init__(self, library, SourceType.LOCAL)
        self.watched = []
        self.watched_file = Settings.pathman["profile"] + "_watched"
        Settings.add_path_file("watched", self.watched_file)

        print "Watched file:", self.watched_file

        if os.stat(self.watched_file).st_size > 0:
            filer = open(self.watched_file, 'r')
            self.watched = pickle.load(filer)
            filer.close()

    def get_stream_URL(self, song_id):
        return song_id

    def get_watched(self):
        return self.watched

    def add_watched(self, directory):
        # already there
        if directory in self.watched:
            return False

        self.watched.append(directory)
        self.save_watched()
        return True

    def remove_watched(self, directory):
        self.watched.remove(directory)
        self.save_watched()

    def save_watched(self):
        filer = open(self.watched_file, 'w')
        pickle.dump(self.watched, filer)
        filer.close()

    def sync(self):
        local_tracks = []
        for path in self.watched:
            filelist = []
            for (dirpath, dirnames, filenames) in os.walk(path):
                filelist.extend(dirpath + '/' + filename for filename in filenames)
            local_tracks += filelist

        for File in local_tracks:
            if not (File.endswith('.mp3') or File.endswith('.wav')):
                local_tracks.remove(File)

        for track in local_tracks:
            afile = eyed3.load(track)
            tag = afile.tag

            if len(tag.artist) and len(tag.album) and len(tag.title) > 0:
                self.library.insert_track(tag.title, tag.album, tag.artist, self._source, str(track), tag.track_num[0], '')
            else:
                print "Could not resolve track metadata for: " + track
