# -*- coding: utf-8 -*-

from .playlist import Playlist


class Album(Playlist):

    def __init__(self, library, id, name, artist=None):
        super(Album, self).__init__(library, id, name)

        self.artist = artist

    def set_artist(self, artist):
        self.artist = artist

        return self
