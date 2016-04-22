from Shelver import *
from Source import *

class Library:
    def __init__(self, cursor, user):
        self.cursor = cursor
        self.sources = []
        self.user = user
        self.add_source(LocalMusic(self, user))
        self.next_id = 0


    def get_next_id(self):
        self.next_id += 1;
        return self.next_id-1

    def add_source(self, source):
        self.sources.append(source)

    def get(self, distinct, get_others, where_like, ordered_return, USI, single=False, db='tracks'):
        print "searching...#$%"
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
        self.next_id = self.user.cursor.fetchone()[0]

        # local_tracks = []
        # for path in self.watched:
        #     filelist = []
        #     for (dirpath, dirnames, filenames) in os.walk(path):
        #         filelist.extend(dirpath + '/' + filename for filename in filenames)
        #     local_tracks += filelist
        #
        # for File in local_tracks:
        #     if not (File.endswith('.mp3') or File.endswith('.wav')):
        #         local_tracks.remove(File)
        #
        # for track in local_tracks:
        #     tag = eyeD3.Tag()
        #     tag.link(track)
        #     if len(tag.getArtist()) and len(tag.getAlbum()) and len(tag.getTitle()) > 0:
        #         self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
        #                             (iden, tag.getTitle(), tag.getAlbum(), tag.getArtist(), 'L', 'L_' + str(track), tag.track_num[0], ''))
        #         iden += 1
        #     else:
        #         print "Could not resolve track metadata for: " + track

        self.sources[0].sync()

        # gmusic_tracks = self.client.G_client.get_all_songs()
        # for track in gmusic_tracks:
        #     art = ''
        #     try:
        #         art = track['albumArtRef'][0]['url']
        #     except KeyError:
        #         art = ''
        #     self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
        #                         (iden, track['title'], track['album'], track['artist'], 'G', 'G_' + str(track['id']), track['trackNumber'], art))
        #     iden += 1

        # Fav_Size = 0
        # S_list = client.S_client.get('/me/favorites', limit=300)
        # while Fav_Size != len(S_list):
        #     Fav_Size = len(S_list)
        #     S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

        # for track in S_list:
        #     self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
        #                         (iden, track.title, "Unknown Album", track.user['username'], 'S', 'S_' + str(track.id), 0, track.artwork_url))
        #     iden += 1

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
