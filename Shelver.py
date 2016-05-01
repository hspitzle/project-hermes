__author__ = 'spitz'

import shelve
from os import path

import Settings


class Shelver(object):
    def __init__(self, title, user):
        self.title = title
        self.user = user
        self.items = []

    def get_shelve(self):
        return path.join(Settings.pathman["user"], self.title)

    def save(self):
        shelf = shelve.open(self.get_shelve(), 'c')
        shelf[self.title] = self.items
        shelf.close()

    def load(self):
        if not path.exists(self.get_shelve()):
            self.save()
            return
        shelf = shelve.open(self.get_shelve(), 'r')
        self.items = shelf[self.title]
        shelf.close()
