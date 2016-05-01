from User import *
from Player import *
# from ServiceManager import *
from os import path

import Settings

class Hermes:
    def __init__(self, username):
        self.setup_paths(username)
        self.user = User(self, username)
        # self.client = ClientHandler(self.user)
        self.player = Player()

    # def __del__(self):
    #     print "**Hermes dtor"

    def setup_paths(self, username):
        Settings.add_path_dir("data", "hermes-userdata")
        Settings.add_path_dir("user", username, "data")

        Settings.pathman["profile"] = path.join(Settings.pathman["user"], username)
        Settings.pathman["library"] = path.join(Settings.pathman["user"], username+"_db")

    def add_account(self, username, password, extras = None):
        self.user.add_account(username, password, extras)

    def intersect(self, res, inp):
        if len(res) == 0:
            for row in inp:
                res.add(row)
        else:
            temp = set()
            for row in inp:
                temp.add(row)
            res = res.intersection(temp)
        return res

    def search(self, tail):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(tail)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'artist', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'album', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'title',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        return [Art_res, Alb_res2, Tra_res]

    def search_album(self, album):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(album)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'album', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'album', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'album',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        return [Art_res, Alb_res2, Tra_res]

    def search_artist(self, album):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(album)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'artist', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'artist', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'artist',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        # return [Art_res, Alb_res2, Tra_res]

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
