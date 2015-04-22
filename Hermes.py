from User import *
from ClientHandler import *
from Player import *

def play(title, cursor):
	if len(title) > 0:
		cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (title,))
		track = cursor.fetchone()
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	else:
		player.play()

def stop(title, cursor):
	player.stop()

def add(title, cursor):
	cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (title,))
	track = cursor.fetchone()
	player.add(track[1].encode("utf-8"), track[2].encode("utf-8"), track[0])

def print_queue(title, cursor):
	player.print_queue(cursor)
def pause(title, cursor):
	player.pause()
def next(title, cursor):
	player.play_next()
def prev(title, cursor):
	player.play_prev()
def start(title, cursor):
	player.play_queue()
def clear_queue(title, cursor):
	player.clear_queue()
def sync(title, cursor):
	user.sync(client)


print "   ___           _           _                        "                    
print "  / _ \\_ __ ___ (_) ___  ___| |_       /\\  /\\___ _ __ _ __ ___   ___  ___" 
print " / /_)/ '__/ _ \\| |/ _ \\/ __| __|____ / /_/ / _ \\ '__| '_ ` _ \\ / _ \\/ __|"
print "/ ___/| | | (_) | |  __/ (__| ||_____/ __  /  __/ |  | | | | | |  __/\__ \\"
print "\\/    |_|  \\___// |\\___|\\___|\\__|    \\/ /_/ \\___|_|  |_| |_| |_|\\___||___/"
print "              |__/   \n"                                                     


user = User()
client = Client_Handler(user)
player = Player()
player.client = client

print ""

func_dict = {
	'play' : play,
	'stop' : stop,
	'add'  : add,
	'print': print_queue,
	'pause': pause,
	'next' : next,
	'prev' : prev,
	'start': start,
	'clear': clear_queue,
	'sync' : sync
}

def intersect(res, inp):
	if(len(res) == 0):
		for row in inp:
	    		 res.add(row)
	else:
		temp = set()
		for row in inp:
	    		 temp.add(row)
		res = res.intersection(temp)
	return res

while(True):
	USI = raw_input("$> ")

	if len(USI.split()) > 1:
		command, tail = USI.split()
	else:
		command = USI
		tail = ''

	if command == 'quit':
		user.db.close()
		break
	elif command in func_dict.keys():
		func_dict[command](tail, user.cursor)
	else:
		Art_res = set()
		Alb_res = set()
		Tra_res = set()
		for word in USI.split():
			user.cursor.execute("SELECT DISTINCT(artist) FROM tracks WHERE artist LIKE ? OR artist LIKE ? ORDER BY artist", (word+'%', '% '+word+'%',))
			all_rows = user.cursor.fetchall()
			Art_res = intersect(Art_res, all_rows)
			
			user.cursor.execute("SELECT DISTINCT(album) FROM tracks WHERE album LIKE ? OR album LIKE ? ORDER BY album", (word+'%', '% '+word+'%',))
			all_rows = user.cursor.fetchall()
			Alb_res = intersect(Alb_res, all_rows)
			
			user.cursor.execute("SELECT DISTINCT(id), artist, album, title FROM tracks WHERE title LIKE ? OR title LIKE ? ORDER BY artist, album", (word+'%', '% '+word+'%',))
			all_rows = user.cursor.fetchall()
			Tra_res = intersect(Tra_res, all_rows)

		print "\n...ARTISTS..............."
		for [artist] in Art_res:
			print artist
		print "\n...ALBUMS..............."
		for [album] in Alb_res:
			print album
		print "\n...TRACKS..............."
		for [ident,artist,album,track] in Tra_res:
			print ident, '\t', artist.encode("utf-8"), ' - ', album.encode("utf-8"), ' - ', track.encode("utf-8")
