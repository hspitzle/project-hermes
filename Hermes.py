from User import *
from Player import *
# from ServiceManager import *
from os import path

import Settings

class Hermes:
    def __init__(self, username):
        self.setup_paths(username)
        self.user = User(self, username)
        self.player = Player()

    # def __del__(self):
    #     print "**Hermes dtor"

    def setup_paths(self, username):
        Settings.add_path_dir("data", "hermes-userdata")
        Settings.add_path_dir("user", username, "data")

        Settings.add_path_file("profile", username, "user")
        Settings.add_path_file("library", username+"_db", "user")

    def add_account(self, j_item):
        self.user.add_account(j_item)
        self.user.add_credentials(j_item)


    def search(self, tail):
        return self.user.library.search(tail)

    def search_album(self, album):
        return self.user.library.search_album(album)

    def search_artist(self, artist):
        return self.user.library.search_artist(artist)


    def get_stream_URL(self, location, song_id):
        return self.user.get_stream_URL(location, song_id)

    def get_watched(self):
        return self.user.get_watched()

    def add_watched(self, directory):
        return self.user.add_watched(directory)

    def remove_watched(self, directory):
        self.user.remove_watched(directory)

    def sync(self):
        print "Syncing"
        self.user.sync()
        print "Done"

    def syncStream(self):
        self.user.sync_stream()
        all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'], 'location', ['artist', 'album', 'tracknum'], 'S', False, 'stream')
        return all_rows

    def create_playlist(self, playlist_name):
        self.user.create_playlist(playlist_name)

    def quit(self):
        self.user.quit()
