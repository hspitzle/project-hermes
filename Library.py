from Shelver import *
from Source import *
import Settings

import sqlite3

class Library:
    def __init__(self, user):
        self.user = user
        self.sources = []

        self.db = sqlite3.connect(Settings.pathman["library"])
        self.cursor = self.db.cursor()

        self.add_source(LocalMusic(self))

    def __del__(self):
        print "***destructing library"

    def close(self):
        self.cursor.execute('''DROP TABLE IF EXISTS stream''')
        self.db.close()

    def add_source(self, source):
        self.sources.append(source)
        for src in self.sources:
            print type(src)
        #>? sync new source? or all sources?

    def get_source(self, src_type):
        return next((src for src in self.sources if (src.get_source() is src_type)), None)

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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location INTEGER, streamid TEXT UNIQUE, tracknum INTEGER, art TEXT)''')
        self.cursor.execute('''SELECT count(*) FROM tracks''')
        Settings.next_id = self.cursor.fetchone()[0]
        print "Library size (before syncing):", Settings.next_id

        for src in self.sources:
            src.sync()
        self.db.commit()

    def get_stream_URL(self, location, song_id):
        return self.get_source(location).get_stream_URL(song_id)

    def insert_track(self, title, album, artist, location, streamid, tracknum, art):
        self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                        (Settings.get_next_id(), title, album, artist, location, streamid, tracknum, art))

    def sync_stream(self):
        sc_music = self.get_source(SourceType.SOUNDCLOUD)
        if sc_music is None:
            return

        self.cursor.execute('''DROP TABLE IF EXISTS stream''')
        self.db.commit()

        tracks = self.client.S_client.get('/me/activities/tracks/affiliated', limit=200)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stream(id INTEGER PRIMARY KEY, title TEXT, album TEXT,artist TEXT, location TEXT, streamid TEXT, tracknum INTEGER, art TEXT)''')

        iden = 0
        duplifier = []
        for track in tracks.obj['collection']:
            if track['origin']['id'] in duplifier:
                continue
            if track['origin']['kind'] == 'playlist':

                Playtracks = self.client.S_client.get('/playlists/99297471/tracks')
                for play in Playtracks:
                    if play.id in duplifier:
                        continue
                    self.cursor.execute('''INSERT OR IGNORE INTO stream VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                        (iden, play.title, "Unknown Album", play.user['username'], 'S', 'S_' + str(play.id), 0, play.artwork_url))
                    self.db.commit()

                    duplifier.append(play.id)
                    duplifier.append(track['origin']['id'])
                    iden += 1
            else:
                self.cursor.execute('''INSERT OR IGNORE INTO stream VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (iden, track['origin']['title'], "Unknown Album", track['origin']['user']['username'], 's', 's_' + str(track['origin']['id']), 0, track['origin']['artwork_url']))
                self.db.commit()

                duplifier.append(track['origin']['id'])
                iden += 1
            if iden == 50:
                break

        self.db.commit()

    def get_watched(self):
        local_music = self.get_source(SourceType.LOCAL)
        if local_music is None:
            return
        return local_music.get_watched()

    def add_watched(self, directory):
        local_music = self.get_source(SourceType.LOCAL)
        if local_music is None:
            local_music = LocalMusic(self)
            self.sources.append(local_music)
        return local_music.add_watched(directory)

    def remove_watched(self, directory):
        local_music = self.get_source(SourceType.LOCAL)
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
