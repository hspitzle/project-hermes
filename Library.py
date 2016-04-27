from Shelver import *
from Source import *

import Settings

class Library:
    def __init__(self, cursor, user):
        self.cursor = cursor
        self.sources = []
        self.user = user
        self.add_source(LocalMusic(user))

    def add_source(self, source):
        self.sources.append(source)
        #> sync new source? or all sources?

    def get(self, distinct, get_others, where_like, ordered_return, USI, single=False, db='tracks'):
        print "searching..."
        query = 'SELECT DISTINCT(' + distinct + ')'
        for item in get_others:
            query += ', ' + item
        query += ' FROM ' + db + ' WHERE ' + where_like + ' LIKE ? OR ' + where_like + ' LIKE ?'
        if len(ordered_return) > 0:
            query += ' ORDER BY '
            for item in ordered_return:
                query += item + ', '
            query = query[:len(query) - 2]
        self.cursor.execute(query, (USI + '%', '% ' + USI + '%',))
        if single is False:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def sync(self):
        self.user.cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location TEXT, streamid TEXT UNIQUE, tracknum INTEGER, art TExT)''')
        self.user.cursor.execute('''SELECT count(*) FROM tracks''')
        Settings.next_id = self.user.cursor.fetchone()[0]

        for src in self.sources:
            src.sync()
        self.user.db.commit()

    def get_local_music(self):
        return next((src for src in self.sources if isinstance(src, LocalMusic)), None)

    def get_watched(self):
        local_music = self.get_local_music()
        if local_music is None:
            return
        return local_music.get_watched()

    def add_watched(self, directory):
        local_music = self.get_local_music()
        if local_music is None:
            local_music = LocalMusic(self)
            self.sources.append(local_music)
        return local_music.add_watched(directory)

    def remove_watched(self, directory):
        local_music = self.get_local_music()
        if local_music is None:
            return
        local_music.remove_watched(directory)

class Playlist(Shelver):
    def __init__(self, title, user):
        super(Playlist, self).__init__(title, user)
        self.load()

    def add(self, sid, streamid, location):
        self.items.append(PlaylistItem(sid, streamid, location))
        self.save()

    def clear(self):
        self.items = []
        self.save()

    def printItems(self):
        for item in self.items:
            item.printItem()


class PlaylistItem:

    def __init__(self, sid, streamid, location):
        self.id = sid
        self.streamid = streamid
        self.location = location

    def printItem(self):
        print self.id, self.streamid, self.location
