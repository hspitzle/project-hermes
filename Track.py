from Library import *

class Track(object):
    def __init__(self, source):
        self._source = source

    def get_url(self):
        pass

    def get_artwork(self):
        pass

    def get_source(self):
        return self._source

class LocalTrack(Track):
    def __init__(self):
        Track.__init__(self, "local")

    
