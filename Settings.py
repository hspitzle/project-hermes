from os import path
import base64

global next_id
next_id = 0

def get_next_id():
    global next_id
    next_id += 1;
    return next_id-1


global pathman
pathman = {}

pathman["assets"] = "assets"
pathman["button_dir"] = path.join(pathman["assets"], "buttons")


global buttons
buttons = {}
buttons["next"] = path.join(pathman["button_dir"], "next.png")
buttons["prev"] = path.join(pathman["button_dir"], "prev.png")
buttons["record"] = path.join(pathman["button_dir"], "record.png")
buttons["play"] = path.join(pathman["button_dir"], "play_fill.png")
buttons["pause"] = path.join(pathman["button_dir"], "pause_nofill.png")
buttons["queue"] = path.join(pathman["button_dir"], "addtoqueue.png")
buttons["browse"] = path.join(pathman["button_dir"], "search.png")

def add_path_dir(key, dirname, prefix = None):
    if prefix is not None:
        dirname = path.join(pathman[prefix], dirname)
    print "Adding directory:", dirname
    pathman[key] = dirname
    if not path.exists(dirname):
        os.mkdir(dirname)

def add_path_file(key, filename, prefix = None):
    if prefix is not None:
        filename = path.join(pathman[prefix], filename)
    print "Adding file:", filename
    pathman[key] = filename
    if not path.exists(filename):
        open(filename, 'w').close()

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
