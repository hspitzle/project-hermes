from Library import *

import soundcloud
from gmusicapi import Mobileclient
from gmusicapi import Webclient
import urllib3.contrib.pyopenssl
import requests

requests.packages.urllib3.disable_warnings()
urllib3.contrib.pyopenssl.inject_into_urllib3()


class Client_Handler:
	
	def __init__(self,user):
		self.GOOGLE_DEVICE_ID = user.GOOGLE_DEVICE_ID
		self.SOUNDCLOUD_CLIENT_ID = user.SOUNDCLOUD_CLIENT_ID

		print "Logging into Google Play... ",
		self.G_client = Mobileclient()
		logged_in = self.G_client.login(user.G_username,user.G_password)
		if logged_in == True:
			print "Success"
		else:
			print "Failed"
		print "Logging into Soundcloud... ",
		self.S_client = soundcloud.Client(client_id=user.SOUNDCLOUD_CLIENT_ID,
                           client_secret=user.SOUNDCLOUD_CLIENT_SECRET_ID,
                           username=user.S_username,
                           password=user.S_password)
		print "Success"
	
	def get_stream_URL(self,track):
		if track.location == 'G':
			return self.G_client.get_stream_url(track.stream_id,self.GOOGLE_DEVICE_ID)
		elif track.location == 'S':
			return self.S_client.get(track.stream_string).stream_url + "?client_id=" + self.SOUNDCLOUD_CLIENT_ID
		else:
			print "Error: Track not found"


	
