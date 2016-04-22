from Library import *
import pickle
import os
from os import path

import eyed3

class Source(object):
    def __init__(self, name):
        self._name = name

    def get_source(self):
        return self._name

    def sync(self):
        pass

class GoogleMusic(Source):
    def __init__(self):
        Source.__init__(self, "google")

class LocalMusic(Source):
    def __init__(self, library, user):
        Source.__init__(self, "local")
        self.user = user
        self.library = library
        self.watched = []
        self.watched_file = path.join(user.userdata_path, user.profile_name + "_watched")

        if not path.exists(self.watched_file):
            open(self.watched_file, 'w').close()

        if os.stat(self.watched_file).st_size > 0:
            filer = open(self.watched_file, 'r')
            self.watched = pickle.load(filer)
            filer.close()

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
                self.user.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                (self.library.get_next_id(), tag.title, tag.album, tag.artist, 'L', 'L_' + str(track), tag.track_num[0], ''))
            else:
                print "Could not resolve track metadata for: " + track