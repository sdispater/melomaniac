# -*- coding: utf-8 -*-


class Artist(object):

    def __init__(self, library, id, name):
        self.id = id
        self.name = name
        self._albums = []
        self._library = library
        self.current_album = 0

    @property
    def albums(self):
        return self._albums

    def add_album(self, album):
        self._albums.append(album.set_artist(self))

        return self

    def count(self):
        return len(self._albums)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)
