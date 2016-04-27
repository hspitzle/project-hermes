from os import path

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
