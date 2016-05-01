import soundcloud
from gmusicapi import Mobileclient
from gmusicapi import Webclient
import urllib3.contrib.pyopenssl
import requests

requests.packages.urllib3.disable_warnings()
urllib3.contrib.pyopenssl.inject_into_urllib3()

class ClientHandler:

    def __init__(self, user):
        # self.GOOGLE_DEVICE_ID = user.GOOGLE_DEVICE_ID
        self.SOUNDCLOUD_CLIENT_ID = user.SOUNDCLOUD_CLIENT_ID

        # self.G_client = Mobileclient()
        #
        # print user.G_username
        # print user.G_password
        #
        # logged_in = self.G_client.login(user.G_username,user.G_password, Mobileclient.FROM_MAC_ADDRESS)
        # print "Google logged in:", logged_in

        # self.S_client = soundcloud.Client(client_id=user.SOUNDCLOUD_CLIENT_ID, client_secret=user.SOUNDCLOUD_CLIENT_SECRET_ID, username=user.S_username, password=user.S_password)

    def get_stream_URL(self, song_id, location):
        if location == 'G':
            return self.G_client.get_stream_url(song_id,self.GOOGLE_DEVICE_ID)
        elif location.upper() == 'S':
            return self.S_client.get('/tracks/' + str(song_id)).stream_url + "?client_id=" + self.SOUNDCLOUD_CLIENT_ID
        elif location == 'L':
            return song_id
        else:
            print "Error: Track not found"
